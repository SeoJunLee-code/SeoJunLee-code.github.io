# -*- coding: utf-8 -*-
"""Build the AEVORIN static site (EN at root, KO under /ko/).
Run: python -I tools/build.py --no-fonts
(Without --no-fonts the build re-subsets the web fonts from tools/fontsrc/*.ttf; if those files are missing,
assets/css/fonts.css would be overwritten with an empty file. Re-subset only with the source TTFs present,
and update tools/font_chars.txt together with the fonts.)"""
import html, json, os, pathlib, random, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from content import build as build_content, BADGES  # noqa: E402
from intro import intro_html  # noqa: E402

D = json.load(open(ROOT / "data/research.json", encoding="utf-8"))
LANGS = ("en", "ko")
SITE = "https://seojunlee-code.github.io"
RIDS = ("context-compaction", "algorithm-innovation", "ai-responsibility", "ai-forgetting-review", "ai-creativity", "kore", "h1", "paper5", "llm-internal-computing", "world-model")
PAGES = ["", "research/", "projects/", "about/", "contact/"] + [f"research/{i}/" for i in RIDS]
# Home cards: the strongest results first (Mixed, Mixed, Refuted, Partial). The other badge kinds reach the home page
# through the status band above the cards; every study is listed on /research/.
HOME_IDS = ("context-compaction", "ai-forgetting-review", "h1", "llm-internal-computing")
# Card band illustrations (assets/img/cards/, made by tools/art.py): file and the part of its viewBox to show, so each
# drawing sits centred in the band without per-card CSS. h1.svg was drawn shifted right for the old layout, hence its crop.
CARD_ART = {"context-compaction": ("compaction.svg", (0, 30, 320, 140)), "ai-forgetting-review": ("forgetting.svg", (0, 22, 320, 156)),
            "h1": ("h1.svg", (95, 0, 320, 200)), "llm-internal-computing": ("llm.svg", (0, 0, 320, 220))}
STATUS_ORDER = ("mixed", "refuted", "partial", "exploratory", "progress", "prototype")
REPO = {"llm-internal-computing": "https://github.com/SeoJunLee-code/llm-internal-computing"}  # KORE repo link intentionally omitted
# Links are switched on only after the repository is verified public (see tools/public_repos.json).
PUBLIC = json.load(open(ROOT / "tools/public_repos.json")) if (ROOT / "tools/public_repos.json").exists() else {}
PILLS = {"en": ["AI-assisted implementation", "No independent review"], "ko": ["AI 보조 구현", "독립 검토 없음"]}
def pills(lang): return "".join(f'<span class="pill">{x}</span>' for x in PILLS[lang])
GITHUB = "https://github.com/SeoJunLee-code"
OG_IMAGE = ROOT / "assets/img/og.png"

MARK = ('<svg class="mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false">'
        '<path class="mk m1" d="M10 56 L32 8 L54 56"/><path class="mk m2" d="M19 41 H45"/>'
        '<path class="mk m3" d="M5 56 H17 M47 56 H59"/><circle class="star" cx="32" cy="7" r="2.2"/></svg>')

# Same condition as assets/js/site.js: once per device/browser (localStorage, sessionStorage as fallback),
# ?intro forces it, ?nointro and prefers-reduced-motion skip it.
INTRO_HEAD = ("<script>try{var q=location.search,s=null;try{s=localStorage.getItem('aev_intro')}catch(e){try{s=sessionStorage.getItem('aev_intro')}catch(e2){}}"
              "if(/[?&]intro\\b/.test(q)||(!s&&!/[?&]nointro\\b/.test(q)&&!matchMedia('(prefers-reduced-motion: reduce)').matches))document.documentElement.classList.add('intro-on')}catch(e){}</script>\n")
