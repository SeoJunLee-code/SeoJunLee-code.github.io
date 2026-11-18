# -*- coding: utf-8 -*-
"""Run: python3 -I -m unittest discover -s tests -v   (from the site root)"""
import json, pathlib, re, subprocess, sys, unittest, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
NX = pathlib.Path("/home/user/repos/Nexus-.github.io")
PAGES = [p for p in ROOT.rglob("index.html")]
TEXTS = [*PAGES, ROOT / "404.html", *ROOT.glob("assets/**/*.css"), *ROOT.glob("assets/**/*.js"), *ROOT.glob("assets/**/*.svg"),
         ROOT / "data/research.json", *ROOT.glob("tools/*.py"), ROOT / "sitemap.xml", ROOT / "robots.txt"]
GENERIC = ["@gmail", "kore@example", "Our Research", "student", "high school"]
def _private_terms():
    """Real-name / school / account strings live in a file OUTSIDE this repo so they are never published.
    Set FORBIDDEN_FILE or place the list at ../aevorin-private/forbidden.txt (one term per line)."""
    import os
    f = pathlib.Path(os.environ.get("FORBIDDEN_FILE", ROOT.parent / "aevorin-private" / "forbidden.txt"))
    return [l.strip() for l in f.read_text(encoding="utf-8").splitlines() if l.strip()] if f.exists() else []
FORBIDDEN = GENERIC + _private_terms()

def vis(p):  # visible text only
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", p.read_text(encoding="utf-8"), flags=re.S)
    return H.unescape(re.sub(r"<[^>]+>", " ", t))

class Site(unittest.TestCase):
    def test_page_sets_match(self):
        en = {str(p.relative_to(ROOT)) for p in PAGES if "ko" not in p.parts}
        ko = {str(p.relative_to(ROOT / "ko")) for p in PAGES if "ko" in p.parts}
        self.assertEqual(en, ko); self.assertEqual(len(en), 15)

    def _scan(self, terms):
        for p in TEXTS:
            t = p.read_text(encoding="utf-8")
            for w in terms:
                self.assertNotIn(w.lower(), t.lower(), f"{w!r} in {p}")

    def test_no_forbidden_strings(self):  # generic terms: always checked
        self._scan(GENERIC)

    def test_no_private_forbidden_strings(self):  # real-name / school / account list kept outside the repo
        terms = _private_terms()
        if not terms: self.skipTest("private forbidden-term list not found (FORBIDDEN_FILE or ../aevorin-private/forbidden.txt)")
        self._scan(terms)

    def test_brand_and_badges(self):
        home, rs = H.unescape((ROOT / "index.html").read_text(encoding="utf-8")), H.unescape((ROOT / "research/index.html").read_text(encoding="utf-8"))
        for s in ["AEVORIN", "Independent AI Research & Engineering", "Beyond What ", "Exists.", "Exploring the boundaries of intelligence. Building what comes next."]:
            self.assertIn(s, home)
        for s in ["Prototype · Unvalidated", "Hypothesis Refuted", "In Progress", "Reproduction · Partial"]:
            self.assertIn(s, home); self.assertIn(s, rs)
        about = (ROOT / "about/index.html").read_text(encoding="utf-8")
        for s in ["Discover", "Construct", "Advance", "Aevum".lower(), "Human-led research direction", "AI-assisted implementation"]:
            self.assertIn(s, about if s != "Aevum".lower() else about.lower())
        self.assertIn('lang="ko"', (ROOT / "ko/index.html").read_text(encoding="utf-8"))

    def test_links_resolve(self):
        for p in PAGES + [ROOT / "404.html"]:
            t = p.read_text(encoding="utf-8")
            for u in re.findall(r'(?:href|src)="([^"]+)"', t):
                if re.match(r"(https?:|#|mailto:)", u) or u.startswith("/"): continue
                tgt = (p.parent / u.split("#")[0]).resolve()
                if tgt.is_dir(): tgt = tgt / "index.html"
                self.assertTrue(tgt.exists(), f"{u} from {p}")

    def test_numbers_come_from_data(self):
        data = json.loads((ROOT / "data/research.json").read_text(encoding="utf-8"))
        allowed = set()
        def walk(o):
            if isinstance(o, dict): [walk(v) for v in o.values()]
            elif isinstance(o, list): [walk(v) for v in o]
            elif isinstance(o, float):
                for v in (o, abs(o)):                       # sign is compared separately by the reader; magnitudes must come from data
                    for d in (2, 3, 4): allowed.add(f"{v:.{d}f}")
                    allowed.add(f"{v*100:.1f}"); allowed.add(f"{v*100:.0f}")
        walk(data)
        extra = {"0.50", "0.5", "0.8", "0.7", "0.000", "0.0005"}  # thresholds quoted from decision rules / prose
        for p in PAGES:
            if "research" not in p.parts or p.parent.name == "research": continue
            for n in re.findall(r"(?<![\d.])\d\.\d{2,4}(?![\d])", vis(p)):
                self.assertTrue(n in allowed or n in extra or n.lstrip("0") in allowed, f"{n} on {p} not traceable to data")

    def test_data_matches_sources(self):
        if not NX.exists(): self.skipTest("Nexus clone not present")
        before = (ROOT / "data/research.json").read_bytes()
        subprocess.run([sys.executable, "-I", str(ROOT / "tools/extract.py"), str(NX)], check=True, capture_output=True)
        self.assertEqual(before, (ROOT / "data/research.json").read_bytes(), "data/research.json differs from a fresh extraction")

    def test_hand_verified_blocks_are_flagged(self):
        d = json.loads((ROOT / "data/research.json").read_text(encoding="utf-8"))
        for k in (d["paper5"]["phase2b"], d["llm_internal"], d["study4"]): self.assertIn("verified", k)

