#!/usr/bin/env python3
"""Generator aset SVG animasi untuk profile README (alternatif gratis GitSkins).

Semua output adalah file SVG statis dengan animasi CSS + SMIL, tanpa JavaScript
dan tanpa resource eksternal, jadi tetap jalan waktu GitHub merendernya lewat
<img> (secure animated mode) dan waktu diproksikan camo.

Pakai:  python3 tools/gen_svg.py
Output: assets/*.svg
"""

import os
import random
from xml.sax.saxutils import escape

random.seed(7)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")

GREEN = "#16F74F"
GREEN_SOFT = "#8CE6A5"
GREEN_DIM = "#0B7A2C"
CYAN = "#22E7F7"
RED = "#F7264F"
BG = "#000000"
CARD = "#040805"

# stack font monospace yang aman di semua OS (Fira Code kalau user punya)
MONO = ("'Fira Code','JetBrains Mono',ui-monospace,SFMono-Regular,Menlo,"
        "Consolas,'DejaVu Sans Mono',monospace")

RAIN_CHARS = "01ABCDEF#$%&*+=<>[]{}/\\|_-~^:;?!"


def fmt(x):
    """Angka ringkas biar file SVG tidak gemuk."""
    return ("%.3f" % x).rstrip("0").rstrip(".") or "0"


def kt_fmt(x):
    """keyTimes butuh presisi tinggi: kalau dibulatkan kasar, step per-karakter
    bisa jadi duplikat -> keyTimes tidak menaik -> animasi diabaikan browser."""
    return ("%.6f" % x).rstrip("0").rstrip(".") or "0"


def defs_common():
    """Filter glow + pola scanline yang dipakai beberapa aset."""
    return f"""
  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="glowHard" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.2" fill="#0affff" opacity="0.045"/>
    </pattern>
  </defs>"""


# --------------------------------------------------------------------------
# 1. HERO — jendela terminal dengan efek mengetik + hujan matrix
# --------------------------------------------------------------------------

