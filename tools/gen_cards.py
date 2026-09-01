#!/usr/bin/env python3
"""Kartu statistik GitHub yang di-host sendiri.

Alasan ada file ini: github-readme-stats & activity-graph di Vercel sering kena
kuota (503 / 402 Payment Required) sehingga README menampilkan gambar rusak.
Script ini menarik data lewat GitHub GraphQL API memakai GITHUB_TOKEN bawaan
Actions, lalu merender assets/stats.svg sendiri. Tanpa token, file lama
dipertahankan dan hanya placeholder yang dibuat kalau belum ada.

Pakai:  GITHUB_TOKEN=xxx python3 tools/gen_cards.py [username]
"""

import json
import os
import sys
import urllib.request
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gen_svg import GREEN, GREEN_SOFT, GREEN_DIM, CARD, MONO, NEON, fmt, OUT  # noqa: E402

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    repositories(first:100, ownerAffiliations:OWNER, isFork:false,
                 orderBy:{field:STARGAZERS, direction:DESC}){
      totalCount
      nodes{
        name stargazerCount forkCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){
          edges{ size node{ name color } }
        }
      }
    }
    contributionsCollection{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
    }
  }
}
"""


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": "bearer " + token,
                 "Content-Type": "application/json",
                 "User-Agent": "profile-card-generator"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def summarize(user):
    repos = user["repositories"]["nodes"]
    stars = sum(r["stargazerCount"] for r in repos)
    forks = sum(r["forkCount"] for r in repos)
    contrib = user["contributionsCollection"]

    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or GREEN])
            langs[n][0] += e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    total = sum(v[0] for _, v in top) or 1

    return {
        "stats": [
            ("commits (1y)", contrib["totalCommitContributions"]),
            ("pull requests", contrib["totalPullRequestContributions"]),
            ("issues", contrib["totalIssueContributions"]),
            ("stars earned", stars),
            ("forks", forks),
            ("public repos", user["repositories"]["totalCount"]),
            ("followers", user["followers"]["totalCount"]),
        ],
        "langs": [(n, v[0] / total, v[1]) for n, v in top],
    }


def render(data, login):
    W = 900
    rows = data["stats"]
    top = 74.0
    RH = 30.0
    H = top + RH * len(rows) + 18
    LX, LW = 470.0, 400.0     # kolom kanan: komposisi bahasa

    out = []
    for i, (label, value) in enumerate(rows):
        y = top + i * RH
        out.append(
            f'  <g>\n'
            f'    <circle cx="30" cy="{fmt(y - 5)}" r="3" fill="{NEON["a"] if i % 2 == 0 else NEON["b"]}">\n'
            f'      <animate attributeName="opacity" dur="2.6s" begin="-{round(i * 0.4, 2)}s" repeatCount="indefinite" values="0.25;1;0.25"/>\n'
            f'    </circle>\n'
            f'    <text x="46" y="{fmt(y)}" font-size="14" fill="{GREEN_SOFT}">{escape(label)}</text>\n'
            f'    <text x="420" y="{fmt(y)}" font-size="15" font-weight="700" text-anchor="end" fill="{GREEN}">{value}</text>\n'
            f'    <line x1="46" y1="{fmt(y + 9)}" x2="420" y2="{fmt(y + 9)}" stroke="{GREEN}" stroke-opacity="0.10"/>\n'
            f'  </g>'
        )

    # bar bahasa: tiap segmen tumbuh dari 0 dengan jeda berurutan
    segs, legend, x = [], [], LX
    by = top + 40
    for i, (name, share, color) in enumerate(data["langs"]):
        w = LW * share
        segs.append(
            f'  <rect x="{fmt(x)}" y="{fmt(by)}" width="0" height="16" fill="{color}" opacity="0.92">\n'
            f'    <animate attributeName="width" dur="1.1s" begin="{round(0.15 * i, 2)}s" fill="freeze"\n'
            f'             values="0;{fmt(w)}" calcMode="spline" keySplines="0.2 0 0.1 1"/>\n'
            f'  </rect>'
        )
        lx = LX + (i % 2) * 200
        ly = by + 46 + (i // 2) * 26
        legend.append(
            f'  <g><rect x="{fmt(lx)}" y="{fmt(ly - 9)}" width="10" height="10" rx="2" fill="{color}"/>'
            f'<text x="{fmt(lx + 18)}" y="{fmt(ly)}" font-size="12" fill="{GREEN_SOFT}">'
            f'{escape(name)} <tspan fill="{GREEN_DIM}">{share * 100:.1f}%</tspan></text></g>'
        )
        x += w

    H = max(H, by + 46 + ((len(data["langs"]) + 1) // 2) * 26 + 20)

    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {fmt(H)}" width="{W}" height="{fmt(H)}" font-family="{MONO}" role="img" aria-label="Statistik GitHub {escape(login)}">
  <title>github stats - {escape(login)}</title>
  <defs>
    <linearGradient id="hd" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{NEON['a']}"/><stop offset="0.5" stop-color="{NEON['b']}"/>
      <stop offset="1" stop-color="{NEON['c']}"/>
    </linearGradient>
  </defs>
  <rect width="{W}" height="{fmt(H)}" rx="14" fill="{CARD}"/>
  <rect x="0" y="0" width="{W}" height="3" rx="1.5" fill="url(#hd)"/>
  <text x="30" y="40" font-size="15" font-weight="700" fill="{GREEN}">{escape(login)} :: metrics</text>
  <line x1="0" y1="52" x2="{W}" y2="52" stroke="{GREEN}" stroke-opacity="0.2"/>
  <text x="{fmt(LX)}" y="{fmt(top)}" font-size="13" fill="{GREEN_DIM}" letter-spacing="2">LANGUAGE MIX</text>
{chr(10).join(segs)}
{chr(10).join(legend)}
{chr(10).join(out)}
  <rect x="0.5" y="0.5" width="{W - 1}" height="{fmt(H - 1)}" rx="14" fill="none" stroke="{GREEN}" stroke-opacity="0.3"/>
</svg>
"""


PLACEHOLDER = {
    "stats": [("commits (1y)", "--"), ("pull requests", "--"), ("issues", "--"),
              ("stars earned", "--"), ("forks", "--"), ("public repos", "--"),
              ("followers", "--")],
    "langs": [("syncing", 1.0, "#0B7A2C")],
}


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "AtokTajuddin"
    token = os.environ.get("GITHUB_TOKEN", "")
    path = os.path.join(OUT, "stats.svg")

    if token:
        try:
            data = summarize(fetch(login, token))
        except Exception as exc:                      # noqa: BLE001
            print("gagal ambil data (%s) - file lama dipertahankan" % exc)
            return 1 if not os.path.exists(path) else 0
    else:
        if os.path.exists(path):
            print("tanpa GITHUB_TOKEN - assets/stats.svg dibiarkan apa adanya")
            return 0
        print("tanpa GITHUB_TOKEN - menulis placeholder")
        data = PLACEHOLDER

    os.makedirs(OUT, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(render(data, login))
    print("stats.svg %d bytes" % os.path.getsize(path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
