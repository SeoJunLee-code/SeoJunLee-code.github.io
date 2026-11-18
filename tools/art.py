# -*- coding: utf-8 -*-
"""Generate image assets: hero planet (sharpened + city lights), milky way, card illustrations, footer ridge.
Run: python3 -I tools/art.py   (needs Pillow + numpy); add --ridge-only to rewrite only assets/img/ridge.svg"""
import math, random, pathlib, sys
import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"

# ---------------------------------------------------------------- footer mountain ridge (SVG)
# Two low faces in the bottom part of a 1600x260 box; the back face always stays above the front one (no crossing),
# soft top gradient, faint rim. Aspect ratio is preserved (xMidYMax slice) so the ridge is never stretched.
# Regenerate only this file with:  python -I tools/art.py --ridge-only
def ridge(seed, base, rough, n=5):
    """ridged fractional noise -> mountain peaks; returns polyline (x,y) in the 1600x260 viewBox"""
    r = random.Random(seed); octs = []
    for o in range(n):
        f = 2 ** o; octs.append([r.random() for _ in range(int(6 * f) + 2)])
    def val(o, x):
        f = 2 ** o; t = x / 1600 * 6 * f; i = int(t); u = t - i; u = u * u * (3 - 2 * u)
        return octs[o][i] * (1 - u) + octs[o][i + 1] * u
    pts = []
    for x in range(0, 1601, 8):
        h = 0
        for o in range(n):
            v = 1 - abs(2 * val(o, x) - 1)          # ridged
            h += v ** 1.6 * (rough * 0.5 ** o)
        pts.append((x, max(130, base - h)))
    return pts
def write_ridge():
    def path(p): return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
    defs = ('<defs><linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b93e8" stop-opacity=".3"/><stop offset=".5" stop-color="#22397a" stop-opacity=".45"/><stop offset="1" stop-color="#0a1328" stop-opacity=".9"/></linearGradient>'
            '<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#132344" stop-opacity="1"/><stop offset=".6" stop-color="#08112a" stop-opacity="1"/><stop offset="1" stop-color="#02050b" stop-opacity="1"/></linearGradient></defs>')
    front = ridge(7, 258, 42)
    back = [(x, min(y, fy - 14)) for (x, y), (_, fy) in zip(ridge(21, 250, 60), front)]   # never below the front face
    layers = ""
    for p, grad, rim, op in [(back, "m1", "#b4ccff", .38), (front, "m2", "#86a2e6", .3)]:
        layers += (f'<path d="{path(p)} L1600 260 L0 260 Z" fill="url(#{grad})"/>'
                   f'<path d="{path(p)}" fill="none" stroke="{rim}" stroke-opacity="{op}" stroke-width="1.4"/>')
    (IMG / "ridge.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 260" preserveAspectRatio="xMidYMax slice">{defs}{layers}</svg>', encoding="utf-8")
    print("ridge ok")
if __name__ == "__main__" and "--ridge-only" in sys.argv:
    write_ridge(); sys.exit(0)

# ---------------------------------------------------------------- home card illustrations added later (SVG, no randomness)
# Same luminous line-art language as cards/h1.svg and cards/llm.svg: soft blue glow, thin bright strokes, one blur filter.
# Regenerate only these two files with:  python -I tools/art.py --cards-new   (the older card files are left untouched)
def card_svg(body, defs=""):
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="320" height="200" fill="none">'
            '<defs><filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
            '<radialGradient id="bg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#6f95ff" stop-opacity=".42"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient>'
            f'{defs}</defs><ellipse cx="160" cy="100" rx="158" ry="92" fill="url(#bg)"/>{body}</svg>')