# ---------------------------------------------------------------- structure, metadata, fonts (added with the design pass)
from html.parser import HTMLParser
SITE = "https://seojunlee-code.github.io"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
HANGUL = re.compile(r"[ᄀ-ᇿ㄰-㆏가-힣]")
EN_PAGES = [p for p in PAGES if "ko" not in p.relative_to(ROOT).parts]
KO_PAGES = [p for p in PAGES if "ko" in p.relative_to(ROOT).parts]
DETAIL = [p for p in PAGES if p.parent.parent.name == "research"]
def rel_path(p):  # 'research/kore/' for research/kore/index.html, '' for the home page
    parts = p.relative_to(ROOT).parts[:-1]
    if parts and parts[0] == "ko": parts = parts[1:]
    return "".join(x + "/" for x in parts)
def page_url(p): return SITE + "/" + ("ko/" if p in KO_PAGES else "") + rel_path(p)
def content_build(lang):
    sys.path.insert(0, str(ROOT / "tools"))
    from content import build
    return build(lang, json.loads((ROOT / "data/research.json").read_text(encoding="utf-8")))

class LangText(HTMLParser):
    """Collects (text, nearest lang) for body text outside script/style/title."""
    def __init__(self):
        super().__init__(); self.stack = []; self.out = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs); parent = self.stack[-1][1] if self.stack else None
        self.stack.append((tag, a.get("lang", parent)))
    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag: del self.stack[i:]; break
    def handle_data(self, d):
        if not d.strip() or any(t in ("script", "style", "title") for t, _ in self.stack): return
        self.out.append((d, self.stack[-1][1] if self.stack else None))