ICON_GH = '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true"><path fill="currentColor" d="M12 .5a11.5 11.5 0 0 0-3.64 22.41c.58.1.79-.25.79-.56v-2c-3.2.7-3.87-1.37-3.87-1.37-.52-1.33-1.28-1.69-1.28-1.69-1.05-.72.08-.7.08-.7 1.15.08 1.76 1.19 1.76 1.19 1.03 1.76 2.7 1.25 3.36.96.1-.75.4-1.25.73-1.54-2.55-.29-5.24-1.28-5.24-5.68 0-1.25.45-2.28 1.19-3.08-.12-.29-.52-1.46.11-3.04 0 0 .97-.31 3.17 1.18a11 11 0 0 1 5.77 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.58.23 2.75.11 3.04.74.8 1.19 1.83 1.19 3.08 0 4.41-2.69 5.38-5.25 5.67.41.36.78 1.06.78 2.14v3.17c0 .31.21.67.8.56A11.5 11.5 0 0 0 12 .5Z"/></svg>'
ICON_MAIL = '<svg viewBox="0 0 24 24" width="17" height="17" aria-hidden="true"><path fill="none" stroke="currentColor" stroke-width="1.6" d="M3 6h18v12H3zM3 7l9 7 9-7"/></svg>'
ORBIT = '''<svg class="orbit" viewBox="0 0 1672 540" preserveAspectRatio="xMidYMin slice" aria-hidden="true" focusable="false">
<defs><linearGradient id="og" x1="0" x2="1"><stop offset="0" stop-color="#9db4ff" stop-opacity="0"/><stop offset=".3" stop-color="#b9c9ff" stop-opacity=".5"/><stop offset=".7" stop-color="#cfdcff" stop-opacity=".6"/><stop offset="1" stop-color="#9db4ff" stop-opacity=".1"/></linearGradient>
<radialGradient id="fl"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#cfe0ff" stop-opacity=".8"/><stop offset="1" stop-color="#6f95ff" stop-opacity="0"/></radialGradient></defs>
<path id="orbitpath" d="M 170 275 C 400 130, 700 92, 835 92 C 1080 92, 1330 170, 1385 235 C 1440 300, 1400 380, 1230 447" fill="none" stroke="url(#og)" stroke-width="1.8"/>
<g class="flare" transform="translate(835 92)"><circle r="26" fill="url(#fl)" opacity=".85"/><path d="M-72 0H72M0 -46V46" stroke="#dfe8ff" stroke-width=".9" opacity=".7"/><circle r="2.8" fill="#fff"/></g>
<g class="tw2" transform="translate(1383 235)"><circle r="14" fill="url(#fl)" opacity=".7"/><circle r="2.6" fill="#fff"/></g>
<circle r="3" fill="#dfe8ff"><animateMotion dur="22s" repeatCount="indefinite" rotate="auto"><mpath href="#orbitpath"/></animateMotion></circle></svg>'''
LIMB = ('<svg class="limb" viewBox="0 0 1672 540" preserveAspectRatio="none" aria-hidden="true" focusable="false"><defs><linearGradient id="lg" x1="0" x2="1"><stop offset="0" stop-color="#7fa0ff" stop-opacity=".0"/><stop offset=".25" stop-color="#a9c3ff" stop-opacity=".55"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset=".75" stop-color="#a9c3ff" stop-opacity=".55"/><stop offset="1" stop-color="#7fa0ff" stop-opacity="0"/></linearGradient></defs>'
        '<path d="M-40 532 Q836 312 1712 532" fill="none" stroke="url(#lg)" stroke-width="7" opacity=".35" vector-effect="non-scaling-stroke"/><path d="M-40 532 Q836 312 1712 532" fill="none" stroke="url(#lg)" stroke-width="1.6" vector-effect="non-scaling-stroke"/></svg>')

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
def url(lang, path): return f"{SITE}/{'ko/' if lang == 'ko' else ''}{path}"
def plain(s):  # tags removed, entities decoded: safe input for html.escape in attributes
    return html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
def attr(s): return html.escape(plain(s), quote=True)

def badge(lang, kind): return f'<span class="badge b-{kind}">{BADGES[lang][kind]}</span>'

def h2_text(t):  # heading text without the evidence tag, for the table of contents
    return re.sub(r"<[^>]+>", "", re.sub(r'<span class="ev[^"]*">.*?</span>', "", t)).strip()

