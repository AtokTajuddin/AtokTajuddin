#!/usr/bin/env python3
"""Varian bento: grid tile asimetris, tiap tile punya warna dan grafiknya sendiri."""

import math

from common import (ABOUT, ALL, COLLAB, GH, HTB_URL, PROJECTS, STATS, THM_HANDLE, THM_URL, TOOLKIT, doc, enter, fade, fmt, icon,
                    kt, measure, out_dir, pct, pic, plen, poly, slide, stroke_in, text, wrap, write, write_readme)

G = 6  # separuh jarak antar tile, dipanggang ke dalam SVG
R = 20

PAL = {
    "dark": dict(mode="dark", tile="#14141B", tile2="#1B1B24", line="#272734", line2="#353545", text="#F4F4F8",
                 muted="#A3A3B8", faint="#62627A", cyan="#22D3EE", violet="#A78BFA", rose="#FB7185",
                 amber="#FBBF24", green="#34D399", blue="#60A5FA", ink="#0B0B10"),
    "light": dict(mode="light", tile="#FFFFFF", tile2="#F5F5FA", line="#E4E4EC", line2="#D3D3DF", text="#14141B",
                  muted="#56566B", faint="#9C9CB0", cyan="#0891B2", violet="#7C3AED", rose="#E11D48",
                  amber="#D97706", green="#059669", blue="#2563EB", ink="#FFFFFF"),
}


def tile(t, W, H, body, label, fill=None, stroke=None):
    w, h = W - 2 * G, H - 2 * G
    frame = (f'<defs><clipPath id="tc"><rect x="{G}" y="{G}" width="{w}" height="{h}" rx="{R}"/></clipPath></defs>'
             f'<rect x="{G + 0.5}" y="{G + 0.5}" width="{w - 1}" height="{h - 1}" rx="{R - 0.5}" '
             f'fill="{fill or t["tile"]}" stroke="{stroke or t["line"]}"/>')
    return doc(W, H, frame + f'<g clip-path="url(#tc)">{body}</g>', ALL, label, transparent=True, t=t)


