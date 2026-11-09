# -*- coding: utf-8 -*-
"""Loading intro rebuilt as SVG+CSS from the reference GIF (9 frames x 0.5 s):
sunrise -> a big thin ring is drawn -> it collapses into a tilted orbit while the metallic 'A' appears
-> a bright arc + star -> AEVORIN wordmark -> tagline -> milky way, while the planet sinks.
Coordinates are in 'crop units' = 3x the GIF pixels, measured on the GIF's last frame."""
import math

# A (wide prism legs), measured on the last GIF frame
APEX = (310, 125)
ORB = dict(cx=318, cy=326, rx=272, ry=122, rot=-22)            # faint outer loop of the orbit
RING = dict(cx=315, cy=360, r=345)                              # the big circle seen in frames 1-2
STAR = (523, 215)
FRONT = "M70 454 C 190 410, 330 340, 523 215"                  # the bright arc that crosses the A
TOP = "M523 215 C 470 188, 405 186, 340 205 C 250 232, 150 335, 70 454"   # faint back arc (behind the A)

W_, H_ = 60, 72                                                 # wordmark glyph box
GAP = 67
def glyphs():
    w, h = W_, H_
    return {
      "A": f"M0 {h} L{w/2} 0 L{w} {h}",                         # the brand's A has no crossbar
      "E": f"M{w} 0 H0 V{h} H{w} M0 {h/2} H{w*.86}",
      "V": f"M0 0 L{w/2} {h} L{w} 0",
      "O": f"M-3 {h/2} a{w/2+3} {h/2} 0 1 0 {w+6} 0 a{w/2+3} {h/2} 0 1 0 {-(w+6)} 0",
      "R": f"M0 {h} V0 H{w*.6} C{w+3} 0 {w+3} {h*.52} {w*.6} {h*.52} H0 M{w*.5} {h*.52} L{w} {h}",
      "I": f"M{w/2} 0 V{h}",
      "N": f"M0 {h} V0 L{w} {h} V0",
    }
def wordmark():
    g = glyphs(); word = "AEVORIN"; total = len(word) * W_ + (len(word) - 1) * GAP
    x0 = 318 - total / 2; out = []
    for i, ch in enumerate(word):
        x = x0 + i * (W_ + GAP)
        out.append(f'<path class="wl" style="--i:{i}" pathLength="1" transform="translate({x:.1f} 585)" d="{g[ch]}"/>')
    return "".join(out)

def intro_html(lang):
    skip = "Skip" if lang == "en" else "건너뛰기"
    sx, sy = STAR
    o, r = ORB, RING
    return f'''<div id="intro" class="intro" aria-hidden="true">
<div class="in-sky"></div><div class="in-milky"></div><div class="in-photo"></div><div class="in-glow"></div>
<svg class="in-logo" viewBox="-110 80 860 700" preserveAspectRatio="xMidYMid meet" focusable="false">
<defs>
<linearGradient id="iL" x1="0" y1="0" x2="1" y2=".9"><stop offset="0" stop-color="#ffffff"/><stop offset=".35" stop-color="#dfe5f2"/><stop offset=".75" stop-color="#9aa6c0"/><stop offset="1" stop-color="#6c7896"/></linearGradient>
<linearGradient id="iR" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#e9eef9"/><stop offset=".45" stop-color="#b4bfd8"/><stop offset="1" stop-color="#7c88a6"/></linearGradient>
<linearGradient id="iG2" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8f9bb8" stop-opacity=".55"/><stop offset="1" stop-color="#4a5675" stop-opacity=".0"/></linearGradient>
<radialGradient id="iS"><stop offset="0" stop-color="#fff"/><stop offset=".16" stop-color="#d6e4ff" stop-opacity=".95"/><stop offset=".5" stop-color="#6f9bff" stop-opacity=".35"/><stop offset="1" stop-color="#4f7bff" stop-opacity="0"/></radialGradient>
<filter id="iF" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
</defs>
<g transform="translate({r['cx']} {r['cy']})"><g><ellipse class="in-loop" cx="0" cy="0" rx="{r['r']}" ry="{r['r']}" pathLength="1" filter="url(#iF)">
<animate attributeName="rx" from="{r['r']}" to="{o['rx']}" begin="1.7s" dur="1s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/>
<animate attributeName="ry" from="{r['r']}" to="{o['ry']}" begin="1.7s" dur="1s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/>
<animateTransform attributeName="transform" type="rotate" from="0" to="{o['rot']}" begin="1.7s" dur="1s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/>
</ellipse></g>
<animateTransform attributeName="transform" type="translate" from="{r['cx']} {r['cy']}" to="{o['cx']} {o['cy']}" begin="1.7s" dur="1s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".6 0 .2 1"/></g>
<g class="in-flares"><circle cx="{r['cx']-r['r']}" cy="{r['cy']}" r="4"/><circle cx="{r['cx']+r['r']*.74}" cy="{r['cy']-r['r']*.67}" r="5"/><circle cx="{r['cx']-r['r']*.52}" cy="{r['cy']+r['r']*.85}" r="4"/></g>
<path class="in-back" d="{TOP}" pathLength="1"/>
<g class="in-mark">
<polygon points="105,487 215,448 240,372 150,432" fill="url(#iG2)"/>
<polygon points="310,125 140,425 240,345 336,160" fill="url(#iL)"/>
<polygon points="310,125 140,425 160,428 318,142" fill="#fff" opacity=".96"/>
<polygon points="240,345 140,425 205,402" fill="#56628a" opacity=".6"/>
<polygon points="338,172 246,342 402,298" fill="#070d20" opacity=".5"/>
<polygon points="310,125 516,487 428,470 338,165" fill="url(#iR)"/>
<polygon points="310,125 516,487 500,484 312,140" fill="#fff" opacity=".55"/>
<polygon points="338,165 428,470 398,462 336,185" fill="#fff" opacity=".3"/>
<polyline points="310,125 140,425" stroke="#fff" stroke-width="2" fill="none"/>
<polyline points="310,125 516,487" stroke="#eef3ff" stroke-width="1.8" fill="none" opacity=".8"/>
</g>
<path class="in-front" d="{FRONT}" pathLength="1" filter="url(#iF)"/>
<g class="in-star" transform="translate({sx} {sy})"><circle r="104" fill="url(#iS)" opacity=".6"/><circle r="70" fill="url(#iS)"/><circle r="34" fill="url(#iS)"/><path d="M-120 0H120M0 -80V80" stroke="#d6e4ff" stroke-width="1" opacity=".75"/><path d="M-60 24L60 -24" stroke="#bcd0ff" stroke-width=".8" opacity=".5"/><circle r="7" fill="#fff"/></g>
<g class="in-word" fill="none" stroke="#dfe6f4" stroke-width="4.6">{wordmark()}</g>
<text class="in-tag" x="318" y="735" text-anchor="middle">Beyond What Exists.</text>
</svg>
<button class="in-skip" type="button">{skip}</button>
</div>'''
