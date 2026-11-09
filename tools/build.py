# -*- coding: utf-8 -*-
"""Build the AEVORIN static site (EN at root, KO under /ko/). Run: python3 -I tools/build.py"""
import json, os, pathlib, random, subprocess, sys, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from content import build as build_content, BADGES  # noqa: E402
from intro import intro_html  # noqa: E402

D = json.load(open(ROOT / "data/research.json", encoding="utf-8"))
LANGS = ("en", "ko")
PAGES = ["", "research/", "projects/", "about/", "contact/"] + [f"research/{i}/" for i in ("kore", "h1", "paper5", "llm-internal-computing", "world-model")]
REPO = {"llm-internal-computing": "https://github.com/SeoJunLee-code/llm-internal-computing"}  # KORE repo link intentionally omitted
# Links are switched on only after the repository is verified public (see tools/public_repos.json).
PUBLIC = json.load(open(ROOT / "tools/public_repos.json")) if (ROOT / "tools/public_repos.json").exists() else {}
PILLS = {"en": ["AI-assisted implementation", "No independent review"], "ko": ["AI 보조 구현", "독립 검토 없음"]}
def pills(lang): return "".join(f'<span class="pill">{x}</span>' for x in PILLS[lang])
GITHUB = "https://github.com/SeoJunLee-code"

MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
        '<path class="mk m1" d="M10 56 L32 8 L54 56"/><path class="mk m2" d="M19 41 H45"/>'
        '<path class="mk m3" d="M5 56 H17 M47 56 H59"/><circle class="star" cx="32" cy="7" r="2.2"/></svg>')

INTRO_HEAD = ("<script>try{var q=location.search;if(/[?&]intro\\b/.test(q)||(!sessionStorage.getItem('aev_intro')&&!/[?&]nointro\\b/.test(q)"
              "&&!matchMedia('(prefers-reduced-motion: reduce)').matches))document.documentElement.classList.add('intro-on')}catch(e){}</script>\n")
ICON_GH = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.76 2.7 1.25 3.36.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.19-3.08-.12-.29-.52-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.58.23 2.75.11 3.04.74.8 1.19 1.83 1.19 3.08 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" d="M3 6h18v12H3zM3 7l9 7 9-7"/></svg>'
ORBIT = '''<svg class="orbit" viewBox="0 0 1672 540" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false">
<defs><linearGradient id="og" x1="0" x2="1"><stop offset="0" stop-color="#9db4ff" stop-opacity="0"/><stop offset=".3" stop-color="#b9c9ff" stop-opacity=".5"/><stop offset=".7" stop-color="#cfdcff" stop-opacity=".6"/><stop offset="1" stop-color="#9db4ff" stop-opacity=".1"/></linearGradient>
<radialGradient id="fl"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#cfe0ff" stop-opacity=".8"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient></defs>
<path id="orbitpath" d="M 170 275 C 400 130, 700 92, 835 92 C 1080 92, 1330 170, 1385 235 C 1440 300, 1400 380, 1230 447" fill="none" stroke="url(#og)" stroke-width="1.8"/>
<g class="flare" transform="translate(835 92)"><circle r="26" fill="url(#fl)" opacity=".85"/><path d="M-72 0H72M0 -46V46" stroke="#dfe8ff" stroke-width=".9" opacity=".7"/><circle r="2.8" fill="#fff"/></g>
<g class="tw2" transform="translate(1383 235)"><circle r="14" fill="url(#fl)" opacity=".7"/><circle r="2.6" fill="#fff"/></g>
<circle r="3" fill="#dfe8ff"><animateMotion dur="22s" repeatCount="indefinite" rotate="auto"><mpath href="#orbitpath"/></animateMotion></circle></svg>'''

def stars_svg(seed=11, n=170):
    rnd = random.Random(seed); out = ['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMid slice">']
    for _ in range(n):
        x, y = rnd.uniform(0, 1600), rnd.uniform(0, 640 if rnd.random() < .9 else 900)
        r = rnd.choice([.5, .6, .7, .8, 1, 1.2, 1.6]); o = rnd.uniform(.25, .95)
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#dfe8ff" opacity="{o:.2f}"/>')
    out.append("</svg>"); return "".join(out)