# ------------------------------------------------------------------ hero (2/3)
def hero(t):
    W, H = 560, 340
    b = []
    b.append(text(34, 50, "Surabaya, Indonesia", "m", "mono-400", 11, t["faint"]))
    b.append(enter(text(31, 118, "Atok", "b", "black-900", 60, t["text"], spacing=-1.8), 0.1, dy=14))
    b.append(enter(text(31, 178, "Tajuddin", "b", "black-900", 60, t["text"], spacing=-1.8), 0.22, dy=14))
    role = (f'<text x="34" y="214" class="s" font-size="15.5" font-weight="500" fill="{t["muted"]}" xml:space="preserve">'
            f'<tspan fill="{t["cyan"]}">Offensive security</tspan> and <tspan fill="{t["violet"]}">DevSecOps</tspan></text>')
    b.append(enter(role, 0.4, dy=8))
    para = "Information Technology student at ITS. I learn on Hack The Box and TryHackMe, then build the tools I needed along the way."
    for i, line in enumerate(wrap(para, "sans-400", 13, 268)):
        b.append(text(34, 256 + i * 19.5, line, "s", "sans-400", 13, t["muted"]))
    # laptop + topi putih
    LX, LY, LW, LH = 330, 96, 196, 128
    lap = [
        f'<rect x="{LX}" y="{LY}" width="{LW}" height="{LH}" rx="10" fill="{t["tile2"]}" stroke="{t["line2"]}" stroke-width="1.2"/>',
        f'<rect x="{LX + 9}" y="{LY + 9}" width="{LW - 18}" height="{LH - 22}" rx="4" fill="{"#0B0B12" if t["mode"] == "dark" else "#14141B"}"/>',
        f'<circle cx="{LX + LW / 2}" cy="{LY + LH - 6.5}" r="1.6" fill="{t["line2"]}"/>',
        f'<path d="M{LX - 18} {LY + LH + 4}H{LX + LW + 18}L{LX + LW + 8} {LY + LH + 16}H{LX - 8}Z" fill="{t["tile2"]}" stroke="{t["line2"]}" stroke-width="1.2" stroke-linejoin="round"/>',
        f'<rect x="{LX + LW / 2 - 22}" y="{LY + LH + 4}" width="44" height="4" rx="2" fill="{t["line2"]}"/>',
    ]
    b.extend(lap)
    # baris terminal di layar, muncul satu per satu sekali
    rows = [
        [("$", "#8B8BA3", 1), (" nmap -sC -sV 10.10.11.42", "#E8E8F0", 0)],
        [("22/tcp", t["green"] if t["mode"] == "dark" else "#34D399", 0), ("  open  ssh", "#8B8BA3", 0)],
        [("80/tcp", t["green"] if t["mode"] == "dark" else "#34D399", 0), ("  open  http", "#8B8BA3", 0)],
        [("$", "#8B8BA3", 1), (" ffuf -w dirs.txt", "#E8E8F0", 0)],
        [("/admin", "#22D3EE", 0), ("  [Status: 302]", "#8B8BA3", 0)],
        [("$", "#8B8BA3", 1), (" sudo -l", "#E8E8F0", 0)],
        [("(root) NOPASSWD:", "#FB7185", 0), (" /usr/bin/vim", "#FBBF24", 0)],
    ]
    for i, segs in enumerate(rows):
        spans = "".join(f'<tspan fill="{c}">{s.replace("<", "&lt;")}</tspan>' for s, c, _ in segs)
        b.append(f'<g opacity="1">{fade(0.6 + i * 0.22, 0.25)}<text x="{LX + 17}" y="{LY + 25 + i * 13.2}" class="m" font-size="8.6" font-weight="400" xml:space="preserve">{spans}</text></g>')
    # topi fedora putih di sudut layar
    hat = (
        f'<g transform="translate({LX + LW - 30} {LY - 6}) rotate(14)">'
        f'<ellipse cx="0" cy="8" rx="44" ry="9.5" fill="#F4F4F8" stroke="#C9C9D6" stroke-width="1"/>'
        f'<path d="M-25 7C-26 -10 -22 -24 -12 -27C-6 -29 -3 -24 0 -24C3 -24 6 -29 12 -27C22 -24 26 -10 25 7C12 10 -12 10 -25 7Z" fill="#FFFFFF" stroke="#C9C9D6" stroke-width="1"/>'
        f'<path d="M-25.4 0C-12 3.5 12 3.5 25.4 0L25.2 6.6C12 9.8 -12 9.8 -25.2 6.6Z" fill="{t["cyan"]}"/>'
        f'<path d="M-4 -23C-2 -17 2 -17 4 -23" fill="none" stroke="#D9D9E4" stroke-width="1.2" stroke-linecap="round"/>'
        f'</g>'
    )
    b.append(f'<g>{slide(0.9, 0, -40, 0.9)}<g>{fade(0.9, 0.5)}{hat}</g></g>')
    return tile(t, W, H, "".join(b), "Atok Tajuddin, offensive security and DevSecOps. A laptop runs nmap, ffuf and sudo -l, with a white hat resting on the screen.")


# --------------------------------------------------------------- brand tiles
def htb(t):
    W, H = 280, 340
    lime = "#9FEF00"
    b = []
    # pola kubus isometrik samar di belakang logo
    cube = []
    for gx in range(-1, 6):
        for gy in range(-1, 5):
            cx, cy = gx * 52 + (26 if gy % 2 else 0), gy * 45 + 10
            cube.append(f'M{cx} {cy - 15}L{cx + 26} {cy}L{cx} {cy + 15}L{cx - 26} {cy}Z')
    b.append(f'<path d="{"".join(cube)}" fill="none" stroke="{lime}" stroke-opacity="0.07"/>')
    b.append(f'<g>{slide(0.2, 0, 16, 0.9)}<g>{fade(0.2, 0.6)}<g transform="translate(92 70) scale(4)"><path d="{icon("hackthebox")}" fill="{lime}"/></g></g></g>')
    b.append(text(30, 254, "Hack The Box", "d", "display-600", 24, "#F4F6FA", spacing=-0.4))
    b.append(text(31, 282, "Web, Linux and Windows machines", "s", "sans-400", 12.5, "#A4B1CD"))
    b.append(text(31, 306, "View profile", "s", "sans-500", 12.5, lime))
    return tile(t, W, H, "".join(b), "Hack The Box profile", fill="#111927", stroke="#1F2B40")