def f1(v): return f"{v:.1f}".rstrip("0").rstrip(".")
def write_compaction():
    """Context compaction: three long rows of tokens (older ones dimmer) funnel into one short, dense block."""
    out = []
    rows = (66, 100, 134)
    for k, y0 in enumerate(rows):
        for i in range(9):                                   # the long context: evenly spaced token cells
            x = 14 + i * 15; op = .25 + .07 * i
            out.append(f'<rect x="{x}" y="{y0 - 7}" width="11" height="14" rx="2.5" stroke="#9db8ff" stroke-opacity="{f1(op)}" fill="#8fb0ff" fill-opacity="{f1(op * .25)}"/>')
        for j in range(6):                                   # the rows bend toward the middle while the cells shrink
            t = (j + 1) / 7; x = 150 + j * 13 - j * j * .9
            y = y0 + (100 - y0) * (3 * t * t - 2 * t * t * t); s = 1 - .1 * j
            out.append(f'<rect x="{f1(x)}" y="{f1(y - 7 * s)}" width="{f1(10 * s)}" height="{f1(14 * s)}" rx="2" stroke="#b9ceff" stroke-opacity="{f1(.6 + .06 * j)}" fill="#8fb0ff" fill-opacity=".14"/>')
        out.append(f'<path d="M140 {y0} C 190 {y0}, 196 100, 236 100" stroke="#8fb0ff" stroke-opacity=".28" stroke-width=".8"/>')
    out.append('<rect x="236" y="84" width="58" height="32" rx="7" fill="#9dbbff" fill-opacity=".16" stroke="#e1eaff" stroke-opacity=".95" stroke-width="1.4"/>')
    out.append("".join(f'<path d="M{243 + i * 4.4:.1f} 90 V110" stroke="#dbe6ff" stroke-opacity="{.55 + .04 * (i % 3):.2f}" stroke-width="1.2"/>' for i in range(11)))
    out.append('<circle cx="294" cy="84" r="9" fill="url(#st)"/><circle cx="294" cy="84" r="2.2" fill="#fff"/>')
    star = '<radialGradient id="st"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#cfe0ff" stop-opacity=".7"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient>'
    (IMG / "cards/compaction.svg").write_text(card_svg('<g filter="url(#g)">' + "".join(out) + "</g>", star), encoding="utf-8")