def build_hero():
    W = 900
    FS = 17.0
    CW = FS * 0.6            # lebar karakter monospace (advance 0.6em)
    LH = 28.0
    PAD = 30.0
    BAR = 38.0

    lines = [
        ("cmd", "$ whoami", 0.055),
        ("out", "  atok tajuddin - systems engineer / red teamer", 0.016),
        ("cmd", "$ cat /etc/focus", 0.055),
        ("out", "  low-level . offensive security . backend . networking", 0.016),
        ("cmd", "$ uptime --since", 0.055),
        ("out", "  building from the ground up, one commit at a time", 0.016),
        ("cmd", "$ ", 0.055),
    ]

    body_top = BAR + 34.0
    H = body_top + LH * len(lines) + 26.0

    # ---- susun timeline ----
    t = 0.55
    per_line = []             # (start, speed, teks)
    cursor = [(0.0, PAD, body_top)]
    for i, (kind, text, speed) in enumerate(lines):
        y = body_top + i * LH
        per_line.append((t, speed, text, kind, y))
        for n in range(len(text) + 1):
            cursor.append((t + n * speed, PAD + n * CW, y))
        t += len(text) * speed
        t += 0.45 if kind == "cmd" else 0.7
    T = round(t + 2.6, 2)     # sisa waktu buat kursor berkedip sebelum loop

    def kt(v):
        return kt_fmt(min(max(v / T, 0.0), 1.0))

    # Reveal per-karakter pakai fill-opacity. Dulu pakai <clipPath> yang lebarnya
    # dianimasikan, tapi Chrome tidak selalu me-repaint elemen yang direferensikan
    # saat isi clipPath berubah -> baris bisa "hilang". Per-karakter jauh lebih aman,
    # sekaligus mengunci grid monospace lewat x eksplisit tiap karakter.
    body = []
    for i, (start, speed, text, kind, y) in enumerate(per_line):
        fill = GREEN if kind == "cmd" else GREEN_SOFT
        weight = "600" if kind == "cmd" else "400"
        spans = []
        for n, ch in enumerate(text):
            if ch == " ":
                continue
            k = kt(start + (n + 1) * speed)
            spans.append(
                f'<tspan x="{fmt(PAD + n * CW)}" fill-opacity="0">{escape(ch)}'
                f'<animate attributeName="fill-opacity" calcMode="discrete" dur="{T}s" '
                f'repeatCount="indefinite" keyTimes="0;{k};1" values="0;1;1"/></tspan>'
            )
        body.append(
            f'    <text y="{fmt(y)}" fill="{fill}" font-weight="{weight}">'
            + "".join(spans) + "</text>"
        )

    ctimes, cxs, cys = ["0"], [fmt(PAD)], [fmt(body_top)]
    last = 0.0
    for (ct, cx, cy) in cursor[1:]:
        frac = min(max(ct / T, 0.0), 1.0)
        if frac <= last + 1e-6 or frac >= 1.0:
            continue
        last = frac
        key = kt_fmt(frac)
        ctimes.append(key)
        cxs.append(fmt(cx))
        cys.append(fmt(cy))
    ctimes.append("1")
    cxs.append(cxs[-1])
    cys.append(cys[-1])

    # ---- hujan matrix di latar ----
    rain = []
    for col in range(int(W // 26)):
        x = 13 + col * 26
        depth = random.random()
        dur = round(7 + depth * 11, 2)
        chars = "".join(random.choice(RAIN_CHARS) for _ in range(16))
        tspans = "".join(
            f'<tspan x="{x}" dy="{0 if k == 0 else 22}">{escape(c)}</tspan>'
            for k, c in enumerate(chars)
        )
        rain.append(
            f'      <g opacity="{fmt(0.05 + depth * 0.07)}">'
            f'<text x="{x}" y="0" font-size="15" fill="{GREEN}">{tspans}</text>'
            f'<animateTransform attributeName="transform" type="translate" '
            f'dur="{dur}s" repeatCount="indefinite" begin="-{round(random.random() * dur, 2)}s" '
            f'values="0,-360;0,{fmt(H + 40)}"/></g>'
        )

    dots = "".join(
        f'<circle cx="{22 + k * 18}" cy="{fmt(BAR / 2)}" r="5" fill="{c}" opacity="0.85"/>'
        for k, c in enumerate(["#F7264F", "#F7C22E", GREEN])
    )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {fmt(H)}" width="{W}" height="{fmt(H)}" font-family="{MONO}" font-size="{fmt(FS)}" role="img" aria-label="Terminal animasi: whoami, focus, uptime">
  <title>atok@its - terminal</title>
  <defs>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="1.4" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.2" fill="#0affff" opacity="0.05"/>
    </pattern>
    <linearGradient id="sweep" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="0.5" stop-color="{GREEN}" stop-opacity="0.10"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="rainFade" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#fff" stop-opacity="0.15"/>
      <stop offset="0.55" stop-color="#fff" stop-opacity="0.9"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <mask id="rainMask"><rect width="{W}" height="{fmt(H)}" fill="url(#rainFade)"/></mask>
    <clipPath id="card"><rect x="1" y="1" width="{W - 2}" height="{fmt(H - 2)}" rx="14"/></clipPath>
  </defs>
  <style>
    .blink {{ animation: bl 1.05s steps(1) infinite; }}
    @keyframes bl {{ 0%,55% {{ opacity: 1 }} 56%,100% {{ opacity: 0 }} }}
  </style>

  <rect width="{W}" height="{fmt(H)}" rx="14" fill="{CARD}"/>
  <g clip-path="url(#card)">
    <g mask="url(#rainMask)">
{chr(10).join(rain)}
    </g>
    <rect width="{W}" height="{fmt(H)}" fill="url(#scan)"/>
    <rect x="0" y="0" width="{W}" height="90" fill="url(#sweep)">
      <animate attributeName="y" dur="6s" repeatCount="indefinite" values="-90;{fmt(H)}"/>
    </rect>
    <rect x="0" y="0" width="{W}" height="{fmt(BAR)}" fill="#0A140D"/>
    <line x1="0" y1="{fmt(BAR)}" x2="{W}" y2="{fmt(BAR)}" stroke="{GREEN}" stroke-opacity="0.25"/>
    {dots}
    <text x="{fmt(W / 2)}" y="{fmt(BAR / 2 + 5)}" text-anchor="middle" font-size="13" fill="{GREEN}" opacity="0.55">atok@its - zsh - 96x24</text>

    <g filter="url(#glow)">
{chr(10).join(body)}
    </g>
    <g class="blink">
      <rect y="0" x="0" width="{fmt(CW)}" height="{fmt(FS * 1.15)}" fill="{GREEN}" opacity="0.9">
        <animate attributeName="x" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{";".join(ctimes)}" values="{";".join(cxs)}"/>
        <animate attributeName="y" calcMode="discrete" dur="{T}s" repeatCount="indefinite" keyTimes="{";".join(ctimes)}" values="{";".join(fmt(float(v) - FS + 2) for v in cys)}"/>
      </rect>
    </g>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{fmt(H - 1)}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.35"/>
</svg>
"""


# --------------------------------------------------------------------------
# 2. GLITCH — nama besar dengan RGB split + slice glitch
# --------------------------------------------------------------------------

def build_glitch(name="ATOK TAJUDDIN", tagline="systems engineer  ::  red teamer  ::  builder"):
    W, H = 900, 170
    FS = 62
    cy = 84
    slices = []
    for i in range(5):
        y = 40 + i * 20
        dx = random.choice([-16, -10, 12, 18, -22])
        delay = round(random.uniform(0, 3.4), 2)
        slices.append(
            f'    <g clip-path="url(#sl{i})" class="gl" style="animation-delay:{delay}s">'
            f'<use href="#nm" transform="translate({dx},0)" fill="{GREEN}"/></g>'
        )
        slices.append(f'@@CLIP{i}@@{y}')
    clip_defs = "".join(
        f'<clipPath id="sl{i}"><rect x="0" y="{40 + i * 20}" width="{W}" height="12"/></clipPath>'
        for i in range(5)
    )
    slice_g = "\n".join(s for s in slices if not s.startswith("@@CLIP"))

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" role="img" aria-label="{escape(name)} - {escape(tagline)}">
  <title>{escape(name)}</title>
  <defs>
    <filter id="g2" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <pattern id="scan2" width="4" height="4" patternUnits="userSpaceOnUse">
      <rect width="4" height="1.4" fill="#0affff" opacity="0.05"/>
    </pattern>
    {clip_defs}
    <text id="nm" x="{W // 2}" y="{cy}" text-anchor="middle" font-size="{FS}" font-weight="700" letter-spacing="6">{escape(name)}</text>
  </defs>
  <style>
    .chroma {{ animation: ch 4.6s steps(1) infinite; }}
    .chroma2 {{ animation: ch2 4.6s steps(1) infinite; }}
    .gl {{ opacity: 0; animation: sl 4.6s steps(1) infinite; }}
    .base {{ animation: flick 4.6s steps(1) infinite; }}
    @keyframes ch {{ 0%,86%,100% {{ transform: translate(0,0); opacity:.0 }}
      87% {{ transform: translate(-5px,2px); opacity:.85 }}
      90% {{ transform: translate(4px,-2px); opacity:.85 }}
      93% {{ transform: translate(-2px,1px); opacity:.5 }} }}
    @keyframes ch2 {{ 0%,86%,100% {{ transform: translate(0,0); opacity:.0 }}
      88% {{ transform: translate(5px,-2px); opacity:.8 }}
      91% {{ transform: translate(-4px,2px); opacity:.8 }}
      94% {{ transform: translate(2px,0); opacity:.45 }} }}
    @keyframes sl {{ 0%,85%,100% {{ opacity: 0 }} 87%,92% {{ opacity: .95 }} 93% {{ opacity: 0 }} }}
    @keyframes flick {{ 0%,88%,100% {{ opacity: 1 }} 89% {{ opacity: .55 }} 90% {{ opacity: 1 }} 91% {{ opacity: .7 }} }}
    .cur {{ animation: bl 1.05s steps(1) infinite; }}
    @keyframes bl {{ 0%,55% {{ opacity: 1 }} 56%,100% {{ opacity: 0 }} }}
  </style>

  <rect width="{W}" height="{H}" rx="14" fill="{CARD}"/>
  <g filter="url(#g2)">
    <use href="#nm" class="chroma" fill="{CYAN}"/>
    <use href="#nm" class="chroma2" fill="{RED}"/>
    <use href="#nm" class="base" fill="{GREEN}"/>
  </g>
{slice_g}
  <g opacity="0.75">
    <text x="{W // 2}" y="{cy + 40}" text-anchor="middle" font-size="15" fill="{GREEN_SOFT}" letter-spacing="2">{escape(tagline)}</text>
  </g>
  <g transform="translate({W // 2 - 150},{cy + 62})">
    <line x1="0" y1="0" x2="300" y2="0" stroke="{GREEN}" stroke-opacity="0.3"/>
    <rect x="0" y="-2" width="70" height="4" fill="{GREEN}">
      <animate attributeName="x" dur="3.4s" repeatCount="indefinite" values="0;230;0" keyTimes="0;0.5;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/>
    </rect>
  </g>
  <rect width="{W}" height="{H}" rx="14" fill="url(#scan2)"/>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.35"/>
</svg>
"""


# --------------------------------------------------------------------------
# 3. MARQUEE — ticker tech stack yang jalan terus
# --------------------------------------------------------------------------

def build_marquee(items=None):
    items = items or ["C", "C++", "Rust", "Go", "Python", "Bash", "TypeScript", "React",
                      "Node.js", "PostgreSQL", "Redis", "Docker", "Linux", "Nmap",
                      "Burp Suite", "Ghidra", "Metasploit", "Wireshark", "Assembly", "Git"]
    W, H = 900, 62
    FS = 14.0
    CW = FS * 0.6
    PADX = 15.0
    GAP = 11.0

    def row(prefix):
        out, x = [], 0.0
        for it in items:
            w = len(it) * CW + PADX * 2
            out.append(
                f'      <g transform="translate({fmt(x)},0)">'
                f'<rect width="{fmt(w)}" height="30" rx="15" fill="#0A160E" stroke="{GREEN}" stroke-opacity="0.4"/>'
                f'<circle cx="{fmt(PADX * 0.55)}" cy="15" r="0" fill="{GREEN}"/>'
                f'<text x="{fmt(w / 2)}" y="20" text-anchor="middle" font-size="{fmt(FS)}" fill="{GREEN}" '
                f'textLength="{fmt(len(it) * CW)}" lengthAdjust="spacingAndGlyphs">{escape(it)}</text></g>'
            )
            x += w + GAP
        return "\n".join(out), x

    inner, RW = row("a")
    dur = round(RW / 46.0, 2)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" role="img" aria-label="Tech stack: {escape(', '.join(items))}">
  <title>arsenal</title>
  <defs>
    <linearGradient id="edge" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
      <stop offset="0" stop-color="#000"/><stop offset="0.07" stop-color="#fff"/>
      <stop offset="0.93" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
    </linearGradient>
    <mask id="edgeMask" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{H}">
      <rect width="{W}" height="{H}" fill="url(#edge)"/></mask>
  </defs>
  <rect width="{W}" height="{H}" rx="12" fill="{CARD}"/>
  <g mask="url(#edgeMask)">
    <g transform="translate(0,16)">
      <animateTransform attributeName="transform" type="translate" dur="{dur}s" repeatCount="indefinite" values="0,16;{fmt(-RW)},16"/>
      <g>
{inner}
      </g>
      <g transform="translate({fmt(RW)},0)">
{inner}
      </g>
    </g>
  </g>
  <rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="12" fill="none" stroke="{GREEN}" stroke-opacity="0.3"/>
</svg>
"""


# --------------------------------------------------------------------------
# 4. DIVIDER — garis dengan paket data yang lewat
# --------------------------------------------------------------------------

def build_divider():
    W, H = 900, 18
    ticks = "".join(
        f'<rect x="{x}" y="7" width="2" height="4" fill="{GREEN}" opacity="0.25"/>'
        for x in range(0, W, 18)
    )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="pembatas animasi">
  <defs>
    <linearGradient id="pk" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0"/>
      <stop offset="0.55" stop-color="{GREEN}" stop-opacity="1"/>
      <stop offset="1" stop-color="#FFFFFF" stop-opacity="0.9"/>
    </linearGradient>
  </defs>
  <line x1="0" y1="9" x2="{W}" y2="9" stroke="{GREEN}" stroke-opacity="0.22"/>
  {ticks}
  <rect y="7.5" width="140" height="3" fill="url(#pk)" rx="1.5">
    <animate attributeName="x" dur="3.6s" repeatCount="indefinite" values="-140;{W}"/>
  </rect>
  <rect y="7.5" width="90" height="3" fill="url(#pk)" rx="1.5" opacity="0.5">
    <animate attributeName="x" dur="3.6s" begin="-1.8s" repeatCount="indefinite" values="-90;{W}"/>
  </rect>
</svg>
"""


# --------------------------------------------------------------------------
# 5. RADAR — sapuan radar dengan blip (buat seksi security)
# --------------------------------------------------------------------------

def build_radar():
    S = 320
    c = S / 2
    R = c - 18
    rings = "".join(
        f'<circle cx="{fmt(c)}" cy="{fmt(c)}" r="{fmt(R * f)}" fill="none" stroke="{GREEN}" stroke-opacity="0.22"/>'
        for f in (0.25, 0.5, 0.75, 1.0)
    )
    cross = (f'<line x1="{fmt(c - R)}" y1="{fmt(c)}" x2="{fmt(c + R)}" y2="{fmt(c)}" stroke="{GREEN}" stroke-opacity="0.18"/>'
             f'<line x1="{fmt(c)}" y1="{fmt(c - R)}" x2="{fmt(c)}" y2="{fmt(c + R)}" stroke="{GREEN}" stroke-opacity="0.18"/>')

    blips = []
    labels = ["recon", "web", "binary", "network", "hardware", "backend"]
    import math
    for i, lbl in enumerate(labels):
        # satu blip per sektor 60 derajat + sedikit jitter
        ang = (i * 2 * math.pi / len(labels)) + random.uniform(-0.28, 0.28)
        rad = (0.42 + 0.16 * (i % 3)) * R
        bx = c + math.cos(ang) * rad
        by = c + math.sin(ang) * rad
        delay = round((ang % 6.28318) / 6.28318 * 4.0, 2)
        anchor = "end" if math.cos(ang) < -0.3 else "start"
        lx = bx - 9 if anchor == "end" else bx + 9
        blips.append(
            f'  <g style="animation-delay:{delay}s" class="blip">'
            f'<circle cx="{fmt(bx)}" cy="{fmt(by)}" r="3.5" fill="{GREEN}"/>'
            f'<circle cx="{fmt(bx)}" cy="{fmt(by)}" r="3.5" fill="none" stroke="{GREEN}" class="ping"/>'
            f'<text x="{fmt(lx)}" y="{fmt(by + 4)}" font-size="11" text-anchor="{anchor}" fill="{GREEN_SOFT}">{escape(lbl)}</text></g>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}" font-family="{MONO}" role="img" aria-label="Radar security: recon, web, binary, network, crypto, forensics">
  <title>security radar</title>
  <defs>
    <radialGradient id="sw">
      <stop offset="0" stop-color="{GREEN}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{GREEN}" stop-opacity="0"/>
    </radialGradient>
    <filter id="gr"><feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <style>
    .blip {{ opacity: 0; animation: bp 4s linear infinite; }}
    @keyframes bp {{ 0% {{ opacity: 1 }} 45% {{ opacity: .25 }} 100% {{ opacity: 0 }} }}
    .ping {{ animation: pg 4s linear infinite; transform-box: fill-box; transform-origin: center; }}
    @keyframes pg {{ 0% {{ r: 3.5; opacity: .9 }} 30% {{ opacity: 0 }} 100% {{ r: 16; opacity: 0 }} }}
  </style>
  <rect width="{S}" height="{S}" rx="16" fill="{CARD}"/>
  <circle cx="{fmt(c)}" cy="{fmt(c)}" r="{fmt(R)}" fill="#06120A"/>
  {rings}
  {cross}
  <g>
    <animateTransform attributeName="transform" type="rotate" dur="4s" repeatCount="indefinite" values="0 {fmt(c)} {fmt(c)};360 {fmt(c)} {fmt(c)}"/>
    <path d="M {fmt(c)} {fmt(c)} L {fmt(c + R)} {fmt(c)} A {fmt(R)} {fmt(R)} 0 0 0 {fmt(c + R * 0.866)} {fmt(c - R * 0.5)} Z" fill="url(#sw)"/>
    <line x1="{fmt(c)}" y1="{fmt(c)}" x2="{fmt(c + R)}" y2="{fmt(c)}" stroke="{GREEN}" stroke-opacity="0.8" filter="url(#gr)"/>
  </g>
{chr(10).join(blips)}
  <circle cx="{fmt(c)}" cy="{fmt(c)}" r="3" fill="{GREEN}" filter="url(#gr)"/>
  <text x="16" y="26" font-size="11" fill="{GREEN}" opacity="0.6">SCAN :: ACTIVE</text>
  <rect x="0.5" y="0.5" width="{S - 1}" height="{S - 1}" rx="16" fill="none" stroke="{GREEN}" stroke-opacity="0.3"/>
</svg>
"""



# --------------------------------------------------------------------------
# 6. BANNER — hero neon ala GitSkins (border animasi + nama gradient)
# --------------------------------------------------------------------------

NEON = {
    "bg": "#0B0F19",
    "card": "#0E1424",
    "a": "#22D3EE",   # cyan
    "b": "#A855F7",   # ungu
    "c": "#34D399",   # mint
    "text": "#9FB3C8",
}

ROUND = ("'Quicksand','Comfortaa','Nunito',ui-rounded,'Segoe UI',"
         "'Trebuchet MS',system-ui,sans-serif")


def build_banner(name="Atok Tajuddin",
                 kicker="ATOKTAJUDDIN",
                 subtitle="Systems Engineer  ·  Red Teamer",
                 pal=None):
    pal = pal or NEON
    W, H = 900, 300
    a, b, c = pal["a"], pal["b"], pal["c"]

    # partikel kecil yang mengambang
    dots = []
    for _ in range(26):
        x = round(random.uniform(30, W - 30), 1)
        y = round(random.uniform(30, H - 30), 1)
        r = round(random.uniform(0.8, 2.0), 2)
        dur = round(random.uniform(2.5, 6.0), 2)
        beg = round(random.uniform(-6, 0), 2)
        col = random.choice([a, b, c, "#FFFFFF"])
        dots.append(
            f'    <circle cx="{x}" cy="{y}" r="{r}" fill="{col}" opacity="0.5">'
            f'<animate attributeName="opacity" dur="{dur}s" begin="{beg}s" '
            f'repeatCount="indefinite" values="0.05;0.75;0.05"/>'
            f'<animate attributeName="cy" dur="{round(dur * 3, 2)}s" begin="{beg}s" '
            f'repeatCount="indefinite" values="{y};{round(y - 14, 1)};{y}"/></circle>'
        )

    # garis sirkuit/petir tipis di kiri-kanan
    bolts = []
    for (px, mirror) in ((120, 1), (W - 120, -1)):
        pts = []
        yy = 40
        xx = px
        while yy < H - 40:
            pts.append(f"{round(xx,1)},{yy}")
            xx += mirror * random.choice([-26, -18, 20, 28])
            yy += random.randint(38, 58)
        bolts.append(
            f'    <polyline points="{" ".join(pts)}" fill="none" stroke="{b}" '
            f'stroke-opacity="0.35" stroke-width="1.6" class="bolt"/>'
        )

    def bracket(x, y, sx, sy):
        L = 34
        return (f'<path d="M {x} {y + sy * L} L {x} {y} L {x + sx * L} {y}" fill="none" '
                f'stroke="{c}" stroke-width="2.5" stroke-linecap="round" opacity="0.85"/>')

    brackets = "".join([
        bracket(46, 46, 1, 1), bracket(W - 46, 46, -1, 1),
        bracket(46, H - 46, 1, -1), bracket(W - 46, H - 46, -1, -1),
    ])

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{escape(name)} - {escape(subtitle)}">
  <title>{escape(name)}</title>
  <defs>
    <linearGradient id="brd" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a}">
        <animate attributeName="stop-color" dur="9s" repeatCount="indefinite" values="{a};{b};{c};{a}"/></stop>
      <stop offset="0.5" stop-color="{b}">
        <animate attributeName="stop-color" dur="9s" repeatCount="indefinite" values="{b};{c};{a};{b}"/></stop>
      <stop offset="1" stop-color="{c}">
        <animate attributeName="stop-color" dur="9s" repeatCount="indefinite" values="{c};{a};{b};{c}"/></stop>
    </linearGradient>
    <linearGradient id="nameGrad" gradientUnits="userSpaceOnUse" x1="180" y1="0" x2="720" y2="0">
      <animate attributeName="x1" dur="6s" repeatCount="indefinite" values="-360;900"/>
      <animate attributeName="x2" dur="6s" repeatCount="indefinite" values="180;1440"/>
      <stop offset="0" stop-color="{a}"/>
      <stop offset="0.35" stop-color="{b}"/>
      <stop offset="0.7" stop-color="{c}"/>
      <stop offset="1" stop-color="{a}"/>
    </linearGradient>
    <radialGradient id="halo" cx="0.5" cy="0.45" r="0.7">
      <stop offset="0" stop-color="{b}" stop-opacity="0.22"/>
      <stop offset="1" stop-color="{b}" stop-opacity="0"/>
    </radialGradient>
    <filter id="nglow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
      <feGaussianBlur stdDeviation="2.2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
    <clipPath id="bcard"><rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="22"/></clipPath>
  </defs>
  <style>
    .bolt {{ animation: bolt 5s ease-in-out infinite; }}
    @keyframes bolt {{ 0%,100% {{ opacity:.12 }} 45% {{ opacity:.45 }} 50% {{ opacity:.1 }} 55% {{ opacity:.5 }} }}
    .dash {{ animation: dash 7s linear infinite; }}
    @keyframes dash {{ to {{ stroke-dashoffset: -1000 }} }}
    .kick {{ animation: kick 3.5s ease-in-out infinite; }}
    @keyframes kick {{ 0%,100% {{ opacity:.55 }} 50% {{ opacity:1 }} }}
    .ul {{ animation: ul 4s ease-in-out infinite; }}
    @keyframes ul {{ 0%,100% {{ opacity:.35 }} 50% {{ opacity:.9 }} }}
  </style>

  <rect width="{W}" height="{H}" rx="26" fill="{pal['bg']}"/>
  <g clip-path="url(#bcard)">
    <rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="22" fill="{pal['card']}"/>
    <rect x="14" y="14" width="{W - 28}" height="{H - 28}" fill="url(#halo)"/>
{chr(10).join(bolts)}
{chr(10).join(dots)}
  </g>

  <g filter="url(#nglow)">
    <rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="22" fill="none"
          stroke="url(#brd)" stroke-width="2.6" stroke-dasharray="220 90" class="dash"/>
  </g>
  <rect x="14" y="14" width="{W - 28}" height="{H - 28}" rx="22" fill="none" stroke="url(#brd)" stroke-width="1" stroke-opacity="0.35"/>
  {brackets}

  <text x="{W // 2}" y="102" text-anchor="middle" font-family="{MONO}" font-size="13"
        letter-spacing="5" fill="{a}" class="kick">&#8249; {escape(kicker.upper())} &#8250;</text>

  <g filter="url(#soft)">
    <text x="{W // 2}" y="176" text-anchor="middle" font-family="{ROUND}" font-size="62"
          font-weight="700" letter-spacing="1" fill="url(#nameGrad)">{escape(name)}</text>
  </g>

  <g class="ul">
    <line x1="{W // 2 - 160}" y1="198" x2="{W // 2 + 160}" y2="198" stroke="{c}"
          stroke-width="2" stroke-dasharray="9 9" stroke-linecap="round"/>
  </g>

  <text x="{W // 2}" y="234" text-anchor="middle" font-family="{MONO}" font-size="15"
        letter-spacing="3" fill="{pal['text']}">{escape(subtitle)}</text>

  <g>
    <circle cx="{W // 2}" cy="262" r="3" fill="{a}">
      <animate attributeName="opacity" dur="1.6s" repeatCount="indefinite" values="1;.2;1"/></circle>
    <circle cx="{W // 2 - 16}" cy="262" r="3" fill="{b}">
      <animate attributeName="opacity" dur="1.6s" begin="-0.5s" repeatCount="indefinite" values="1;.2;1"/></circle>
    <circle cx="{W // 2 + 16}" cy="262" r="3" fill="{c}">
      <animate attributeName="opacity" dur="1.6s" begin="-1s" repeatCount="indefinite" values="1;.2;1"/></circle>
  </g>
</svg>
"""


def build_divider_neon(pal=None):
    """Garis pembatas ujung diamond + kilau berjalan (gaya GitSkins)."""
    pal = pal or NEON
    W, H = 900, 22
    a, b, c = pal["a"], pal["b"], pal["c"]
    cy = H / 2
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="pembatas">
  <defs>
    <linearGradient id="dl" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{a}"/><stop offset="0.5" stop-color="{b}"/><stop offset="1" stop-color="{c}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="#fff" stop-opacity="0"/>
      <stop offset="0.5" stop-color="#fff" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </linearGradient>
    <filter id="dg"><feGaussianBlur stdDeviation="2.2" result="x"/>
      <feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <g filter="url(#dg)">
    <line x1="18" y1="{fmt(cy)}" x2="{W - 18}" y2="{fmt(cy)}" stroke="url(#dl)" stroke-width="2"/>
    <path d="M 6 {fmt(cy)} L 14 {fmt(cy - 7)} L 22 {fmt(cy)} L 14 {fmt(cy + 7)} Z" fill="{a}"/>
    <path d="M {W - 22} {fmt(cy)} L {W - 14} {fmt(cy - 7)} L {W - 6} {fmt(cy)} L {W - 14} {fmt(cy + 7)} Z" fill="{c}"/>
  </g>
  <rect y="{fmt(cy - 1.5)}" width="150" height="3" fill="url(#shine)" opacity="0.8">
    <animate attributeName="x" dur="4.5s" repeatCount="indefinite" values="-150;{W}"/>
  </rect>
  <circle cy="{fmt(cy)}" r="3.5" fill="#fff" opacity="0.9" filter="url(#dg)">
    <animate attributeName="cx" dur="4.5s" repeatCount="indefinite" values="18;{W - 18};18"
             keyTimes="0;0.5;1" calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>
  </circle>
</svg>
"""



# --------------------------------------------------------------------------
# 7. SECTION HEADER — pengganti heading markdown "> system.stats" yang kaku
# --------------------------------------------------------------------------

def build_section(title, hint=""):
    W, H = 900, 56
    a, b, c = NEON["a"], NEON["b"], NEON["c"]
    cy = 34
    tw = len(title) * 11.4 + 46          # perkiraan lebar teks buat menaruh garis
    hint_el = ('<text x="%d" y="%d" text-anchor="end" font-size="11" fill="%s">%s</text>'
               % (W - 4, cy - 14, GREEN_DIM, escape(hint))) if hint else ""
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="{MONO}" role="img" aria-label="{escape(title)}">
  <title>{escape(title)}</title>
  <defs>
    <linearGradient id="lg" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{a}" stop-opacity="0.9"/>
      <stop offset="0.5" stop-color="{b}" stop-opacity="0.55"/>
      <stop offset="1" stop-color="{c}" stop-opacity="0"/>
    </linearGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/>
    </linearGradient>
    <filter id="sg"><feGaussianBlur stdDeviation="1.6" result="x"/>
      <feMerge><feMergeNode in="x"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
  </defs>
  <style>
    .cr {{ animation: bl 1.05s steps(1) infinite; }}
    @keyframes bl {{ 0%,55% {{ opacity:1 }} 56%,100% {{ opacity:0 }} }}
  </style>
  <rect x="0" y="{cy - 20}" width="5" height="26" rx="2.5" fill="url(#bar)" filter="url(#sg)"/>
  <text x="20" y="{cy}" font-size="19" font-weight="700" fill="{GREEN}" filter="url(#sg)">&gt; {escape(title)}</text>
  <rect x="{fmt(tw)}" y="{cy - 15}" width="10" height="16" fill="{GREEN}" class="cr"/>
  <line x1="{fmt(tw + 26)}" y1="{cy - 7}" x2="{W - 4}" y2="{cy - 7}" stroke="url(#lg)" stroke-width="2"/>
  <circle cy="{cy - 7}" r="3" fill="#fff" opacity="0.85">
    <animate attributeName="cx" dur="5s" repeatCount="indefinite" values="{fmt(tw + 26)};{W - 14};{fmt(tw + 26)}"
             keyTimes="0;0.5;1" calcMode="spline" keySplines="0.4 0 0.2 1;0.4 0 0.2 1"/>
    <animate attributeName="opacity" dur="5s" repeatCount="indefinite" values="0;0.9;0.9;0"/>
  </circle>
  {hint_el}
</svg>
"""


# --------------------------------------------------------------------------
# 8. NOW — panel "ps aux" animasi, pengganti daftar bullet
# --------------------------------------------------------------------------

def build_now(rows=None):
    rows = rows or [
        ("0x01", "low-level utils in C & Rust", "RUNNING"),
        ("0x02", "red team tradecraft & reverse engineering", "TRAINING"),
        ("0x03", "backend services in Go & TypeScript", "SHIPPING"),
        ("0x04", "bare-metal ARM (C + Assembly)", "EXPLORING"),
        ("0x05", "networking & system architecture", "LEARNING"),
    ]
    W = 900
    RH = 34.0
    top = 62.0
    H = top + RH * len(rows) + 18
    BAR_X, BAR_W = 560.0, 190.0

    out = []
    for i, (pid, task, state) in enumerate(rows):
        y = top + i * RH
        beg = round(-i * 0.9, 2)
        out.append(
            '  <g>\n'
            f'    <rect x="14" y="{fmt(y - 20)}" width="{W - 28}" height="{fmt(RH - 6)}" rx="7" fill="#0A160E" opacity="0.55"/>\n'
            f'    <text x="30" y="{fmt(y)}" font-size="13" fill="{GREEN_DIM}">{escape(pid)}</text>\n'
            f'    <text x="86" y="{fmt(y)}" font-size="14" fill="{GREEN_SOFT}">{escape(task)}</text>\n'
            f'    <rect x="{fmt(BAR_X)}" y="{fmt(y - 8)}" width="{fmt(BAR_W)}" height="7" rx="3.5" fill="#0E2A18"/>\n'
            f'    <rect y="{fmt(y - 8)}" width="58" height="7" rx="3.5" fill="{GREEN}" opacity="0.9">\n'
            f'      <animate attributeName="x" dur="3.2s" begin="{beg}s" repeatCount="indefinite"\n'
            f'               values="{fmt(BAR_X)};{fmt(BAR_X + BAR_W - 58)};{fmt(BAR_X)}" keyTimes="0;0.5;1"\n'
            f'               calcMode="spline" keySplines="0.45 0 0.55 1;0.45 0 0.55 1"/>\n'
            f'    </rect>\n'
            f'    <circle cx="{fmt(BAR_X + BAR_W + 18)}" cy="{fmt(y - 5)}" r="4" fill="{GREEN}">\n'
            f'      <animate attributeName="opacity" dur="1.8s" begin="{beg}s" repeatCount="indefinite" values="1;0.2;1"/>\n'
            f'    </circle>\n'
            f'    <text x="{fmt(BAR_X + BAR_W + 30)}" y="{fmt(y)}" font-size="12" fill="{GREEN}" letter-spacing="1">{escape(state)}</text>\n'
            '  </g>'
        )

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {fmt(H)}" width="{W}" height="{fmt(H)}" font-family="{MONO}" role="img" aria-label="Sedang dikerjakan: {escape(', '.join(r[1] for r in rows))}">
  <title>ps aux - sedang berjalan</title>
  <rect width="{W}" height="{fmt(H)}" rx="14" fill="{CARD}"/>
  <rect x="0" y="0" width="{W}" height="36" rx="14" fill="#0A160E"/>
  <rect x="0" y="22" width="{W}" height="14" fill="#0A160E"/>
  <text x="30" y="23" font-size="12" fill="{GREEN_DIM}" letter-spacing="2">PID</text>
  <text x="86" y="23" font-size="12" fill="{GREEN_DIM}" letter-spacing="2">TASK</text>
  <text x="{fmt(BAR_X)}" y="23" font-size="12" fill="{GREEN_DIM}" letter-spacing="2">ACTIVITY</text>
  <text x="{fmt(BAR_X + 208)}" y="23" font-size="12" fill="{GREEN_DIM}" letter-spacing="2">STATE</text>
  <line x1="0" y1="36" x2="{W}" y2="36" stroke="{GREEN}" stroke-opacity="0.22"/>
{chr(10).join(out)}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{fmt(H - 1)}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.3"/>
</svg>
"""


# --------------------------------------------------------------------------
# 9. FOCUS LIST — daftar bidang fokus dengan animasi stagger
# --------------------------------------------------------------------------

def build_focus_list(items=None):
    items = items or [
        ("low-level & systems programming", "C / Rust / Assembly"),
        ("offensive security", "red team / reverse engineering"),
        ("hardware programming", "bare-metal ARM"),
        ("backend engineering", "Go / TypeScript / SQL"),
        ("networking & architecture", "TCP/IP / distributed systems"),
    ]
    W = 540
    RH = 56.0
    H = 24 + RH * len(items) + 8
    a, b = NEON["a"], NEON["b"]
    rows = []
    for i, (title, sub) in enumerate(items):
        y = 34 + i * RH
        d = round(i * 0.35, 2)
        rows.append(
            f'  <g class="row" style="animation-delay:{d}s">\n'
            f'    <rect x="18" y="{fmt(y - 9)}" width="10" height="10" rx="2" fill="{a if i % 2 == 0 else b}"/>\n'
            f'    <rect x="14" y="{fmt(y - 13)}" width="18" height="18" rx="4" fill="none" stroke="{GREEN}">\n'
            f'      <animate attributeName="opacity" dur="2.4s" begin="{d}s" repeatCount="indefinite" values="0.15;0.85;0.15"/>\n'
            f'    </rect>\n'
            f'    <text x="46" y="{fmt(y)}" font-size="15" fill="{GREEN}">{escape(title)}</text>\n'
            f'    <text x="46" y="{fmt(y + 19)}" font-size="12" fill="{GREEN_DIM}">{escape(sub)}</text>\n'
            f'    <line x1="16" y1="{fmt(y + 32)}" x2="{W - 16}" y2="{fmt(y + 32)}" stroke="{GREEN}" stroke-opacity="0.12"/>\n'
            '  </g>'
        )
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {fmt(H)}" width="{W}" height="{fmt(H)}" font-family="{MONO}" role="img" aria-label="Bidang fokus: {escape(', '.join(i[0] for i in items))}">
  <title>focus areas</title>
  <style>
    .row {{ opacity: 0; animation: in 9s ease-out infinite; }}
    @keyframes in {{ 0% {{ opacity: 0; transform: translateX(-14px) }}
      8%, 96% {{ opacity: 1; transform: translateX(0) }}
      100% {{ opacity: 0; transform: translateX(-14px) }} }}
  </style>
  <rect width="{W}" height="{fmt(H)}" rx="14" fill="{CARD}"/>
{chr(10).join(rows)}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{fmt(H - 1)}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.3"/>
</svg>
"""


def main():
    os.makedirs(OUT, exist_ok=True)
    assets = {
        "hero.svg": build_hero(),
        "glitch.svg": build_glitch(),
        "marquee.svg": build_marquee(),
        "divider.svg": build_divider(),
        "radar.svg": build_radar(),
        "banner.svg": build_banner(),
        "divider-neon.svg": build_divider_neon(),
        "now.svg": build_now(),
        "focus-list.svg": build_focus_list(),
    }
    for key, title, hint in [
        ("whoami", "whoami", "identity"),
        ("focus", "focus.areas", "where the time goes"),
        ("arsenal", "arsenal", "tools of the trade"),
        ("projects", "featured.projects", "public repositories"),
        ("now", "ps aux", "currently running"),
        ("stats", "system.stats", "live from github"),
        ("connect", "connect", "say hi"),
    ]:
        assets["sect-%s.svg" % key] = build_section(title, hint)

    for name, svg in assets.items():
        path = os.path.join(OUT, name)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("%-14s %6d bytes" % (name, len(svg.encode("utf-8"))))


if __name__ == "__main__":
    main()