def page_dir(lang, path): return ROOT / ("ko" if lang == "ko" else "") / path
def rel(frm: pathlib.Path, to: pathlib.Path, trailing=True):
    r = os.path.relpath(to, frm).replace(os.sep, "/")
    r = "./" if r == "." else r
    return r + ("/" if trailing and not r.endswith("/") else "")
def link(lang, path, tolang, topath):
    return rel(page_dir(lang, path), page_dir(tolang, topath))

def badge(lang, kind): return f'<span class="badge b-{kind}">{BADGES[lang][kind]}</span>'

def render_blocks(blocks):
    out = []
    for b in blocks:
        t = b[0]
        if t == "h2": out.append(f"<h2>{b[1]}</h2>")
        elif t == "p": out.append(f"<p>{b[1]}</p>")
        elif t == "ul": out.append("<ul>" + "".join(f"<li>{i}</li>" for i in b[1]) + "</ul>")
        elif t == "note": out.append(f'<div class="note n-{b[2]}">{b[1]}</div>')
        elif t == "table":
            head = "".join(f"<th>{x}</th>" for x in b[1]); rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b[2])
            out.append(f'<div class="tw-scroll"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif t == "kv": out.append('<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in b[1]) + "</dl>")
    return "\n".join(out)

def shell(lang, path, C, title, body, hero=False, active=""):
    pd = page_dir(lang, path); assets = rel(pd, ROOT / "assets", trailing=False)
    other = "ko" if lang == "en" else "en"
    nav = "".join(f'<a href="{link(lang, path, lang, p)}"{" aria-current=\"page\"" if p == active else ""}>{l}</a>' for p, l in C["nav"])
    sw = (f'<div class="lang" role="group" aria-label="Language"><a class="{"on" if lang == "en" else ""}" href="{link(lang, path, "en", path)}" hreflang="en" lang="en">EN</a>'
          f'<a class="{"on" if lang == "ko" else ""}" href="{link(lang, path, "ko", path)}" hreflang="ko" lang="ko">KR</a></div>')
    home = link(lang, path, lang, "")
    full_title = title if path == "" else f"{title} · AEVORIN"
    foot_c = link(lang, path, lang, "contact/")
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title><meta name="description" content="{C["desc"]}"><meta name="theme-color" content="#03060d">
<link rel="icon" href="{assets}/img/favicon.svg" type="image/svg+xml">
<link rel="alternate" hreflang="en" href="{link(lang, path, "en", path)}"><link rel="alternate" hreflang="ko" href="{link(lang, path, "ko", path)}">
<link rel="stylesheet" href="{assets}/css/fonts.css"><link rel="stylesheet" href="{assets}/css/site.css">
{INTRO_HEAD if hero else ""}</head>
<body class="{"home" if hero else "inner"}">
{intro_html(lang) if hero else ""}<a class="skip" href="#main">{C["brand"]["skip"]}</a>
<header class="nav"><div class="nav-in">
<a class="logo" href="{home}" aria-label="AEVORIN">{MARK}<span class="wm">AEVORIN</span></a>
<button class="burger" aria-expanded="false" aria-controls="menu" aria-label="Menu"><span></span><span></span></button>
<nav id="menu" class="menu" aria-label="Main">{nav}</nav>{sw}
</div></header>
{body}
<footer class="foot"><div class="foot-in">
<a class="logo sm" href="{home}" aria-label="AEVORIN">{MARK}<span class="wm">AEVORIN</span></a>
<p class="tag">{C["brand"]["footer"]}</p>
<div class="foot-links"><a href="{GITHUB}" rel="noopener">GitHub {ICON_GH}</a><a href="{foot_c}">{C["nav"][4][1]} {ICON_MAIL}</a></div>
</div></footer>
<script src="{assets}/js/site.js" defer></script>
</body></html>'''

ART = {"kore": "kore.svg", "h1": "h1.svg", "paper5": "paper5.svg", "llm-internal-computing": "llm.svg"}
def card(lang, path, r, with_q=False):
    href = link(lang, path, lang, f"research/{r['id']}/")
    art = rel(page_dir(lang, path), ROOT / "assets/img/cards", trailing=False) + "/" + ART[r["id"]] if r["id"] in ART else ""
    return (f'<a class="card c-{r["id"]}" href="{href}">' + (f'<img class="art" src="{art}" alt="" aria-hidden="true" loading="lazy">' if art else "") + f'<div class="card-top">{badge(lang, r["badge"])}</div>'
            f'<h3>{r["title"]}</h3><p class="sub">{r["sub"]}</p><p class="blurb">{r["blurb"]}</p>'
            f'<span class="more">{C_BRAND["learn"]} <i aria-hidden="true">→</i></span></a>')

def inner_head(kicker, title, lead=""):
    return f'<section class="phead"><div class="wrap"><p class="kicker">{kicker}</p><h1>{title}</h1>{f"<p class=lead>{lead}</p>" if lead else ""}</div></section>'

def build_site():
    global C_BRAND
    for lang in LANGS:
        C = build_content(lang, D); C_BRAND = C["brand"]; en = lang == "en"
        for path in PAGES:
            pd = page_dir(lang, path); pd.mkdir(parents=True, exist_ok=True)
            if path == "":
                cards = "".join(card(lang, path, r) for r in C["research"][:4])
                body = f'''<main id="main"><section class="hero">