def write_forgetting():
    """Forgetting and review: a fixed set of memory slots, some kept, some fading out, circled by a review loop."""
    # 1 kept, 2 fading, 3 evicted (empty); fixed pattern, read left to right
    state = ((1, 2, 1, 3, 1, 2), (2, 1, 3, 1, 2, 1))
    out = []
    for r, row in enumerate(state):
        for c, s in enumerate(row):
            x, y = 70 + c * 32, 70 + r * 34
            if s == 1:
                out.append(f'<rect x="{x}" y="{y}" width="24" height="24" rx="5" fill="#9dbbff" fill-opacity=".2" stroke="#d6e4ff" stroke-opacity=".95" stroke-width="1.3"/>'
                           f'<circle cx="{x + 12}" cy="{y + 12}" r="3" fill="#eef4ff"/>')
            elif s == 2:
                out.append(f'<rect x="{x}" y="{y}" width="24" height="24" rx="5" fill="#8fb0ff" fill-opacity=".06" stroke="#9db8ff" stroke-opacity=".45" stroke-dasharray="3 3"/>'
                           f'<circle cx="{x + 12}" cy="{y + 12}" r="2.4" fill="#b9ceff" opacity=".35"/>')
            else:
                out.append(f'<rect x="{x}" y="{y}" width="24" height="24" rx="5" stroke="#8fb0ff" stroke-opacity=".18" stroke-dasharray="2 4"/>')
    # review loop: an open ellipse around the slots with an arrow head, and a bright point riding on it
    rx, ry, cx, cy = 132, 62, 160, 99
    def pt(a): return cx + rx * math.cos(math.radians(a)), cy + ry * math.sin(math.radians(a))
    a0, a1 = 200, 500
    pts = [pt(a0 + (a1 - a0) * i / 60) for i in range(61)]
    for k in range(6):                                       # brighter toward the arrow head
        seg = pts[k * 10:k * 10 + 11]
        out.append('<path d="M' + " L".join(f"{x:.1f} {y:.1f}" for x, y in seg) + f'" stroke="#d6e2ff" stroke-opacity="{.18 + .15 * k:.2f}" stroke-width="1.6" stroke-linecap="round"/>')
    (ex, ey), (px, py) = pts[-1], pts[-3]
    ang = math.atan2(ey - py, ex - px); hx = lambda d, s: (ex - 9 * math.cos(ang + s * d), ey - 9 * math.sin(ang + s * d))
    (lx, ly), (qx, qy) = hx(.5, 1), hx(.5, -1)
    out.append(f'<path d="M{lx:.1f} {ly:.1f} L{ex:.1f} {ey:.1f} L{qx:.1f} {qy:.1f}" stroke="#e1eaff" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    sx, sy = pt(305)
    out.append(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="11" fill="url(#st)"/><circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.4" fill="#fff"/>')
    defs = ('<radialGradient id="st"><stop offset="0" stop-color="#fff"/><stop offset=".4" stop-color="#cfe0ff" stop-opacity=".7"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient>')
    (IMG / "cards/forgetting.svg").write_text(card_svg('<g filter="url(#g)">' + "".join(out) + "</g>", defs), encoding="utf-8")
if __name__ == "__main__" and "--cards-new" in sys.argv:
    write_compaction(); write_forgetting(); print("new cards ok"); sys.exit(0)


# ---------------------------------------------------------------- hero planet: upscale, sharpen, warm city lights
src = Image.open(ROOT / "tools/src/horizon_frame0.png").convert("RGB")
W = 2400; H = round(src.size[1] * W / src.size[0]); sc = W / src.size[0]
im = src.resize((W, H), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=3, percent=140, threshold=2))
im.save(IMG / "horizon_cool.webp", quality=84, method=6)   # intro: cold blue-white like the GIF
rnd = np.random.default_rng(5)
lights = Image.new("RGB", (W, H), (0, 0, 0)); d = ImageDraw.Draw(lights)
cx = 254 * sc; crest = 262 * sc; k = 0.000542 / sc          # limb arc measured on the source frame
def limb(x): return crest + k * (x - cx) ** 2
n = 2600
for _ in range(n):
    x = rnd.normal(cx, 520); y = limb(x) + abs(rnd.normal(0, 0.18)) * (H - crest) + 10
    if not (0 <= x < W and 0 <= y < H - 2): continue
    cluster = 0.5 + 0.5 * math.sin(x / 90) * math.cos(y / 70)
    a = int(255 * rnd.uniform(.25, 1) * max(.15, cluster))
    r = rnd.choice([1.2, 1.6, 2.2, 3.0])
    d.ellipse([x - r, y - r, x + r, y + r], fill=(a, int(a * .62), int(a * .28)))
lights = lights.filter(ImageFilter.GaussianBlur(1.1))
lights = Image.eval(lights, lambda v: int(v * .8))
im = ImageChops.screen(im, lights)
# crisp warm sun-glow right on the crest (mockup shows an orange-white core)
glow = Image.new("RGB", (W, H), (0, 0, 0)); gd = ImageDraw.Draw(glow)
for rr, col in [(260, (60, 36, 14)), (150, (110, 70, 30)), (70, (190, 140, 80)), (26, (255, 230, 190))]:
    gd.ellipse([cx - rr * 1.9, crest - rr * .55, cx + rr * 1.9, crest + rr * .55], fill=col)
glow = glow.filter(ImageFilter.GaussianBlur(38))
im = ImageChops.screen(im, glow)
im.save(IMG / "horizon.webp", quality=84, method=6)
print("horizon", im.size)

# ---------------------------------------------------------------- milky way (screen-blended on dark), smooth float noise
def gblur(a, sigma):
    ky = np.fft.fftfreq(a.shape[0])[:, None]; kx = np.fft.fftfreq(a.shape[1])[None, :]
    return np.real(np.fft.ifft2(np.fft.fft2(a) * np.exp(-2 * (np.pi * sigma) ** 2 * (kx ** 2 + ky ** 2))))
def field(shape, sigma, seed):
    f = gblur(np.random.default_rng(seed).standard_normal(shape), sigma); return (f - f.mean()) / (f.std() + 1e-9)
Hh, Ww = 450, 800                                   # generated at half size, upsampled smoothly
yy, xx = np.mgrid[0:Hh, 0:Ww].astype(float)
x0, y0, x1, y1 = Ww * 1.03, -20, -Ww * 0.05, Hh * 0.74
dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy)
dist = np.abs((xx - x0) * dy - (yy - y0) * dx) / L
along = ((xx - x0) * dx + (yy - y0) * dy) / (L * L)
width = 70 + 50 * np.clip(1 - np.abs(along - .28) * 2.2, 0, 1)
band = np.exp(-(dist / width) ** 2) * np.clip(1.2 - along * .75, 0, 1)
turb = np.clip(.75 + .10 * field((Hh, Ww), 16, 1) + .12 * field((Hh, Ww), 5, 2) + .09 * field((Hh, Ww), 1.6, 3), 0, 1.3)
dust = np.clip(.5 + .42 * field((Hh, Ww), 9, 4), 0, 1) ** 1.8
dens = np.clip(band * turb * (1 - .5 * dust), 0, 1)
core = np.clip(dens * 1.5, 0, 1)
col = np.stack([14 + 52 * core ** 1.5, 40 + 88 * core ** 1.2, 112 + 128 * core], -1)
img = col * dens[..., None] * .72
big = Image.fromarray(np.clip(img, 0, 255).astype("uint8")).resize((1600, 900), Image.BICUBIC).filter(ImageFilter.GaussianBlur(.8))
st = np.zeros((900, 1600)); r = np.random.default_rng(8)
bandfull = np.asarray(Image.fromarray((band * 255).astype("uint8")).resize((1600, 900), Image.BICUBIC), dtype=float) / 255
for _ in range(5200):
    x, y = int(r.uniform(0, 1600)), int(r.uniform(0, 720))
    if r.random() < min(.2 + 1.5 * bandfull[y, x], 1): st[y, x] = r.uniform(.35, 1) ** 2
