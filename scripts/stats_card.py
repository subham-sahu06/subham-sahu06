"""Build assets/stats.svg and assets/langs.svg (animated, radical colours) from the GitHub GraphQL API."""
import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from html import escape

USER = os.environ.get("STATS_USER", "subham-sahu06")
NAME = os.environ.get("STATS_NAME", "Subham Sahu")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT_DIR = os.environ.get("STATS_OUT", "assets")

BG, BORDER, TITLE, TEXT, ICON = "#141321", "#e4e2e2", "#fe428e", "#a9fef7", "#f8d847"
FONT = "font-family='Segoe UI, Ubuntu, sans-serif'"

GITHUB_MARK = ("M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49"
               "-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 "
               "1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59"
               ".82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 "
               "1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 "
               "3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42"
               "-3.58-8-8-8z")

ICONS = {
    "star": "<path d='M8 .25l2.3 4.66 5.14.75-3.72 3.63.88 5.12L8 11.99l-4.6 2.42.88-5.12L.56 5.66l5.14-.75z' fill='{c}'/>",
    "commit": "<circle cx='8' cy='8' r='3' fill='none' stroke='{c}' stroke-width='1.6'/><path d='M0 8h5M11 8h5' stroke='{c}' stroke-width='1.6'/>",
    "pr": "<circle cx='4' cy='3' r='2' fill='none' stroke='{c}' stroke-width='1.5'/><circle cx='4' cy='13' r='2' fill='none' stroke='{c}' stroke-width='1.5'/><circle cx='12' cy='13' r='2' fill='none' stroke='{c}' stroke-width='1.5'/><path d='M4 5v6M12 11V6a2 2 0 0 0-2-2H7' fill='none' stroke='{c}' stroke-width='1.5'/>",
    "issue": "<circle cx='8' cy='8' r='6.5' fill='none' stroke='{c}' stroke-width='1.5'/><circle cx='8' cy='8' r='1.6' fill='{c}'/>",
    "repo": "<path d='M3 1.5h10v11H4.5A1.5 1.5 0 0 0 3 14V1.5zM3 14a1.5 1.5 0 0 0 1.5 1.5H13v-3' fill='none' stroke='{c}' stroke-width='1.5'/>",
}


def graphql(query, variables):
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]