<div class="hero-sky"></div><div class="hero-photo"></div><div class="hero-glow"></div><svg class="limb" viewBox="0 0 1672 540" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs><linearGradient id="lg" x1="0" x2="1"><stop offset="0" stop-color="#7fa0ff" stop-opacity=".0"/><stop offset=".25" stop-color="#a9c3ff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset=".75" stop-color="#a9c3ff" stop-opacity=".55"/><stop offset="1" stop-color="#7fa0ff" stop-opacity="0"/></linearGradient></defs><path d="M-40 532 Q836 312 1712 532" fill="none" stroke="url(#lg)" stroke-width="7" opacity=".35" vector-effect="non-scaling-stroke"/><path d="M-40 532 Q836 312 1712 532" fill="none" stroke="url(#lg)" stroke-width="1.6" vector-effect="non-scaling-stroke"/></svg>{ORBIT}
<div class="hero-in"><h1 class="brand">AEVORIN</h1><p class="ident">{C["brand"]["identity"]}</p><span class="rule"></span>
<p class="slogan">{C["brand"]["slogan_a"]}<em>{C["brand"]["slogan_b"]}</em></p><p class="support">{C["brand"]["support"]}</p>
<a class="down" href="#research" aria-label="Scroll"><svg viewBox="0 0 24 24" width="20" height="20"><path d="M12 5v14M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></a></div>
</section>
<section id="research" class="home-research"><div class="wrap hr-grid"><div class="hr-lead"><p class="kicker">{"RESEARCH" if en else "연구"}</p><h2>{"Research" if en else "연구"}</h2><p>{C["home_research_lead"]}</p>
<a class="btn" href="{link(lang, path, lang, "research/")}">{C["brand"]["view_all"]}</a></div><div class="cards">{cards}</div></div></section></main>'''
                html = shell(lang, path, C, C["title"]["home"], body, hero=True, active="")
            elif path == "research/":
                items = "".join(
                    f'<a class="row" href="{link(lang, path, lang, f"research/{r["id"]}/")}"><div class="row-h">{badge(lang, r["badge"])}<h3>{r["title"]} <span class="sub">— {r["sub"]}</span></h3></div>'
                    f'<p class="q">{r["q"]}</p><p class="one">{r["one"]}</p></a>' for r in C["research"])
                body = f'<main id="main">{inner_head("RESEARCH" if en else "연구", "Research" if en else "연구", C["research_intro"])}<section class="wrap list">{items}</section></main>'
                html = shell(lang, path, C, C["title"]["research"], body, active="research/")
            elif path.startswith("research/"):
                rid = path.split("/")[1]; r = next(x for x in C["research"] if x["id"] == rid)
                L = C["detail_labels"]
                repo = REPO.get(rid)
                meta = f'<div class="meta">{badge(lang, r["badge"])}{pills(lang)}' + (f'<a class="repo" href="{repo}" rel="noopener">{L["repo"]} ↗</a>' if repo and PUBLIC.get(repo) else (f'<span class="repo off">{L["repo"]}: {"not public yet" if en else "공개 예정"}</span>' if repo else "")) + "</div>"
                body = (f'<main id="main"><section class="phead"><div class="wrap narrow"><a class="back" href="{link(lang, path, lang, "research/")}">← {L["back"]}</a>'
                        f'<h1>{r["title"]}</h1><p class="subh">{r["sub"]}</p>{meta}<div class="qbox"><span>{(("What it measures" if en else "측정 대상") if rid == "world-model" else L["question"])}</span>{r["q"]}</div></div></section>'
                        f'<article class="wrap narrow prose">{render_blocks(C["pages"][rid])}</article></main>')
                html = shell(lang, path, C, f'{r["title"]} — {r["sub"]}', body, active="research/")
            elif path == "projects/":
                P = C["projects"]
                items = "".join(f'<article class="proj"><h3>{i["title"]}</h3><p class="sub">{i["sub"]}</p><p>{i["body"]}</p><p class="ai">{i["ai"]}</p>'
                                f'<div class="meta">{pills(lang)}</div>' + (f'<a class="repo" href="{i["repo"]}" rel="noopener">GitHub ↗</a>' if PUBLIC.get(i["repo"]) else f'<span class="repo off">GitHub: {"not public yet" if en else "공개 예정"}</span>') + '</article>' for i in P["items"])
                body = f'<main id="main">{inner_head("PROJECTS" if en else "프로젝트", P["title"], P["intro"])}<section class="wrap list">{items}</section></main>'
                html = shell(lang, path, C, P["title"], body, active="projects/")
            elif path == "about/":
                body = f'<main id="main">{inner_head("ABOUT" if en else "소개", "About" if en else "소개")}<article class="wrap narrow prose">{render_blocks(C["about"])}</article></main>'
                html = shell(lang, path, C, "About" if en else "소개", body, active="about/")
            elif path == "contact/":
                K = C["contact"]
                body = (f'<main id="main">{inner_head("CONTACT" if en else "연락", K["title"], K["body"])}<section class="wrap narrow prose">'
                        f'<p><a class="btn" href="{GITHUB}" rel="noopener">{K["link_label"]} ↗</a></p></section></main>')
                html = shell(lang, path, C, K["title"], body, active="contact/")
            (pd / "index.html").write_text(html, encoding="utf-8")
    (ROOT / "404.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Not found · AEVORIN</title>'
        '<link rel="stylesheet" href="/assets/css/fonts.css"><link rel="stylesheet" href="/assets/css/site.css"></head><body class="inner"><main class="wrap narrow prose" style="padding-top:20vh">'
        '<h1>404</h1><p>This page does not exist. <a href="/">AEVORIN</a></p></main></body></html>', encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

def write_assets():
    (ROOT / "assets/img/stars.svg").write_text(stars_svg(), encoding="utf-8")
    (ROOT / "assets/img/favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#050a16"/>'
        '<g fill="none" stroke="#dfe8ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 52 L32 12 L52 52"/><path d="M20 38 H44"/></g><circle cx="32" cy="10" r="2.6" fill="#9db4ff"/></svg>', encoding="utf-8")

def subset_fonts():
    from fontTools.ttLib import TTFont
    src = pathlib.Path(os.environ.get("FONT_SRC", ROOT / "tools/fontsrc"))
    chars = set(map(chr, range(0x20, 0x7F))) | set("‘’“”–—·…→←↗×≥≤±§ε≈")
    for f in ROOT.rglob("*.html"): chars |= set(f.read_text(encoding="utf-8"))
    chars |= set(json.dumps(D, ensure_ascii=False))
    txt = src.parent / "chars.txt"; txt.write_text("".join(sorted(chars)), encoding="utf-8")
    fonts = {"AEV Serif": ("CormorantGaramond", "serif"), "AEV Sans": ("Inter", "sans"), "AEV Serif KR": ("NotoSerifKR", "serif-kr"), "AEV Sans KR": ("NotoSansKR", "sans-kr")}
    css = []
    for fam, (prefix, key) in fonts.items():
        for p in sorted(src.glob(prefix + "_*.ttf")):
            w = TTFont(p)["OS/2"].usWeightClass
            out = ROOT / f"assets/fonts/{key}-{w}.woff2"
            subprocess.run(["pyftsubset", str(p), f"--text-file={txt}", "--flavor=woff2", f"--output-file={out}", "--layout-features=*", "--no-hinting"], check=True)
            css.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:swap;src:url("../fonts/{out.name}") format("woff2")}}')
    (ROOT / "assets/css/fonts.css").write_text("\n".join(css) + "\n", encoding="utf-8")

if __name__ == "__main__":
    write_assets(); build_site()
    if "--no-fonts" not in sys.argv: subset_fonts()
    n = len(list(ROOT.rglob("index.html")))
    print("built", n, "pages")