def thm(t):
    W, H = 280, 250
    b = []
    for i in range(7):
        b.append(f'<circle cx="236" cy="54" r="{24 + i * 22}" fill="none" stroke="#FFFFFF" stroke-opacity="{0.10 - i * 0.012:.3f}"/>')
    b.append(f'<g>{fade(0.3, 0.6)}<g transform="translate(186 20) scale(3.3)"><path d="{icon("tryhackme")}" fill="#FFFFFF"/></g></g>')
    b.append(text(30, 168, "TryHackMe", "d", "display-600", 24, "#FFFFFF", spacing=-0.4))
    b.append(text(31, 194, THM_HANDLE, "m", "mono-400", 12, "#FFD3D3"))
    b.append(text(31, 218, "View profile", "s", "sans-500", 12.5, "#FFFFFF"))
    return tile(t, W, H, "".join(b), "TryHackMe profile " + THM_HANDLE, fill="#C8141B", stroke="#A80F15")


# ---------------------------------------------------------------- projects
def head(t, p, x, y, wmax, accent):
    b = [text(x, y, p["repo"], "m", "mono-400", 10.5, t["faint"]),
         text(x - 1, y + 30, p["title"], "d", "display-600", 23, t["text"], spacing=-0.4)]
    lines = wrap(p["desc"], "sans-400", 13, wmax)
    for i, line in enumerate(lines):
        b.append(text(x, y + 56 + i * 19, line, "s", "sans-400", 13, t["muted"]))
    return b, y + 56 + len(lines) * 19


def chips(t, tags, x, y, color):
    b = []
    for tag in tags:
        w = measure(tag, "mono-400", 10) + 16
        b.append(f'<rect x="{fmt(x)}" y="{y}" width="{fmt(w)}" height="20" rx="10" fill="{color}" fill-opacity="0.12"/>')
        b.append(text(x + w / 2, y + 13.5, tag, "m", "mono-400", 10, color, anchor="middle"))
        x += w + 6
    return b


