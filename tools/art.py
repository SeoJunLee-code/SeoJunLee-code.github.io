# -*- coding: utf-8 -*-
"""Generate image assets: hero planet (sharpened + city lights), milky way, card illustrations, footer ridge.
Run: python3 -I tools/art.py   (needs Pillow + numpy)"""
import math, random, pathlib
import numpy as np
from PIL import Image, ImageFilter, ImageChops, ImageDraw

ROOT = pathlib.Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"

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

# ---------------------------------------------------------------- footer mountain ridge (SVG)
def ridge(seed, base, rough, n=5):
    """ridged fractional noise -> sharp mountain peaks; returns polyline (x,y) in the 1600x260 viewBox"""
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
        pts.append((x, max(14, base - h)))
    return pts
def path(p): return "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in p)
layers = ""
defs = ('<defs><linearGradient id="m1" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#6b93e8" stop-opacity=".75"/><stop offset=".5" stop-color="#22397a" stop-opacity=".6"/><stop offset="1" stop-color="#0a1328" stop-opacity=".95"/></linearGradient>'
        '<linearGradient id="m2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#16284f" stop-opacity="1"/><stop offset=".6" stop-color="#08112a" stop-opacity="1"/><stop offset="1" stop-color="#02050b" stop-opacity="1"/></linearGradient>'
        '<filter id="rg"><feGaussianBlur stdDeviation="1.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>')
for seed, base, rough, grad, rim, op in [(21, 222, 128, "m1", "#b4ccff", .95), (7, 246, 96, "m2", "#86a2e6", 1)]:
    p = ridge(seed, base, rough, n=5)
    layers += (f'<path d="{path(p)} L1600 260 L0 260 Z" fill="url(#{grad})" opacity="{op}"/>'
               f'<path d="{path(p)}" fill="none" stroke="{rim}" stroke-opacity=".85" stroke-width="1.7" filter="url(#rg)"/>')
(IMG / "ridge.svg").write_text(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 260" preserveAspectRatio="none">{defs}{layers}</svg>', encoding="utf-8")
print("cards + ridge ok")
