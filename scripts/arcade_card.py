"""Build assets/arcade.svg: the contribution calendar of the last year as an arcade game screen."""
import json
import os
import sys
import urllib.request
from datetime import date, timedelta

USER = os.environ.get("ARCADE_USER", "subham-sahu06")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("ARCADE_OUT", "assets/arcade.svg")
DATA = os.environ.get("ARCADE_DATA", "")

BG, FRAME, PINK, CYAN, YELLOW, DIM = "#0d1117", "#39d353", "#39d353", "#7ee787", "#26a641", "#21262d"
LEVELS = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]


def fetch():
    if DATA:
        return json.load(open(DATA))
    query = """
    query($login:String!) {
      user(login:$login) {
        contributionsCollection {
          contributionCalendar {
            totalContributions
            weeks { contributionDays { date contributionCount contributionLevel } }
          }
        }
      }
    }"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": query, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        body = json.load(resp)
    if "errors" in body:
        sys.exit(f"GraphQL error: {body['errors']}")
    return body["data"]["user"]["contributionsCollection"]["contributionCalendar"]


LEVEL_INDEX = {"NONE": 0, "FIRST_QUARTILE": 1, "SECOND_QUARTILE": 2, "THIRD_QUARTILE": 3, "FOURTH_QUARTILE": 4}


def stats(weeks):
    days = [d for w in weeks for d in w["contributionDays"]]
    days.sort(key=lambda d: d["date"])
    counts = {date.fromisoformat(d["date"]): d["contributionCount"] for d in days}
    today = max(counts)
    end = today if counts[today] > 0 else today - timedelta(days=1)
    combo, d = 0, end
    while counts.get(d, 0) > 0:
        combo += 1
        d -= timedelta(days=1)
    last30 = [counts.get(today - timedelta(days=i), 0) for i in range(30)]
    shields = round(100 * sum(1 for c in last30 if c > 0) / 30)
    best = max(counts.values()) if counts else 0
    return combo, shields, best


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(cal):
    weeks = cal["weeks"]
    total = cal["totalContributions"]
    combo, shields, best = stats(weeks)
    level = total // 25 + 1

    cell, gap = 11, 3
    step = cell + gap
    gx, gy = 70, 72
    ncols = len(weeks)
    width = gx + ncols * step + 40
    gridw = ncols * step
    height = 250

    out = []
    a = out.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(USER)} contributions in the last year as an arcade game">')
    a("<style>")
    a(".t{font-family:'Courier New',Consolas,monospace;font-weight:700}")
    a("@keyframes tw{0%,100%{opacity:.15}50%{opacity:.9}}.s{animation:tw 3s ease-in-out infinite}")
    a("@keyframes fly{0%{transform:translateX(0)}50%{transform:translateX(" + str(gridw - 20) + "px)}100%{transform:translateX(0)}}")
    a(".ship{animation:fly 14s ease-in-out infinite}")
    a("@keyframes shot{0%{transform:translateY(0);opacity:1}80%{opacity:1}100%{transform:translateY(-120px);opacity:0}}")
    a(".laser{animation:shot 1.4s linear infinite}")
    a("@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:.2}}.b{animation:blink 1.2s step-end infinite}")
    a("@keyframes scan{0%{transform:translateY(0)}100%{transform:translateY(" + str(height - 40) + "px)}}.scan{animation:scan 4s linear infinite}")
    a("</style>")
    a(f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="12" fill="{BG}" stroke="{FRAME}" stroke-width="1.5"/>')
    a(f'<rect x="8" y="8" width="{width-16}" height="{height-16}" rx="8" fill="none" stroke="{DIM}" stroke-width="1"/>')

    stars = [(30, 120), (120, 205), (330, 56), (510, 215), (640, 204), (width - 18, 120), (22, 170), (430, 206), (790, 210), (width - 40, 205)]
    for i, (x, y) in enumerate(stars):
        if x < width - 10:
            a(f'<circle class="s" cx="{x}" cy="{y}" r="1.2" fill="{CYAN}" style="animation-delay:{i*0.4:.1f}s"/>')

    a(f'<text class="t" x="24" y="34" font-size="11" fill="{YELLOW}">SCORE: {total:,}</text>')
    a(f'<text class="t" x="{width*0.30:.0f}" y="34" font-size="11" fill="{CYAN}">RANK: LVL {level} · OPEN SOURCE PILOT</text>')
    a(f'<text class="t" x="{width*0.64:.0f}" y="34" font-size="11" fill="{PINK}">COMBO: x{combo} DAYS</text>')
    a(f'<text class="t" x="{width-150}" y="34" font-size="11" fill="{CYAN}">SHIELDS: {shields}%</text>')
    bars = round(shields / 10)
    for i in range(10):
        a(f'<rect x="{width-58+i*4}" y="26" width="3" height="9" fill="{CYAN if i < bars else DIM}"/>')
    a(f'<line x1="20" y1="44" x2="{width-20}" y2="44" stroke="{DIM}"/>')

    last_month = None
    for i, w in enumerate(weeks):
        first = date.fromisoformat(w["contributionDays"][0]["date"])
        if first.month != last_month and first.day <= 7:
            a(f'<text class="t" x="{gx + i*step}" y="{gy-8}" font-size="8" fill="#8b949e">{first.strftime("%b").upper()}</text>')
            last_month = first.month
    for r, name in ((1, "MON"), (3, "WED"), (5, "FRI")):
        a(f'<text class="t" x="{gx-34}" y="{gy + r*step + 9}" font-size="8" fill="#8b949e">{name}</text>')

    for i, w in enumerate(weeks):
        for d in w["contributionDays"]:
            r = date.fromisoformat(d["date"]).isoweekday() % 7
            lv = LEVEL_INDEX.get(d.get("contributionLevel", "NONE"), 0)
            a(f'<rect x="{gx + i*step}" y="{gy + r*step}" width="{cell}" height="{cell}" rx="2" fill="{LEVELS[lv]}"><title>{d["date"]}: {d["contributionCount"]}</title></rect>')

    a(f'<rect class="scan" x="12" y="20" width="{width-24}" height="2" fill="{CYAN}" opacity=".07"/>')

    sy = gy + 7 * step + 34
    a(f'<g class="ship" transform="translate(0,0)"><g transform="translate({gx+6},{sy}) scale(1.5)">')
    a(f'<rect class="laser" x="-1" y="-22" width="2" height="10" fill="{YELLOW}"/>')
    a(f'<path d="M0,-12 L7,6 L0,2 L-7,6 Z" fill="{PINK}"/>')
    a(f'<path d="M-3,6 L0,12 L3,6 Z" fill="{YELLOW}" class="b"/>')
    a("</g></g>")

    fy = height - 18
    a(f'<text class="t" x="24" y="{fy}" font-size="8" fill="#8b949e">POWER: LOW</text>')
    for i, c in enumerate(LEVELS):
        a(f'<rect x="{82 + i*13}" y="{fy-8}" width="10" height="10" rx="2" fill="{c}"/>')
    a(f'<text class="t" x="{82 + 5*13 + 4}" y="{fy}" font-size="8" fill="#8b949e">OVERDRIVE</text>')
    a(f'<text class="t" x="{width-24}" y="{fy}" font-size="8" fill="#8b949e" text-anchor="end">BEST DAY: {best} · SECTOR: {esc(USER.upper())}</text>')
    a("</svg>")
    return "\n".join(out)


if __name__ == "__main__":
    svg = build(fetch())
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"wrote {OUT}")