def render_blocks(blocks):
    """Returns (html, [(id, text) for each h2])."""
    out, heads = [], []
    for b in blocks:
        t = b[0]
        if t == "h2":
            hid = f"s{len(heads) + 1}"; heads.append((hid, h2_text(b[1])))
            out.append(f'<h2 id="{hid}">{b[1]}</h2>')
        elif t == "p": out.append(f"<p>{b[1]}</p>")
        elif t == "ul": out.append("<ul>" + "".join(f"<li>{i}</li>" for i in b[1]) + "</ul>")
        elif t == "note": out.append(f'<div class="note n-{b[2]}">{b[1]}</div>')
        elif t == "table":
            head = "".join(f"<th>{x}</th>" for x in b[1]); rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in b[2])
            out.append(f'<div class="tw-scroll"><table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>')
        elif t == "kv": out.append('<dl class="kv">' + "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in b[1]) + "</dl>")
    return "\n".join(out), heads

def head_meta(lang, path, title, desc, og_type):
    other = "ko" if lang == "en" else "en"
    canon = url(lang, path)
    img = (f'<meta property="og:image" content="{SITE}/assets/img/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">'
           if OG_IMAGE.exists() else "")
    return (f'<link rel="canonical" href="{canon}">\n'
            f'<link rel="alternate" hreflang="en" href="{url("en", path)}"><link rel="alternate" hreflang="ko" href="{url("ko", path)}"><link rel="alternate" hreflang="x-default" href="{url("en", path)}">\n'
            f'<meta property="og:site_name" content="AEVORIN"><meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
            f'<meta property="og:url" content="{canon}"><meta property="og:type" content="{og_type}">'
            f'<meta property="og:locale" content="{"en_US" if lang == "en" else "ko_KR"}"><meta property="og:locale:alternate" content="{"en_US" if other == "en" else "ko_KR"}">{img}'
            f'<meta name="twitter:card" content="{"summary_large_image" if img else "summary"}">\n')

def shell(lang, path, C, title, body, hero=False, active="", desc="", og_type="website", absolute=False):
    """absolute=True (404 page): every asset and link is root-absolute, no canonical/hreflang/og, noindex."""
    A = C["aria"]
    if absolute:
        assets = "/assets"
        lk = lambda tolang, topath: "/" + ("ko/" if tolang == "ko" else "") + topath
    else:
        assets = rel(page_dir(lang, path), ROOT / "assets", trailing=False)
        lk = lambda tolang, topath: link(lang, path, tolang, topath)
    nav = "".join(f'<a href="{lk(lang, p)}"{" aria-current=\"page\"" if p == active else ""}>{l}</a>' for p, l in C["nav"])
    sw_path = "" if absolute else path
    sw = (f'<div class="lang" role="group" aria-label="{A["lang"]}">'
          f'<a{" class=\"on\" aria-current=\"true\"" if lang == "en" else ""} href="{lk("en", sw_path)}" hreflang="en" lang="en">EN</a>'
          f'<a{" class=\"on\" aria-current=\"true\"" if lang == "ko" else ""} href="{lk("ko", sw_path)}" hreflang="ko" lang="ko">KR</a></div>')
    home = lk(lang, "")
    full_title = html.escape(title if path == "" and not absolute else f"{title} · AEVORIN", quote=True)
    d = attr(desc or C["desc"])
    en_attr = ' lang="en"' if lang == "ko" else ""
    meta = ('<meta name="robots" content="noindex">\n' if absolute else head_meta(lang, path, full_title, d, og_type))
    preload = ("".join(f'<link rel="preload" as="font" type="font/woff2" crossorigin href="{assets}/fonts/{f}.woff2">' for f in ("sans-kr-400", "serif-kr-500")) + "\n"
               if lang == "ko" else "")
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title><meta name="description" content="{d}"><meta name="theme-color" content="#03060d">
{meta}<link rel="icon" href="{assets}/img/favicon.svg" type="image/svg+xml">
{preload}<link rel="stylesheet" href="{assets}/css/fonts.css"><link rel="stylesheet" href="{assets}/css/site.css">
{INTRO_HEAD if hero else ""}</head>
<body class="{"home" if hero else "inner"}">
{intro_html(lang) if hero else ""}<a class="skip" href="#main">{C["brand"]["skip"]}</a>
<header class="nav"><div class="nav-in">
<a class="logo" href="{home}" aria-label="AEVORIN">{MARK}<span class="wm">AEVORIN</span></a>
<button class="burger" aria-expanded="false" aria-controls="menu" aria-label="{A["menu"]}"><span></span><span></span></button>
<nav id="menu" class="menu" aria-label="{A["main"]}">{nav}</nav>{sw}
</div></header>
{body}
<footer class="foot"><div class="foot-in">
<a class="logo sm" href="{home}" aria-label="AEVORIN">{MARK}<span class="wm">AEVORIN</span></a>
<p class="tag"{en_attr}>{C["brand"]["footer"]}</p>
<div class="foot-links"><a href="{GITHUB}" rel="noopener">GitHub {ICON_GH}</a><a href="{lk(lang, "contact/")}">{C["nav"][4][1]} {ICON_MAIL}</a></div>
</div></footer>
<script src="{assets}/js/site.js" defer></script>
</body></html>'''

def card_art(lang, path, rid):
    """Decorative drawing for the card band: an inline SVG that crops the file with its viewBox (aria-hidden, no text)."""
    name, (x, y, w, h) = CARD_ART[rid]
    f = ROOT / "assets/img/cards" / name
    iw, ih = (int(v) for v in re.search(r'<svg[^>]* width="(\d+)" height="(\d+)"', f.read_text(encoding="utf-8")).groups())
    src = rel(page_dir(lang, path), f, trailing=False)
    return (f'<svg class="band-art" viewBox="{x} {y} {w} {h}" width="{w}" height="{h}" preserveAspectRatio="xMidYMid meet" focusable="false">'
            f'<image href="{src}" width="{iw}" height="{ih}"/></svg>')

def card(lang, path, r, C):
    href = link(lang, path, lang, f"research/{r['id']}/")
    return (f'<a class="card" data-id="{r["id"]}" href="{href}"><span class="card-band" aria-hidden="true">{card_art(lang, path, r["id"])}</span>'
            f'<div class="card-top">{badge(lang, r["badge"])}</div>'
            f'<h3>{r["title"]}</h3><p class="sub">{r["sub"]}</p><p class="one">{r["one"]}</p>'
            f'<span class="more">{C["brand"]["learn"]} <i aria-hidden="true">→</i></span></a>')

def status_band(lang, path, C):
    counts = {k: sum(1 for r in C["research"] if r["badge"] == k) for k in STATUS_ORDER}
    assert sum(counts.values()) == len(C["research"]), "a study uses a badge kind missing from STATUS_ORDER"
    chips = "".join(f'<li>{badge(lang, k)}<span class="cnt">{n}</span></li>' for k, n in counts.items() if n)
    return (f'<a class="status" href="{link(lang, path, lang, "research/")}#legend">'
            f'<span class="st-n">{C["labels"]["studies"](len(C["research"]))}</span><ul class="st-chips">{chips}</ul></a>')

def legend(lang, C):
    L = C["badge_legend"]
    assert set(L) == set(BADGES[lang]), "badge legend must define every badge kind"
    items = "".join(f'<div><dt>{badge(lang, k)}</dt><dd>{L[k]}</dd></div>' for k in STATUS_ORDER)
    # Open by default; on narrow screens the inline script folds it before first paint so the list starts on the first
    # screen (unless the visitor came for #legend). Without JavaScript it simply stays open.
    fold = ("<script>try{if(matchMedia('(max-width:560px)').matches&&location.hash!=='#legend')"
            "document.currentScript.previousElementSibling.removeAttribute('open')}catch(e){}</script>")
    return (f'<section class="wrap legend-wrap"><details class="legend-box" open><summary><h2 class="legend-h">{C["labels"]["legend"]}</h2></summary>'
            f'<dl id="legend" class="legend">{items}</dl></details>{fold}</section>')

def pager(lang, path, C, rid):
    R, L = C["research"], C["labels"]
    i = [r["id"] for r in R].index(rid)
    out = [f'<a class="pg-all" href="{link(lang, path, lang, "research/")}">← {L["all"]}</a>']
    if i > 0:
        p = R[i - 1]
        out.append(f'<a class="pg-prev" rel="prev" href="{link(lang, path, lang, f"research/{p["id"]}/")}"><span class="pg-l">← {L["prev"]}</span><span class="pg-t">{p["title"]}</span><span class="pg-s">{p["sub"]}</span></a>')
    if i < len(R) - 1:
        n = R[i + 1]
        out.append(f'<a class="pg-next" rel="next" href="{link(lang, path, lang, f"research/{n["id"]}/")}"><span class="pg-l">{L["next"]} →</span><span class="pg-t">{n["title"]}</span><span class="pg-s">{n["sub"]}</span></a>')
    return f'<nav class="pager" aria-label="{C["aria"]["pager"]}">{"".join(out)}</nav>'

def inner_head(kicker, title, lead="", narrow=False):
    return (f'<section class="phead"><div class="wrap{" narrow" if narrow else ""}"><p class="kicker">{kicker}</p><h1>{title}</h1>'
            + (f'<p class="lead">{lead}</p>' if lead else "") + "</div></section>")

def build_site():
    for lang in LANGS:
        C = build_content(lang, D); en = lang == "en"; L = C["labels"]
        by_id = {r["id"]: r for r in C["research"]}
        def study(i):
            if i not in by_id: raise KeyError(f"unknown research id: {i}")
            return by_id[i]
        en_attr = ' lang="en"' if lang == "ko" else ""
        for path in PAGES:
            pd = page_dir(lang, path); pd.mkdir(parents=True, exist_ok=True)
            desc, og_type = C["descs"].get(path, ""), "website"
            if path == "":
                cards = "".join(card(lang, path, study(i), C) for i in HOME_IDS)
                body = f'''<main id="main" tabindex="-1"><section class="hero">
<div class="hero-sky"></div><div class="hero-photo"></div><div class="hero-glow"></div>{LIMB}{ORBIT}
<div class="hero-in"><h1 class="brand">AEVORIN</h1><p class="ident"{en_attr}>{C["brand"]["identity"]}</p><span class="rule"></span>
<p class="slogan"{en_attr}>{C["brand"]["slogan_a"]}<em>{C["brand"]["slogan_b"]}</em></p><p class="support"{en_attr}>{C["brand"]["support"]}</p>
<a class="down" href="#research" aria-label="{C["aria"]["scroll"]}"><svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" focusable="false"><path d="M12 5v14M6 13l6 6 6-6" fill="none" stroke="currentColor" stroke-width="1.4"/></svg></a></div>
</section>
<section id="research" class="home-research"><div class="wrap hr-grid"><div class="hr-lead"><p class="kicker">{L["kicker"]}</p><h2>{L["research"]}</h2>{status_band(lang, path, C)}<p>{C["home_research_lead"]}</p>
<a class="btn" href="{link(lang, path, lang, "research/")}">{C["brand"]["view_all"]}</a></div><div class="cards">{cards}</div></div></section></main>'''
                html_ = shell(lang, path, C, C["title"]["home"], body, hero=True, desc=desc)
            elif path == "research/":
                items = "".join(
                    f'<a class="row" href="{link(lang, path, lang, f"research/{r["id"]}/")}"><div class="row-h"><h2>{r["title"]} <span class="sub">— {r["sub"]}</span></h2>{badge(lang, r["badge"])}</div>'
                    f'<p class="q">{r["q"]}</p><p class="one">{r["one"]}</p></a>' for r in C["research"])
                body = f'<main id="main" tabindex="-1">{inner_head(L["kicker"], L["research"], C["research_intro"])}{legend(lang, C)}<section class="wrap list">{items}</section></main>'
                html_ = shell(lang, path, C, C["title"]["research"], body, active="research/", desc=desc)
            elif path.startswith("research/"):
                rid = path.split("/")[1]; r = study(rid)
                DL = C["detail_labels"]
                repo = REPO.get(rid)
                meta = f'<div class="meta">{badge(lang, r["badge"])}{pills(lang)}' + (f'<a class="repo" href="{repo}" rel="noopener">{DL["repo"]} ↗</a>' if repo and PUBLIC.get(repo) else (f'<span class="repo off">{DL["repo"]}: {"not public yet" if en else "공개 예정"}</span>' if repo else "")) + "</div>"
                prose, heads = render_blocks(C["pages"][rid])
                toc = (f'<nav class="toc" aria-label="{L["contents"]}"><p class="toc-h">{L["contents"]}</p><ol>'
                       + "".join(f'<li><a href="#{hid}">{t}</a></li>' for hid, t in heads) + "</ol></nav>") if len(heads) >= 6 else ""
                body = (f'<main id="main" tabindex="-1"><section class="phead"><div class="wrap narrow"><a class="back" href="{link(lang, path, lang, "research/")}">← {DL["back"]}</a>'
                        f'<h1>{r["title"]}</h1><p class="subh">{r["sub"]}</p>{meta}<div class="qbox"><span>{(("What it measures" if en else "측정 대상") if rid == "world-model" else DL["question"])}</span>{r["q"]}</div>'
                        f'<div class="result"><span>{L["result"]}</span>{r["one"]}</div>{toc}</div></section>'
                        f'<article class="wrap narrow prose">{prose}{pager(lang, path, C, rid)}</article></main>')
                html_ = shell(lang, path, C, f'{r["title"]} — {r["sub"]}', body, active="research/", desc=r["one"], og_type="article")
            elif path == "projects/":
                P = C["projects"]
                items = "".join(f'<article class="proj"><h2>{i["title"]}</h2><p class="sub">{i["sub"]}</p><p>{i["body"]}</p><p class="ai">{i["ai"]}</p>'
                                f'<div class="meta">{pills(lang)}</div>' + (f'<a class="repo" href="{i["repo"]}" rel="noopener">GitHub ↗</a>' if PUBLIC.get(i["repo"]) else f'<span class="repo off">GitHub: {"not public yet" if en else "공개 예정"}</span>') + '</article>' for i in P["items"])
                body = f'<main id="main" tabindex="-1">{inner_head("PROJECTS" if en else "프로젝트", P["title"], P["intro"])}<section class="wrap list">{items}</section></main>'
                html_ = shell(lang, path, C, C["title"]["projects"], body, active="projects/", desc=desc)
            elif path == "about/":
                prose, _ = render_blocks(C["about"])
                body = f'<main id="main" tabindex="-1">{inner_head("ABOUT" if en else "소개", "About" if en else "소개", narrow=True)}<article class="wrap narrow prose">{prose}</article></main>'
                html_ = shell(lang, path, C, C["title"]["about"], body, active="about/", desc=desc)
            elif path == "contact/":
                K = C["contact"]
                body = (f'<main id="main" tabindex="-1">{inner_head("CONTACT" if en else "연락", K["title"], K["body"], narrow=True)}<section class="wrap narrow prose">'
                        f'<p><a class="btn" href="{GITHUB}" rel="noopener">{K["link_label"]} ↗</a></p></section></main>')
                html_ = shell(lang, path, C, C["title"]["contact"], body, active="contact/", desc=desc)
            (pd / "index.html").write_text(html_, encoding="utf-8")
        if en:  # one 404 page for the whole site (GitHub Pages serves /404.html), English with a Korean line
            body = (f'<main id="main" tabindex="-1"><section class="phead nf"><div class="wrap narrow"><p class="kicker">404</p><h1>{C["title"]["notfound"]}</h1>'
                    f'<p class="lead">{L["nf_body"]}</p><p class="lead" lang="ko">{L["nf_ko"]}</p>'
                    f'<p class="nf-links"><a class="btn" href="/">{L["nf_home"]}</a><a class="btn" href="/research/">{L["research"]}</a>'
                    f'<a class="btn" href="/ko/" hreflang="ko" lang="ko">{L["nf_ko_link"]}</a></p></div></section></main>')
            (ROOT / "404.html").write_text(shell(lang, "", C, C["title"]["notfound"], body, desc="Page not found on AEVORIN.", absolute=True), encoding="utf-8")
    (ROOT / ".nojekyll").write_text("", encoding="utf-8")

def write_seo():
    urls = []
    for lang in LANGS:
        for path in PAGES:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{h}" href="{url(l, path)}"/>' for h, l in (("en", "en"), ("ko", "ko"), ("x-default", "en")))
            urls.append(f"<url><loc>{url(lang, path)}</loc>{alts}</url>")
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
                                      + "\n".join(urls) + "\n</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")

def write_assets():
    (ROOT / "assets/img/stars.svg").write_text(stars_svg(), encoding="utf-8")
    (ROOT / "assets/img/favicon.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="12" fill="#050a16"/>'
        '<g fill="none" stroke="#dfe8ff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 52 L32 12 L52 52"/><path d="M20 38 H44"/></g><circle cx="32" cy="10" r="2.6" fill="#9db4ff"/></svg>', encoding="utf-8")

def subset_fonts():
    from fontTools.ttLib import TTFont
    src = pathlib.Path(os.environ.get("FONT_SRC", ROOT / "tools/fontsrc"))
    ttfs = sorted(src.glob("*.ttf"))
    if not ttfs:  # never wipe fonts.css when the source fonts are absent
        sys.exit(f"no source fonts in {src}; run with --no-fonts")
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
    write_assets(); build_site(); write_seo()
    if "--no-fonts" not in sys.argv: subset_fonts()
    n = len(list(ROOT.rglob("index.html")))
    print("built", n, "pages")