def css_blocks(css):
    """Yields (media context, selector text) for every rule block; @keyframes blocks are skipped."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S)
    ctx, buf, i = [], "", 0
    while i < len(css):
        c = css[i]
        if c == "{":
            head = " ".join(buf.split()); buf = ""
            if head.startswith("@keyframes"):
                d = 0
                while True:
                    if css[i] == "{": d += 1
                    elif css[i] == "}":
                        d -= 1
                        if d == 0: break
                    i += 1
            elif head.startswith("@media"):
                yield ("@", head); ctx.append(head)
            else:
                yield (ctx[-1] if ctx else "", head); ctx.append(None)
        elif c == "}":
            if ctx: ctx.pop()
            buf = ""
        else:
            buf += c
        i += 1

class Structure(unittest.TestCase):
    def test_en_hangul_inside_lang_ko(self):
        for p in EN_PAGES + [ROOT / "404.html"]:
            lt = LangText(); lt.feed(p.read_text(encoding="utf-8"))
            for text, lang in lt.out:
                if HANGUL.search(text): self.assertEqual(lang, "ko", f"Korean outside lang=ko on {p}: {text.strip()[:60]!r}")

    def test_ko_titles(self):
        for p in KO_PAGES:
            if rel_path(p) == "": continue
            title = re.search(r"<title>(.*?)</title>", p.read_text(encoding="utf-8")).group(1)
            for w in ("Research ·", "Projects ·", "About ·", "Contact ·"): self.assertNotIn(w, title, p)

    def test_head_meta(self):
        descs = {"en": set(), "ko": set()}
        for p in PAGES:
            t = p.read_text(encoding="utf-8"); u = page_url(p); path = rel_path(p)
            canon = re.search(r'<link rel="canonical" href="([^"]+)">', t)
            self.assertTrue(canon and canon.group(1) == u, f"canonical on {p}")
            for lang, href in (("en", f"{SITE}/{path}"), ("ko", f"{SITE}/ko/{path}"), ("x-default", f"{SITE}/{path}")):
                self.assertIn(f'<link rel="alternate" hreflang="{lang}" href="{href}">', t, p)
            for prop in ("og:title", "og:description", "og:url", "og:type", "og:locale", "og:site_name"):
                self.assertRegex(t, rf'<meta property="{prop}" content="[^"]+">', f"{prop} on {p}")
            self.assertIn(f'<meta property="og:url" content="{u}">', t)
            self.assertRegex(t, r'<meta name="twitter:card" content="summary(_large_image)?">')
            self.assertIn(f'<meta property="og:type" content="{"article" if p in DETAIL else "website"}">', t, p)
            d = re.search(r'<meta name="description" content="([^"]*)">', t).group(1)
            self.assertTrue(0 < len(H.unescape(d)) <= 200, f"description length on {p}")
            self.assertNotRegex(d, r"<|&lt;|&amp;amp;", f"tag or double escape in description on {p}")
            descs["ko" if p in KO_PAGES else "en"].add(d)
        self.assertEqual(len(descs["en"]), 15); self.assertEqual(len(descs["ko"]), 15)

    def test_sitemap_robots(self):
        sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        locs = re.findall(r"<loc>([^<]+)</loc>", sm)
        self.assertEqual(sorted(locs), sorted(page_url(p) for p in PAGES)); self.assertEqual(len(locs), 30)
        for block in re.findall(r"<url>(.*?)</url>", sm):
            self.assertEqual(len(re.findall(r'<xhtml:link rel="alternate" hreflang="(en|ko|x-default)"', block)), 3)
        self.assertIn(f"Sitemap: {SITE}/sitemap.xml", (ROOT / "robots.txt").read_text(encoding="utf-8"))

    def test_css_no_duplicate_blocks(self):
        seen = set()
        for key in css_blocks((ROOT / "assets/css/site.css").read_text(encoding="utf-8")):
            self.assertNotIn(key, seen, f"repeated in the same context: {key}"); seen.add(key)

    def test_visible_chars_in_font_subset(self):
        allowed = set((ROOT / "tools/font_chars.txt").read_text(encoding="utf-8"))
        for p in PAGES + [ROOT / "404.html"]:
            t = re.sub(r"<title>.*?</title>", "", p.read_text(encoding="utf-8"), flags=re.S)
            t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.S)
            text = H.unescape(re.sub(r"<[^>]+>", " ", t))
            bad = {c for c in text if c not in allowed and not c.isspace()}
            self.assertFalse(bad, f"characters missing from the font subset on {p}: {''.join(sorted(bad))}")
        css = (ROOT / "assets/css/site.css").read_text(encoding="utf-8")
        for s in re.findall(r'content:\s*"([^"]*)"', css):
            self.assertFalse({c for c in s if c not in allowed and not c.isspace()}, s)

    def test_404(self):
        t = (ROOT / "404.html").read_text(encoding="utf-8")
        for s in ('class="nav"', 'class="foot"', 'lang="ko"', 'content="noindex"', 'class="skip"', 'rel="icon"'): self.assertIn(s, t)
        self.assertNotIn(' style="', t)
        for u in re.findall(r'(?:href|src)="([^"]+)"', t):
            # root-absolute or external; the only exception is the same-page skip link (#main)
            self.assertTrue(u.startswith("/") or u.startswith("https:") or u == "#main", u)

    def test_home_cards(self):
        want = ["context-compaction", "ai-forgetting-review", "h1", "llm-internal-computing"]
        plain = lambda s: H.unescape(re.sub(r"<[^>]+>", "", s))
        for lang, p in (("en", ROOT / "index.html"), ("ko", ROOT / "ko/index.html")):
            t = p.read_text(encoding="utf-8"); one = {r["id"]: r["one"] for r in content_build(lang)["research"]}
            cards = re.findall(r'<a class="card" data-id="([^"]+)".*?<p class="one">(.*?)</p>', t, flags=re.S)
            self.assertEqual([c[0] for c in cards], want)
            for cid, text in cards: self.assertEqual(plain(text), plain(one[cid]))
            self.assertNotIn('class="art"', t)  # the old absolutely positioned card art (overlapped the text) stays gone
            # each card band holds exactly one decorative drawing: aria-hidden band, inline SVG <image>, no text, small file
            bands = re.findall(r'<a class="card" data-id="([^"]+)"[^>]*><span class="card-band" aria-hidden="true">(.*?)</span>', t, flags=re.S)
            self.assertEqual([b[0] for b in bands], want)
            seen = set()
            for cid, inner in bands:
                imgs = re.findall(r'<image href="([^"]+)"', inner)
                self.assertEqual(len(imgs), 1, cid); self.assertNotIn("<text", inner)
                f = (p.parent / imgs[0]).resolve()
                self.assertEqual(f.parent, (ROOT / "assets/img/cards").resolve(), cid); self.assertTrue(f.exists(), f)
                self.assertLess(f.stat().st_size, 25000 if f.name in ("compaction.svg", "forgetting.svg") else 60000, f)
                self.assertNotIn("<text", f.read_text(encoding="utf-8")); seen.add(f.name)
            self.assertEqual(len(seen), len(want), "every home card shows its own drawing")

    def test_heading_order(self):
        for p in PAGES + [ROOT / "404.html"]:
            levels = [int(x) for x in re.findall(r"<h([1-6])[\s>]", p.read_text(encoding="utf-8"))]
            for a, b in zip(levels, levels[1:]): self.assertLessEqual(b - a, 1, f"heading h{a} -> h{b} on {p}")

    def test_detail_structure(self):
        self.assertEqual(len(DETAIL), 20)
        for p in DETAIL:
            t = p.read_text(encoding="utf-8")
            self.assertIn('class="result"', t, p); self.assertIn('class="pager"', t, p)
            article = t[t.index("<article"):t.index("</article>")]
            h2 = re.findall(r'<h2 id="([^"]+)"', article)
            toc = re.search(r'<nav class="toc".*?</nav>', t, flags=re.S)
            if len(h2) >= 6:
                self.assertTrue(toc, p); self.assertEqual(re.findall(r'href="#([^"]+)"', toc.group(0)), h2)
            else:
                self.assertIsNone(toc, p)


if __name__ == "__main__": unittest.main()