stl = np.asarray(Image.fromarray((np.clip(st, 0, 1) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(.6)), dtype=float)
out = np.clip(np.asarray(big, dtype=float) + stl[..., None] * np.array([1, 1, 1.08]) * 1.3, 0, 255)
Image.fromarray(out.astype("uint8")).save(IMG / "milkyway.webp", quality=90, method=6)
print("milkyway ok")

# ---------------------------------------------------------------- card illustrations (SVG)
def svg(w, h, body, defs="", shift=0):
    w += shift; body = f'<g transform="translate({shift} 0)">{body}</g>' if shift else body
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" fill="none">'
            f'<defs><filter id="g" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.2" result="b"/>'
            f'<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>{defs}</defs>{body}</svg>')
CARDS = IMG / "cards"
# 1) KORE: luminous flowing ribbons + particles
rr = random.Random(3); b = []
def bez(p0, p1, p2, p3, t):
    u = 1 - t; return (u**3*p0[0] + 3*u*u*t*p1[0] + 3*u*t*t*p2[0] + t**3*p3[0], u**3*p0[1] + 3*u*u*t*p1[1] + 3*u*t*t*p2[1] + t**3*p3[1])
ribbons = [((6, 150), (90, 40), (170, 190), (318, 40), "#8fb2ff"), ((6, 160), (100, 70), (190, 170), (318, 66), "#6f98ff"),
           ((6, 140), (80, 20), (160, 150), (318, 20), "#b9ceff"), ((6, 170), (110, 100), (200, 150), (318, 96), "#5b84f2")]
for (p0, p1, p2, p3, col) in ribbons:
    pts = [bez(p0, p1, p2, p3, i / 60) for i in range(61)]
    b.append(f'<path d="M{pts[0][0]:.1f} {pts[0][1]:.1f} ' + " ".join(f"L{x:.1f} {y:.1f}" for x, y in pts[1:]) + f'" stroke="{col}" stroke-opacity=".42" stroke-width=".9"/>')
    for i in range(150):
        t = rr.random(); x, y = bez(p0, p1, p2, p3, t); spread = 3 + 9 * math.sin(t * math.pi)
        o = rr.uniform(.2, 1) * (.25 + .75 * math.sin(t * math.pi) ** .6)
        rad = rr.choice([.5, .7, .9, 1.2, 1.7]) if rr.random() > .05 else 2.6
        b.append(f'<circle cx="{x + rr.gauss(0, spread):.1f}" cy="{y + rr.gauss(0, spread):.1f}" r="{rad}" fill="{col}" opacity="{o:.2f}"/>')
(CARDS / "kore.svg").write_text(svg(320, 200, '<g filter="url(#g)">' + "".join(b) + "</g>"), encoding="utf-8")
# 2) H1: backlit silhouettes
def head(cx, cy, s, op):
    return (f'<g opacity="{op}" transform="translate({cx} {cy}) scale({s})">'
            f'<path d="M-46 110 C-46 62 -26 48 0 44 C26 48 46 62 46 110 Z" fill="url(#sh)" stroke="#9db6ff" stroke-opacity=".6" stroke-width="1.3"/>'
            f'<ellipse cx="0" cy="12" rx="21" ry="26" fill="url(#sh)" stroke="#b4c8ff" stroke-opacity=".85" stroke-width="1.4"/></g>')
