# -*- coding: utf-8 -*-
"""Run: python3 -I -m unittest discover -s tests -v   (from the site root)"""
import json, pathlib, re, subprocess, sys, unittest, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
NX = pathlib.Path("/home/user/repos/Nexus-.github.io")
PAGES = [p for p in ROOT.rglob("index.html")]
TEXTS = [*PAGES, ROOT / "404.html", *ROOT.glob("assets/**/*.css"), *ROOT.glob("assets/**/*.js"), *ROOT.glob("assets/**/*.svg"),
         ROOT / "data/research.json", *ROOT.glob("tools/*.py")]
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
        self.assertEqual(en, ko); self.assertEqual(len(en), 10)

    def test_no_forbidden_strings(self):
        if not _private_terms(): print("WARNING: private forbidden-term list not found; only generic terms checked", file=sys.stderr)
        for p in TEXTS:
            t = p.read_text(encoding="utf-8")
            for w in FORBIDDEN:
                self.assertNotIn(w.lower(), t.lower(), f"{w!r} in {p}")

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
                for d in (2, 3, 4): allowed.add(f"{o:.{d}f}")
                allowed.add(f"{o*100:.1f}"); allowed.add(f"{o*100:.0f}")
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

if __name__ == "__main__": unittest.main()