def fetch():
    data = graphql("""
    query($login:String!) {
      user(login:$login) {
        createdAt
        pullRequests { totalCount }
        issues { totalCount }
        repositoriesContributedTo(contributionTypes:[COMMIT, ISSUE, PULL_REQUEST, REPOSITORY]) { totalCount }
        repositories(ownerAffiliations:OWNER, isFork:false, first:100) {
          nodes {
            stargazerCount
            languages(first:10, orderBy:{field:SIZE, direction:DESC}) { edges { size node { name color } } }
          }
        }
      }
    }""", {"login": USER})["user"]
    commits = 0
    first_year = int(data["createdAt"][:4])
    for year in range(first_year, datetime.now(timezone.utc).year + 1):
        c = graphql("""
        query($login:String!, $from:DateTime!, $to:DateTime!) {
          user(login:$login) { contributionsCollection(from:$from, to:$to) { totalCommitContributions } }
        }""", {"login": USER, "from": f"{year}-01-01T00:00:00Z", "to": f"{year}-12-31T23:59:59Z"})
        commits += c["user"]["contributionsCollection"]["totalCommitContributions"]
    stars = sum(r["stargazerCount"] for r in data["repositories"]["nodes"])
    langs = {}
    for repo in data["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            name = e["node"]["name"]
            size, color = langs.get(name, (0, e["node"]["color"] or "#888888"))
            langs[name] = (size + e["size"], color)
    stats = [
        ("star", "Total Stars", stars),
        ("commit", "Total Commits", commits),
        ("pr", "Total PRs", data["pullRequests"]["totalCount"]),
        ("issue", "Total Issues", data["issues"]["totalCount"]),
        ("repo", "Contributed to", data["repositoriesContributedTo"]["totalCount"]),
    ]
    return stats, langs


def short(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def stats_svg(stats):
    rows = []
    for i, (icon, label, value) in enumerate(stats):
        y = 70 + i * 25
        delay = 0.45 + i * 0.15
        rows.append(f"""    <g transform="translate(25,{y})"><g class="row" style="animation-delay:{delay:.2f}s">
      <svg x="0" y="-12" width="16" height="16" viewBox="0 0 16 16">{ICONS[icon].format(c=ICON)}</svg>
      <text x="25" y="0" fill="{TEXT}" font-size="14" font-weight="600">{label}:</text>
      <text x="160" y="0" fill="{TEXT}" font-size="14" font-weight="700">{short(value)}</text>
    </g></g>""")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="467" height="195" viewBox="0 0 467 195">
  <style>
    .title {{ opacity: 0; animation: fadein 0.6s ease-in-out forwards; }}
    .row {{ opacity: 0; animation: slidein 0.4s ease-in-out forwards; }}
    .mark {{ fill-opacity: 0; stroke-dasharray: 1; stroke-dashoffset: 1;
             animation: draw 1.6s ease-in-out 0.4s forwards, fill 0.8s ease-in-out 1.9s forwards; }}
    @keyframes fadein {{ to {{ opacity: 1; }} }}
    @keyframes slidein {{ from {{ opacity: 0; transform: translateX(-10px); }} to {{ opacity: 1; }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fill {{ to {{ fill-opacity: 1; }} }}
  </style>
  <rect x="0.5" y="0.5" width="466" height="194" rx="4.5" fill="{BG}" stroke="{BORDER}"/>
  <g {FONT}>
    <text class="title" x="25" y="38" fill="{TITLE}" font-size="20" font-weight="700">{escape(NAME)}'s GitHub Stats</text>
{chr(10).join(rows)}
  </g>
  <svg x="315" y="45" width="120" height="120" viewBox="-0.5 -0.5 17 17">
    <path class="mark" pathLength="1" d="{GITHUB_MARK}" fill="{TITLE}" stroke="{TITLE}" stroke-width="0.35"/>
  </svg>
</svg>
"""


def langs_svg(langs, top=6):
    items = sorted(langs.items(), key=lambda kv: -kv[1][0])[:top]
    total = sum(v[0] for _, v in items) or 1
    bar, x = [], 0.0
    for name, (size, color) in items:
        w = 300 * size / total
        bar.append(f'<rect x="{x:.2f}" y="0" width="{w:.2f}" height="8" fill="{color}"/>')
        x += w
    rows = []
    for i, (name, (size, color)) in enumerate(items):
        col, line = i % 2, i // 2
        delay = 0.6 + i * 0.12
        rows.append(f"""    <g class="row" style="animation-delay:{delay:.2f}s" transform="translate({25 + col * 150},{95 + line * 25})">
      <circle cx="5" cy="-5" r="5" fill="{color}"/>
      <text x="16" y="0" fill="{TEXT}" font-size="12">{escape(name)} {100 * size / total:.2f}%</text>
    </g>""")
    height = 95 + ((len(items) + 1) // 2) * 25
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="350" height="{height}" viewBox="0 0 350 {height}">
  <style>
    .title {{ opacity: 0; animation: fadein 0.6s ease-in-out forwards; }}
    .bar {{ animation: grow 1s ease-in-out 0.3s both; }}
    .row {{ opacity: 0; animation: fadein 0.4s ease-in-out forwards; }}
    @keyframes fadein {{ to {{ opacity: 1; }} }}
    @keyframes grow {{ from {{ transform: scaleX(0); }} to {{ transform: scaleX(1); }} }}
  </style>
  <rect x="0.5" y="0.5" width="349" height="{height - 1}" rx="4.5" fill="{BG}" stroke="{BORDER}"/>
  <g {FONT}>
    <text class="title" x="25" y="38" fill="{TITLE}" font-size="18" font-weight="700">Most Used Languages</text>
    <clipPath id="round"><rect x="0" y="0" width="300" height="8" rx="4"/></clipPath>
    <g transform="translate(25,58)"><g class="bar" clip-path="url(#round)">{''.join(bar)}</g></g>
{chr(10).join(rows)}
  </g>
</svg>
"""


def main():
    if not TOKEN:
        sys.exit("GITHUB_TOKEN is not set")
    stats, langs = fetch()
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "stats.svg"), "w") as f:
        f.write(stats_svg(stats))
    with open(os.path.join(OUT_DIR, "langs.svg"), "w") as f:
        f.write(langs_svg(langs))
    print("Wrote stats.svg and langs.svg")


if __name__ == "__main__":
    main()