defs = ('<linearGradient id="sh" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#22366a"/><stop offset="1" stop-color="#060b1b"/></linearGradient>'
        '<radialGradient id="bk" cx=".5" cy=".35" r=".6"><stop offset="0" stop-color="#6f95ff" stop-opacity=".55"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient>')
body = '<ellipse cx="160" cy="70" rx="170" ry="90" fill="url(#bk)"/>' + head(58, 70, .9, .5) + head(262, 72, .9, .5) + head(108, 56, 1.1, .78) + head(210, 56, 1.1, .78) + head(160, 40, 1.3, 1)
body += "".join(f'<circle cx="{rr.uniform(10,310):.0f}" cy="{rr.uniform(8,110):.0f}" r="{rr.choice([.7,1,1.5])}" fill="#b4c8ff" opacity="{rr.uniform(.3,.9):.2f}"/>' for _ in range(46))
(CARDS / "h1.svg").write_text(svg(320, 200, body, defs, shift=95), encoding="utf-8")
# 3) Paper 5: brain with contour + denser network
rr = random.Random(11)
def inside(x, y):
    def e(cx, cy, rx, ry): return ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1
    return e(150, 92, 100, 66) or e(105, 112, 52, 40) or e(205, 118, 46, 36) or e(168, 150, 24, 30)
pts = []
while len(pts) < 190:
    p = (rr.uniform(40, 270), rr.uniform(20, 190))
    if inside(*p) and all(math.dist(p, q) > 8.5 for q in pts): pts.append(p)
lines = []
for i, p in enumerate(pts):
    for j in sorted(range(len(pts)), key=lambda j: math.dist(p, pts[j]))[1:5]:
        if j > i and math.dist(p, pts[j]) < 30: lines.append(f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{pts[j][0]:.1f}" y2="{pts[j][1]:.1f}" stroke="#86a8ff" stroke-opacity=".5" stroke-width=".8"/>')
contour = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" stroke="#a9c3ff" stroke-opacity=".28" stroke-width="1"/>' for cx, cy, rx, ry in [(150, 92, 100, 66), (105, 112, 52, 40), (205, 118, 46, 36), (168, 150, 24, 30)])
nodes = "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr.choice([1.3,1.8,2.4,3.4]):.1f}" fill="#d6e5ff" opacity="{rr.uniform(.55,1):.2f}"/>' for x, y in pts)
glow = '<radialGradient id="bg2" cx=".5" cy=".45" r=".6"><stop offset="0" stop-color="#5f86f0" stop-opacity=".35"/><stop offset="1" stop-color="#5f86f0" stop-opacity="0"/></radialGradient>'
(CARDS / "paper5.svg").write_text(svg(320, 200, '<ellipse cx="160" cy="100" rx="150" ry="95" fill="url(#bg2)"/><g filter="url(#g)">' + contour + "".join(lines) + nodes + "</g>", glow, shift=70), encoding="utf-8")
# 4) LLM: glowing wireframe cube
def iso(x, y, z, s=34, ox=160, oy=118):
    return (ox + (x - y) * s * .866, oy + (x + y) * s * .5 - z * s)
ln = []; N = 4
for a_ in range(N + 1):
    for b_ in range(N + 1):
        for (p, q) in [((a_, b_, 0), (a_, b_, N)), ((a_, 0, b_), (a_, N, b_)), ((0, a_, b_), (N, a_, b_))]:
            (x1, y1), (x2, y2) = iso(*p), iso(*q); edge = a_ in (0, N) and b_ in (0, N)
            ln.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{"#cfe0ff" if edge else "#8fb0ff"}" stroke-opacity="{.95 if edge else .32}" stroke-width="{1.4 if edge else .7}"/>')
verts = "".join(f'<circle cx="{iso(x,y,z)[0]:.1f}" cy="{iso(x,y,z)[1]:.1f}" r="2" fill="#fff" opacity=".95"/>' for x in range(N + 1) for y in range(N + 1) for z in (0, N) if x in (0, N) and y in (0, N))
core = '<radialGradient id="cg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#9dbbff" stop-opacity=".55"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient>'
(CARDS / "llm.svg").write_text(svg(320, 220, '<ellipse cx="160" cy="98" rx="120" ry="95" fill="url(#cg)"/><g filter="url(#g)">' + "".join(ln) + verts + "</g>", core), encoding="utf-8")

write_ridge()
print("cards ok")
