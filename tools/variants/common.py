"""Konten dan helper bersama untuk varian profil alternatif.

Setiap varian menulis README.md dan assets/ ke variants/<nama>/, lalu
preview.py melayaninya di http://127.0.0.1:8765/<nama>/.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.dirname(HERE)
ROOT = os.path.dirname(TOOLS)
sys.path.insert(0, TOOLS)

from theme import FACES, doc, fmt, kt, measure, text, wrap, write  # noqa: E402,F401

ALL = set(FACES)
GH = "https://github.com/AtokTajuddin"
HTB_URL = "https://profile.hackthebox.com/profile/019cfed2-60ce-730f-a565-c66876cfda10"
THM_HANDLE = "Hadamard"
THM_URL = "https://tryhackme.com/p/" + THM_HANDLE

MAIN = "bento"  # varian yang jadi README utama di root repo
NAME = "Atok Tajuddin"
ABOUT = ("I study Information Technology at Institut Teknologi Sepuluh Nopember (ITS) in Surabaya. "
         "Most of my practice happens on Hack The Box and TryHackMe: web exploitation, then privilege "
         "escalation on Linux and Windows. Alongside it I write analysis tools in Python, C++ and Nim, "
         "and run a SOC lab for the defensive side.")

COLLAB = "Interested in collaborating on security research, CTFs, and open source security tooling."

PROJECTS = [
    {
        "slug": "nexus", "repo": "big_architectiure_soc_project", "title": "Nexus Sentinel",
        "lang": ("Python", "#3572A5"), "tags": ["Suricata", "Tetragon", "Shuffle"],
        "desc": "A SOC lab in Docker Compose. Suricata and Tetragon alerts pass through an ML service "
                "that adds CVE context, then Shuffle runs the response.",
    },
    {
        "slug": "boar", "repo": "BOAR_Project", "title": "BOAR",
        "lang": ("Python", "#3572A5"), "tags": ["CWE", "GDB", "SARIF"],
        "desc": "Finds buffer overflows in C and C++ source with 14 rules, confirms them by crashing "
                "the binary under GDB, and writes SARIF for code scanning.",
    },
    {
        "slug": "pe", "repo": "nim-pe-analyzer", "title": "Nim PE Analyzer",
        "lang": ("Nim", "#FFC200"), "tags": ["PE32", "DOS header"],
        "desc": "Reads a Windows executable's MZ and PE headers and reports when the magic bytes "
                "have been tampered with.",
    },
]

TOOLKIT = [
    ("Offensive and RE", ["Burp Suite", "Nmap", "Metasploit", "Wireshark", "Ghidra"]),
    ("Detection", ["Suricata", "Tetragon eBPF", "MISP", "Shuffle SOAR", "Grafana"]),
    ("Languages", ["Python", "C / C++", "Rust", "Go", "Nim"]),
    ("Platform", ["Linux", "Docker", "Git", "GitHub Actions", "Bash"]),
]

with open(os.path.join(ROOT, "assets", "stats.json"), encoding="utf-8") as _f:
    STATS = json.load(_f)


def icon(name):
    with open(os.path.join(TOOLS, "icons", name + ".svg"), encoding="utf-8") as f:
        return re.search(r'<path d="([^"]+)"', f.read()).group(1)


SPLINE = ".22 1 .36 1"


def fade(delay, dur=0.6):
    """Muncul sekali: nilai statis tetap terlihat, animasi mulai dari 0 lalu diam."""
    total = delay + dur
    return (f'<animate attributeName="opacity" values="0;0;1" keyTimes="{kt(0, delay / total, 1)}" '
            f'dur="{fmt(total)}s" fill="freeze"/>')


def slide(delay, dx=0, dy=0, dur=0.8):
    total = delay + dur
    return (f'<animateTransform attributeName="transform" type="translate" values="{fmt(dx)} {fmt(dy)};{fmt(dx)} {fmt(dy)};0 0" '
            f'keyTimes="{kt(0, delay / total, 1)}" dur="{fmt(total)}s" calcMode="spline" '
            f'keySplines="0 0 1 1;{SPLINE}" fill="freeze"/>')


def enter(inner, delay, dx=0, dy=0, dur=0.8):
    return f'<g>{slide(delay, dx, dy, dur)}<g>{fade(delay, dur * 0.7)}{inner}</g></g>'


def plen(pts):
    return sum(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 for (x1, y1), (x2, y2) in zip(pts, pts[1:]))


def stroke_in(d, length, delay, attrs, dur=1.0):
    """Path yang tergambar sekali lewat stroke-dashoffset, lalu diam utuh."""
    total = delay + dur
    L = fmt(length + 1)
    return (f'<path d="{d}" {attrs} stroke-dasharray="{L} {L}" stroke-dashoffset="0">'
            f'<animate attributeName="stroke-dashoffset" values="{L};{L};0" keyTimes="{kt(0, delay / total, 1)}" '
            f'dur="{fmt(total)}s" calcMode="spline" keySplines="0 0 1 1;.45 0 .2 1" fill="freeze"/></path>')


def poly(pts):
    return "M" + "L".join(f"{fmt(x)} {fmt(y)}" for x, y in pts)


def pic(base, alt, width=None, height=None, href=None):
    """Elemen <picture> dark/light untuk README."""
    size = f' width="{width}"' if width else ""
    size += f' height="{height}"' if height else ""
    p = (f'<picture><source media="(prefers-color-scheme: dark)" srcset="assets/{base}-dark.svg" />'
         f'<source media="(prefers-color-scheme: light)" srcset="assets/{base}-light.svg" />'
         f'<img src="assets/{base}-dark.svg"{size} alt="{alt}" /></picture>')
    return f'<a href="{href}">{p}</a>' if href else p


def out_dir(name):
    if name == MAIN:
        return os.path.join(ROOT, "assets")
    return os.path.join(ROOT, "variants", name, "assets")


def write_readme(name, body):
    path = os.path.join(ROOT, "README.md") if name == MAIN else os.path.join(ROOT, "variants", name, "README.md")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def pct(w, total=840):
    return "%.2f%%" % (w / total * 100 * 0.995)
