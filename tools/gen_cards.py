#!/usr/bin/env python3
"""Kartu statistik GitHub yang di-host sendiri (dark + light).

Data ditarik lewat GitHub GraphQL memakai GITHUB_TOKEN bawaan Actions lalu
disimpan ke assets/stats.json. Tanpa token, kartu dirender ulang dari
stats.json yang terakhir tersimpan, jadi desain tetap bisa diubah lokal.

Pakai:  GITHUB_TOKEN=xxx python3 tools/gen_cards.py [username]
"""

import json
import os
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import OUT, THEMES, doc, fmt, measure, text, write  # noqa: E402

QUERY = """
query($login:String!){
  user(login:$login){
    followers{totalCount}
    repositories(first:100, ownerAffiliations:OWNER, isFork:false, privacy:PUBLIC,
                 orderBy:{field:STARGAZERS, direction:DESC}){
      totalCount
      nodes{
        stargazerCount
        forkCount
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){
          edges{ size node{ name color } }
        }
      }
    }
    contributionsCollection{
      totalCommitContributions
      totalPullRequestContributions
      totalIssueContributions
      restrictedContributionsCount
      contributionCalendar{ weeks{ contributionDays{ contributionLevel } } }
    }
  }
}
"""

DATA = os.path.join(OUT, "stats.json")
LEVEL = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}
ISO = os.path.join(os.path.dirname(OUT), "variants", "iso", "assets")  # kartu gaya iso


def fetch(login, token):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": login}}).encode(),
        headers={"Authorization": "bearer " + token, "Content-Type": "application/json",
                 "User-Agent": "profile-card-generator"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        payload = json.load(r)
    if "errors" in payload:
        raise RuntimeError(payload["errors"])
    return payload["data"]["user"]


def summarize(user):
    repos = user["repositories"]["nodes"]
    c = user["contributionsCollection"]
    langs = {}
    for r in repos:
        for e in r["languages"]["edges"]:
            n = e["node"]["name"]
            langs.setdefault(n, [0, e["node"]["color"] or "#8B96A5"])
            langs[n][0] += e["size"]
    top = sorted(langs.items(), key=lambda kv: -kv[1][0])[:6]
    total = sum(v[0] for _, v in top) or 1
    return {
        "metrics": {
            "contributions": c["totalCommitContributions"] + c["restrictedContributionsCount"],
            "pull_requests": c["totalPullRequestContributions"],
            "repositories": user["repositories"]["totalCount"],
            "stars": sum(r["stargazerCount"] for r in repos),
            "followers": user["followers"]["totalCount"],
            "issues": c["totalIssueContributions"],
            "forks": sum(r["forkCount"] for r in repos),
        },
        # level harian 0-4, urut dari hari terlama; dipakai untuk streak dan hari aktif
        "calendar": [LEVEL[d["contributionLevel"]] for w in c["contributionCalendar"]["weeks"]
                     for d in w["contributionDays"]],
        "languages": [[n, round(v[0] / total, 4), v[1]] for n, v in top],
    }


def render(data, t):
    W, H = 840, 150
    m = data["metrics"]
    b = []
    # satu kalimat, angka di dalam kalimat (bukan deretan angka berlabel)
    runs = [
        ("{:,}".format(m["contributions"]), "sans-500", t["text"]),
        (" contributions in the past year across ", "sans-400", t["muted"]),
        ("{:,}".format(m["repositories"]), "sans-500", t["text"]),
        (" public repositories.", "sans-400", t["muted"]),
    ]
    spans = "".join(
        f'<tspan font-weight="{500 if key == "sans-500" else 400}" fill="{col}">{s_}</tspan>' for s_, key, col in runs
    )
    b.append(f'<text x="28" y="50" class="s" font-size="15" xml:space="preserve">{spans}</text>')
    # pastikan glyph kalimat ikut ter-subset: teks bayangan tak terlihat
    for s_, key, col in runs:
        b.append(text(0, -10, s_, "s", key, 1, "none"))

    bx, bw, by = 28.0, W - 56.0, 76
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="8" rx="4" fill="{t["panel2"]}"/>')
    b.append(f'<clipPath id="bar"><rect x="{bx}" y="{by}" width="{bw}" height="8" rx="4"/></clipPath><g clip-path="url(#bar)">')
    x = bx
    langs = data["languages"]
    for i, (name, share, color) in enumerate(langs):
        w = max(bw * share - 2, 0)
        b.append(
            f'<rect x="{fmt(x)}" y="{by}" width="{fmt(w)}" height="8" fill="{color}">'
            f'<animate attributeName="width" from="0" to="{fmt(w)}" dur="0.9s" begin="{0.2 + i * 0.1:.2f}s" '
            f'fill="freeze" calcMode="spline" keyTimes="0;1" keySplines="0.45 0 0.2 1"/></rect>'
        )
        x += bw * share
    b.append("</g>")
    lx = 28.0
    for name, share, color in langs:
        pct = "%.0f%%" % (share * 100)
        b.append(f'<circle cx="{fmt(lx + 4)}" cy="{110.5}" r="4" fill="{color}"/>')
        b.append(text(lx + 14, 115, name, "s", "sans-500", 12.5, t["text"]))
        px = lx + 14 + measure(name, "sans-500", 12.5) + 6
        b.append(text(px, 115, pct, "s", "sans-400", 12.5, t["faint"]))
        lx = px + measure(pct, "sans-400", 12.5) + 22
    assert lx < W, lx
    return doc(W, H, "".join(b), {"sans-500", "sans-400"},
               "%d contributions in the past year across %d public repositories" % (m["contributions"], m["repositories"]), t=t)


def main():
    login = sys.argv[1] if len(sys.argv) > 1 else "AtokTajuddin"
    token = os.environ.get("GITHUB_TOKEN", "")
    data = None
    if token:
        try:
            data = summarize(fetch(login, token))
            with open(DATA, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
        except Exception as exc:  # noqa: BLE001
            print("gagal ambil data (%s), pakai stats.json terakhir" % exc)
    if data is None:
        if not os.path.exists(DATA):
            print("stats.json belum ada dan tidak ada token, lewati")
            return 0
        with open(DATA, encoding="utf-8") as f:
            data = json.load(f)
    for mode, t in THEMES.items():
        path, size = write(f"stats-{mode}.svg", render(data, t), ISO)
        print("%-20s %6d bytes" % (os.path.basename(path), size))
    return 0


if __name__ == "__main__":
    sys.exit(main())
