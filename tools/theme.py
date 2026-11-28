"""Sistem visual bersama untuk semua aset profil.

Semua SVG memakai palet, tipografi, dan helper yang sama supaya README
terasa satu kesatuan. Font di-embed sebagai woff2 base64 (subset ASCII),
jadi tampilan konsisten di semua perangkat tanpa bergantung font sistem.
"""

import base64
import io
import json
import os
import re
from xml.sax.saxutils import escape, unescape

try:  # subset per-SVG kalau fontTools tersedia, kalau tidak embed font utuh
    from fontTools import subset as _subset
    from fontTools.ttLib import TTFont as _TTFont
except ImportError:  # pragma: no cover
    _subset = None

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "assets")
FONT_DIR = os.path.join(HERE, "fonts")

THEMES = {
    "dark": {
        "mode": "dark",
        "panel": "#110E22",
        "panel2": "#171331",
        "line": "#272249",
        "line2": "#373163",
        "text": "#EEF0FF",
        "muted": "#A7A4CF",
        "faint": "#6C6899",
        "accent": "#22D3EE",
        "amber": "#C084FC",
        "green": "#34D399",
        "violet": "#A855F7",
        "dot": "#272249",
    },
    "light": {
        "mode": "light",
        "panel": "#FCFBFF",
        "panel2": "#F4F2FE",
        "line": "#E5E1F8",
        "line2": "#D6D0F3",
        "text": "#19142F",
        "muted": "#575279",
        "faint": "#9893BA",
        "accent": "#0891B2",
        "amber": "#9333EA",
        "green": "#059669",
        "violet": "#7C3AED",
        "dot": "#E5E1F8",
    },
}

# kunci font -> (family css, weight)
FACES = {
    "display-500": ("D", 500),
    "display-600": ("D", 600),
    "sans-400": ("S", 400),
    "sans-500": ("S", 500),
    "mono-400": ("M", 400),
    "mono-500": ("M", 500),
    "black-900": ("B", 900),
}

with open(os.path.join(FONT_DIR, "metrics.json"), encoding="utf-8") as _f:
    METRICS = json.load(_f)

_font_cache = {}


def _font_b64(key, chars=None):
    ck = (key, "".join(sorted(chars)) if chars else None)
    if ck not in _font_cache:
        path = os.path.join(FONT_DIR, key + ".woff2")
        if chars and _subset is not None:
            font = _TTFont(path)
            opts = _subset.Options()
            opts.flavor = "woff2"
            opts.layout_features = ["kern"]
            opts.name_IDs = []
            sub = _subset.Subsetter(opts)
            sub.populate(text="".join(chars))
            sub.subset(font)
            buf = io.BytesIO()
            font.flavor = "woff2"
            font.save(buf)
            raw = buf.getvalue()
        else:
            with open(path, "rb") as f:
                raw = f.read()
        _font_cache[ck] = base64.b64encode(raw).decode()
    return _font_cache[ck]


_TEXT_RE = re.compile(r'<text [^>]*class="([dsmb])" font-size="[^"]*" font-weight="(\d+)"[^>]*>(.*?)</text>', re.S)
_FAM_KEY = {"d": "display", "s": "sans", "m": "mono", "b": "black"}


def used_chars(body):
    """Kumpulkan karakter yang benar-benar dipakai per font dari isi SVG."""
    used = {}
    for cls, weight, content in _TEXT_RE.findall(body):
        key = "%s-%s" % (_FAM_KEY[cls], weight)
        used.setdefault(key, set()).update(unescape(re.sub(r"<[^>]+>", "", content)))
    return used


def font_css(keys, used=None):
    rules = []
    for key in sorted(set(keys)):
        chars = (used or {}).get(key)
        if used is not None and not chars:
            continue  # font tidak terpakai di SVG ini
        fam, weight = FACES[key]
        rules.append(
            "@font-face{font-family:%s;font-weight:%d;font-style:normal;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}" % (fam, weight, _font_b64(key, chars))
        )
    rules.append(".d{font-family:D,'Space Grotesk',Inter,system-ui,sans-serif}"
                 ".s{font-family:S,Inter,system-ui,sans-serif}"
                 ".m{font-family:M,'JetBrains Mono',ui-monospace,monospace}"
                 ".b{font-family:B,'Inter Display',Inter,system-ui,sans-serif}")
    return "".join(rules)


def measure(text, key, size, spacing=0.0):
    table = METRICS[key]
    w = sum(table.get(ch, 0.6) for ch in text) * size
    return w + spacing * max(len(text) - 1, 0)


def wrap(text, key, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if cur and measure(trial, key, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def fmt(v):
    s = "%.2f" % v
    return s.rstrip("0").rstrip(".") if "." in s else s


def kt(*vals):
    """keyTimes presisi 6 desimal, wajib naik monoton dan diawali 0 diakhiri 1."""
    out = []
    for v in vals:
        v = min(max(v, 0.0), 1.0)
        if out and v <= out[-1]:
            v = out[-1] + 0.000001
        out.append(round(v, 6))
    assert out[0] == 0 and out[-1] == 1, out
    return ";".join("%.6f" % v for v in out)


def text(x, y, s, cls, key, size, fill, anchor=None, spacing=None, extra=""):
    fam, weight = FACES[key]
    attrs = [f'x="{fmt(x)}"', f'y="{fmt(y)}"', f'class="{cls}"', f'font-size="{fmt(size)}"',
             f'font-weight="{weight}"', f'fill="{fill}"']
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if spacing:
        attrs.append(f'letter-spacing="{fmt(spacing)}"')
    if extra:
        attrs.append(extra)
    return f'<text {" ".join(attrs)}>{escape(s)}</text>'


def doc(w, h, body, fonts, label, css="", transparent=False, t=None):
    """Bungkus isi menjadi dokumen SVG lengkap dengan font yang dibutuhkan."""
    bg = ""
    if not transparent:
        bg = (f'<rect x="0.5" y="0.5" width="{fmt(w - 1)}" height="{fmt(h - 1)}" rx="14" '
              f'fill="{t["panel"]}" stroke="{t["line"]}"/>')
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {fmt(w)} {fmt(h)}" '
        f'width="{fmt(w)}" height="{fmt(h)}" role="img" aria-label="{escape(label)}">'
        f"<title>{escape(label)}</title>"
        f"<style>{font_css(fonts, used_chars(body))}{css}</style>"
        f"{bg}{body}</svg>\n"
    )


def write(name, content, out=None):
    out = out or OUT
    os.makedirs(out, exist_ok=True)
    path = os.path.join(out, name)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path, len(content.encode())
