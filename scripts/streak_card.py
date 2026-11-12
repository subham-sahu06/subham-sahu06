"""Build assets/streak.svg (contribution streak card) from the GitHub GraphQL API."""
import json
import os
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone

USER = os.environ.get("STREAK_USER", "subham-sahu06")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("STREAK_OUT", "assets/streak.svg")

# "radical" colours, same as the other cards in the README.
BG, RING, FIRE = "#141321", "#fe428e", "#fe428e"
NUM, LABEL, DATES, STROKE = "#fe428e", "#a9fef7", "#f8d847", "#e4e2e2"


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


def fetch_days():
    created = graphql(
        "query($login:String!){user(login:$login){createdAt}}", {"login": USER}
    )["user"]["createdAt"]
    first_year = int(created[:4])
    today = datetime.now(timezone.utc).date()
    query = """
    query($login:String!, $from:DateTime!, $to:DateTime!) {
      user(login:$login) {
        contributionsCollection(from:$from, to:$to) {
          contributionCalendar { weeks { contributionDays { date contributionCount } } }
        }
      }
    }"""
    days = {}
    for year in range(first_year, today.year + 1):
        data = graphql(query, {
            "login": USER,
            "from": f"{year}-01-01T00:00:00Z",
            "to": f"{year}-12-31T23:59:59Z",
        })
        weeks = data["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
        for week in weeks:
            for d in week["contributionDays"]:
                day = date.fromisoformat(d["date"])
                if day <= today:
                    days[day] = d["contributionCount"]
    return days, today


def streaks(days, today):
    ordered = sorted(days)
    total = sum(days.values())
    first = next((d for d in ordered if days[d] > 0), today)

    longest = (0, None, None)
    run_start, run_len = None, 0
    for d in ordered:
        if days[d] > 0:
            if run_len == 0:
                run_start = d
            run_len += 1
            if run_len > longest[0]:
                longest = (run_len, run_start, d)
        else:
            run_len = 0

    # Current streak: today without contributions does not break it yet.
    end = today if days.get(today, 0) > 0 else today - timedelta(days=1)
    current, d = 0, end
    while days.get(d, 0) > 0:
        current += 1
        d -= timedelta(days=1)
    current_range = (d + timedelta(days=1), end) if current else (None, None)
    return total, first, current, current_range, longest


def fmt(d, today):
    if d is None:
        return ""
    return d.strftime("%b %-d") if d.year == today.year else d.strftime("%b %-d, %Y")


def span(a, b, today):
    if a is None:
        return ""
    return fmt(a, today) if a == b else f"{fmt(a, today)} - {fmt(b, today)}"


def render(total, first, current, cur_range, longest, today):
    total_range = f"{fmt(first, today)} - Present"
    cur_text = span(cur_range[0], cur_range[1], today)
    long_text = span(longest[1], longest[2], today)
    font = "font-family='Segoe UI, Ubuntu, sans-serif'"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="195" viewBox="0 0 495 195">
  <style>
    .fade {{ opacity: 0; animation: fadein 0.6s ease-in-out forwards; }}
    .d1 {{ animation-delay: 0.3s; }} .d2 {{ animation-delay: 0.6s; }} .d3 {{ animation-delay: 0.9s; }}
    .ring {{ stroke-dasharray: 252; stroke-dashoffset: 252; animation: draw 1.2s ease-in-out 0.4s forwards; }}
    .fire {{ opacity: 0; animation: fadein 0.5s ease-in-out 1.4s forwards; }}
    @keyframes fadein {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
    @keyframes draw {{ to {{ stroke-dashoffset: 0; }} }}
  </style>
  <rect x="0.5" y="0.5" width="494" height="194" rx="4.5" fill="{BG}" stroke="{STROKE}" stroke-opacity="1"/>
  <line x1="165" y1="28" x2="165" y2="170" stroke="{STROKE}" stroke-width="1"/>
  <line x1="330" y1="28" x2="330" y2="170" stroke="{STROKE}" stroke-width="1"/>
  <g {font} text-anchor="middle">
    <g class="fade d1">
      <text x="82.5" y="79" fill="{NUM}" font-size="28" font-weight="700">{total:,}</text>
      <text x="82.5" y="115" fill="{LABEL}" font-size="14">Total Contributions</text>
      <text x="82.5" y="145" fill="{DATES}" font-size="12">{total_range}</text>
    </g>
    <circle class="ring" cx="247.5" cy="71" r="40" fill="none" stroke="{RING}" stroke-width="5" transform="rotate(-90 247.5 71)"/>
    <path class="fire" d="M247.5 19 c4 6 9 9 9 15 a9 9 0 0 1 -18 0 c0 -4 3 -6 4 -9 c1 3 3 4 4 4 c1 -3 0 -6 1 -10z" fill="{FIRE}" stroke="{BG}" stroke-width="3"/>
    <g class="fade d2">
      <text x="247.5" y="80" fill="{NUM}" font-size="28" font-weight="700">{current}</text>
      <text x="247.5" y="140" fill="{LABEL}" font-size="14" font-weight="700">Current Streak</text>
      <text x="247.5" y="166" fill="{DATES}" font-size="12">{cur_text}</text>
    </g>
    <g class="fade d3">
      <text x="412.5" y="79" fill="{NUM}" font-size="28" font-weight="700">{longest[0]}</text>
      <text x="412.5" y="115" fill="{LABEL}" font-size="14">Longest Streak</text>
      <text x="412.5" y="145" fill="{DATES}" font-size="12">{long_text}</text>
    </g>
  </g>
</svg>
"""


def main():
    if not TOKEN:
        sys.exit("GITHUB_TOKEN is not set")
    days, today = fetch_days()
    svg = render(*streaks(days, today), today)
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