def nexus(t):
    W, H = 560, 250
    p = PROJECTS[0]
    b, yb = head(t, p, 30, 44, 216, t["cyan"])
    b += chips(t, p["tags"], 30, H - G - 44, t["cyan"])
    # diagram pipeline: dua sensor -> ML -> Shuffle -> respons
    line = f'fill="none" stroke="{t["line2"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"'
    paths = [
        [(376, 66), (390, 66), (390, 108), (404, 108)],
        [(376, 150), (390, 150), (390, 108), (404, 108)],
        [(446, 125), (446, 163)],
        [(488, 180), (500, 180)],
    ]
    delays = [0.3, 0.4, 1.2, 1.8]
    for pts, dl in zip(paths, delays):
        b.append(stroke_in(poly(pts), plen(pts), dl, line, dur=0.5))
    nodes = [(292, 66, 84, "Suricata", t["cyan"], 0.1), (292, 150, 84, "Tetragon", t["cyan"], 0.2),
             (404, 108, 96, "ML + CVE", t["violet"], 0.9), (404, 180, 84, "Shuffle", t["green"], 1.5)]
    for x0, y, w, label, col, delay in nodes:
        node = (f'<rect x="{x0}" y="{y - 17}" width="{w}" height="34" rx="9" fill="{col}" fill-opacity="0.13" stroke="{col}" stroke-opacity="0.6"/>'
                f'<circle cx="{x0 + 13}" cy="{y}" r="3.2" fill="{col}"/>'
                + text(x0 + 22, y + 4, label, "s", "sans-500", 11.5, t["text"]))
        b.append(enter(node, delay, dy=6, dur=0.6))
    for i, pts in enumerate(paths[:2]):
        d = poly(pts)
        b.append(f'<circle r="3.4" fill="{t["cyan"]}" opacity="0"><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" begin="{0.6 + i * 0.2}s" dur="0.7s" fill="freeze"/>'
                 f'<animateMotion path="{d}" begin="{0.6 + i * 0.2}s" dur="0.7s" calcMode="spline" keyPoints="0;1" keyTimes="0;1" keySplines=".45 0 .2 1" fill="freeze"/></circle>')
    ok = (f'<circle cx="514" cy="180" r="14" fill="{t["green"]}"/>'
          f'<path d="M507.5 180l4.5 4.5 8.5-9" fill="none" stroke="{t["ink"]}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    b.append(enter(ok, 2.1, dy=4, dur=0.5))
    return tile(t, W, H, "".join(b), f"Project: {p['title']} - {p['desc']}")


def boar(t):
    W, H = 420, 290
    p = PROJECTS[1]
    b, yb = head(t, p, 30, 44, 350, t["rose"])
    # stack memori: buf[8] | rbp | ret
    x0, y0, cw, ch = 30, 176, 28.4, 30
    labels = ["buf[8]"] * 8 + ["rbp", "rbp", "ret", "ret"]
    for i in range(12):
        x = x0 + i * (cw + 2)
        over = i >= 8
        b.append(f'<rect x="{fmt(x)}" y="{y0}" width="{fmt(cw)}" height="{ch}" rx="4" fill="{t["tile2"]}" stroke="{t["line2"]}"/>')
        col = t["rose"] if over else t["amber"]
        fill = (f'<rect x="{fmt(x)}" y="{y0}" width="{fmt(cw)}" height="{ch}" rx="4" fill="{col}" fill-opacity="{0.9 if over else 0.22}"/>'
                + text(x + cw / 2, y0 + 19.5, "41", "m", "mono-500", 11, t["ink"] if over else t["text"], anchor="middle"))
        b.append(f'<g>{fade(0.5 + i * 0.12, 0.2)}{fill}</g>')
    b.append(f'<path d="M{x0} {y0 + ch + 9}h{8 * (cw + 2) - 2}" stroke="{t["faint"]}" stroke-width="1"/>')
    b.append(text(x0, y0 + ch + 24, "char buf[8]", "m", "mono-400", 10, t["faint"]))
    bx = x0 + 8 * (cw + 2)
    b.append(text(bx + cw + 1, y0 + ch + 24, "rbp", "m", "mono-400", 10, t["faint"], anchor="middle"))
    b.append(text(bx + 3 * (cw + 2) - 1, y0 + ch + 24, "ret", "m", "mono-400", 10, t["rose"], anchor="middle"))
    b.append(enter(text(W - G - 30, 166, "SIGSEGV", "m", "mono-500", 10.5, t["rose"], anchor="end"), 2.0, dy=4, dur=0.4))
    b += chips(t, p["tags"], 30, H - G - 40, t["rose"])
    return tile(t, W, H, "".join(b), f"Project: {p['title']} - {p['desc']}")


def pe(t):
    W, H = 420, 290
    p = PROJECTS[2]
    b, yb = head(t, p, 30, 44, 350, t["amber"])
    rows = [
        ("00000000", ["4D", "5A", "90", "00", "03", "00", "00", "00"], {0: "amber", 1: "amber"}),
        ("00000038", ["00", "00", "00", "00", "80", "00", "00", "00"], {4: "blue"}),
        ("00000080", ["50", "45", "00", "00", "4C", "01", "03", "00"], {0: "amber", 1: "amber", 2: "amber", 3: "amber"}),
    ]
    y = 168
    for r, (off, bytes_, hl) in enumerate(rows):
        b.append(text(30, y + r * 24, off, "m", "mono-400", 11, t["faint"]))
        for i, byte in enumerate(bytes_):
            x = 104 + i * 25
            col = hl.get(i)
            if col:
                box = f'<rect x="{x - 3}" y="{y + r * 24 - 13}" width="22" height="18" rx="4" fill="{t[col]}" fill-opacity="0.2" stroke="{t[col]}" stroke-opacity="0.7"/>'
                b.append(f'<g>{fade(0.5 + r * 0.35 + i * 0.05, 0.3)}{box}</g>')
            b.append(text(x + 8, y + r * 24, byte, "m", "mono-400", 11, t[col] if col else t["muted"], anchor="middle"))
    asc = ["MZ......", "........", "PE..L..."]
    for r, a in enumerate(asc):
        b.append(text(312, y + r * 24, a, "m", "mono-400", 11, t["faint"]))
    b.append(enter(text(W - G - 30, 152, "e_lfanew = 0x80", "m", "mono-400", 10, t["blue"], anchor="end"), 1.4, dy=4, dur=0.4))
    b += chips(t, p["tags"], 30, H - G - 40, t["amber"])
    return tile(t, W, H, "".join(b), f"Project: {p['title']} - {p['desc']}")


# ------------------------------------------------------------- toolkit + stats
def toolkit(t):
    W, H = 560, 270
    cols = [t["rose"], t["cyan"], t["violet"], t["green"]]
    b = [text(30, 46, "Toolkit", "d", "display-600", 20, t["text"], spacing=-0.3)]
    y = 82
    for (head_, items), col in zip(TOOLKIT, cols):
        b.append(f'<circle cx="34" cy="{y - 4}" r="4" fill="{col}"/>')
        b.append(text(46, y, head_, "s", "sans-500", 12, t["muted"]))
        x = 150
        for it in items:
            w = measure(it, "sans-400", 11.5) + 14
            b.append(f'<rect x="{fmt(x)}" y="{y - 16}" width="{fmt(w)}" height="24" rx="7" fill="{t["tile2"]}" stroke="{t["line"]}"/>')
            b.append(text(x + 7, y, it, "s", "sans-400", 11.5, t["text"]))
            x += w + 5
        assert x < W - G - 20, (head_, x)
        y += 44
    return tile(t, W, H, "".join(b), "Toolkit: " + "; ".join(h + ": " + ", ".join(i) for h, i in TOOLKIT))


def languages(t):
    W, H = 280, 270
    b = [text(30, 46, "Languages", "d", "display-600", 20, t["text"], spacing=-0.3)]
    x, bw, y = 30, W - 2 * G - 48, 74
    for i, (name, share, col) in enumerate(STATS["languages"]):
        w = bw * share
        bar = f'<rect x="{fmt(x)}" y="{y}" width="{fmt(max(w - 2, 1))}" height="12" rx="3" fill="{col}"/>'
        b.append(f'<g>{fade(0.2 + i * 0.1, 0.3)}{bar}</g>')
        x += w
    for i, (name, share, col) in enumerate(STATS["languages"]):
        ly = y + 44 + i * 24
        b.append(f'<circle cx="34" cy="{ly - 4}" r="4" fill="{col}"/>')
        b.append(text(46, ly, name, "s", "sans-400", 12, t["text"]))
        b.append(text(W - G - 30, ly, f"{share * 100:.1f}%", "m", "mono-400", 11, t["muted"], anchor="end"))
    langs = ", ".join(f"{n} {round(s_ * 100)}%" for n, s_, _ in STATS["languages"])
    return tile(t, W, H, "".join(b), "Languages across public repositories: " + langs)


def streaks():
    days = STATS.get("calendar", [])
    longest = run = 0
    for lv in days:
        run = run + 1 if lv else 0
        longest = max(longest, run)
    # hari ini yang belum ada kontribusi tidak memutus streak
    cur, tail = 0, days[:-1] if days and not days[-1] else days
    for lv in reversed(tail):
        if not lv:
            break
        cur += 1
    return sum(1 for lv in days if lv), longest, cur


def activity(t):
    W, H = 560, 300
    m = STATS["metrics"]
    active, longest, cur = streaks()
    b = [text(30, 46, "GitHub activity", "d", "display-600", 20, t["text"], spacing=-0.3),
         text(W - G - 30, 46, "past 12 months", "m", "mono-400", 10.5, t["faint"], anchor="end"),
         enter(text(27, 130, str(m["contributions"]), "b", "black-900", 68, t["text"], spacing=-2.6), 0.15, dy=10),
         text(30, 154, "contributions", "s", "sans-400", 12.5, t["muted"])]
    side = [(str(active), "active days", t["green"]), (str(longest), "longest streak, days", t["amber"])]
    if cur:
        side[1] = (str(cur), f"day streak now, best {longest}", t["amber"])
    for i, (num, lab, col) in enumerate(side):
        x = 262 + i * 140
        b.append(f'<rect x="{x}" y="84" width="3" height="66" rx="1.5" fill="{col}"/>')
        b.append(enter(text(x + 16, 122, num, "d", "display-600", 32, t["text"], spacing=-0.8), 0.3 + i * 0.15, dy=8))
        b.append(text(x + 17, 146, lab, "s", "sans-400", 12, t["muted"]))
    cells = [("pull_requests", "pull requests"), ("issues", "issues opened"), ("stars", "stars earned"),
             ("forks", "forks"), ("repositories", "public repos"), ("followers", "followers")]
    b.append(f'<path d="M30 182H{W - G - 30}" stroke="{t["line"]}"/>')
    for i, (key, lab) in enumerate(cells):
        x, y = 30 + (i % 3) * 170, 218 + (i // 3) * 44
        num = str(m.get(key, 0))
        nw = measure(num, "display-600", 20, -0.3)
        cell = (text(x, y, num, "d", "display-600", 20, t["text"], spacing=-0.3)
                + text(x + nw + 8, y, lab, "s", "sans-400", 12, t["muted"]))
        b.append(f'<g>{fade(0.5 + i * 0.08, 0.3)}{cell}</g>')
    label = (f"{m['contributions']} contributions in the past year, {active} active days, longest streak {longest} days. "
             + ", ".join(f"{m.get(k, 0)} {lab}" for k, lab in cells))
    return tile(t, W, H, "".join(b), label)


# ambang peringkat S/A/B/C, dihitung sendiri dari stats.json
TROPHIES = [("Commits", "contributions", (1000, 100, 10, 1)), ("Repositories", "repositories", (50, 20, 10, 1)),
            ("Pull requests", "pull_requests", (100, 20, 5, 1)), ("Followers", "followers", (100, 20, 10, 1)),
            ("Streak", "streak", (100, 30, 7, 1)), ("Stars", "stars", (100, 30, 5, 1))]


def trophies(t):
    W, H = 280, 300
    m = dict(STATS["metrics"], streak=streaks()[1])
    tier_col = {"S": t["amber"], "A": t["cyan"], "B": t["violet"], "C": t["muted"], "-": t["faint"]}
    b = [text(30, 46, "Trophies", "d", "display-600", 20, t["text"], spacing=-0.3)]
    alt = []
    for i, (name, key, th) in enumerate(TROPHIES):
        v = m.get(key, 0)
        rank = next((r for r, lim in zip("SABC", th) if v >= lim), "-")
        col = tier_col[rank]
        x, top = 30 + (i % 2) * 122, 72 + (i // 2) * 72
        cx, cy, r = x + 16, top + 22, 17
        hexa = poly([(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)))
                     for a in range(-90, 270, 60)]) + "Z"
        badge = (f'<path d="{hexa}" fill="{col}" fill-opacity="0.14" stroke="{col}" stroke-width="1.6" stroke-linejoin="round"/>'
                 + text(cx, cy + 5.5, rank, "b", "black-900", 15, col, anchor="middle"))
        unit = "days" if key == "streak" else ""
        cell = badge + text(x + 40, top + 18, name, "s", "sans-500", 11.5, t["text"]) \
            + text(x + 40, top + 35, f"{v} {unit}".strip(), "m", "mono-400", 10.5, t["faint"])
        # teks tidak boleh menyentuh badge kolom kanan atau tepi tile
        limit = (30 + 122 - 6) if i % 2 == 0 else (W - G - 10)
        assert x + 40 + measure(name, "sans-500", 11.5) < limit, name
        b.append(enter(cell, 0.3 + i * 0.12, dy=6, dur=0.5))
        alt.append(f"{name} {rank} ({v})")
    return tile(t, W, H, "".join(b), "Trophies: " + ", ".join(alt))


def main():
    out = out_dir("bento")
    made = {}
    for mode, t in PAL.items():
        for name, fn in (("hero", hero), ("htb", htb), ("thm", thm), ("nexus", nexus), ("boar", boar), ("pe", pe),
                         ("toolkit", toolkit), ("langs", languages),
                         ("activity", activity), ("trophies", trophies)):
            svg = fn(t)
            write(f"{name}-{mode}.svg", svg, out)
            import re as _re
            made[name] = int(_re.search(r'width="([\d.]+)"', svg).group(1))
    w = {k: pct(v) for k, v in made.items()}
    raw = "https://raw.githubusercontent.com/AtokTajuddin/AtokTajuddin/output/"
    snake = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="{raw}github-snake-dark.svg" />'
             f'<source media="(prefers-color-scheme: light)" srcset="{raw}github-snake.svg" />'
             f'<img src="{raw}github-snake.svg" width="{pct(840 - 2 * G)}" alt="Contribution snake eating through the past year of GitHub activity" /></picture>')
    readme = f"""<p align="center">
{pic("hero", "Atok Tajuddin, offensive security and DevSecOps", w["hero"], href=GH + "?tab=repositories")}{pic("htb", "Hack The Box profile", w["htb"], href=HTB_URL)}
{pic("thm", "TryHackMe profile " + THM_HANDLE, w["thm"], href=THM_URL)}{pic("nexus", "Nexus Sentinel, a SOC lab in Docker Compose", w["nexus"], href=GH + "/" + PROJECTS[0]["repo"])}
{pic("boar", "BOAR, buffer-overflow analysis for C and C++", w["boar"], href=GH + "/" + PROJECTS[1]["repo"])}{pic("pe", "Nim PE Analyzer, a PE header checker", w["pe"], href=GH + "/" + PROJECTS[2]["repo"])}
{pic("toolkit", "Toolkit", w["toolkit"])}{pic("langs", "Languages", w["langs"])}
{pic("activity", "GitHub activity", w["activity"])}{pic("trophies", "Trophies", w["trophies"])}
</p>

<p align="center">{snake}</p>

{ABOUT}

{COLLAB}
"""
    write_readme("bento", readme)
    print("bento ok")


if __name__ == "__main__":
    main()
