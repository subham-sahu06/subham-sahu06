"""Update the "Open Source Contributions" table in README.md.

Finds every pull request by USERNAME in repositories that USERNAME does not
own (so PRs into your own forks are skipped), keeps the ones that are open or
merged, and rewrites the table between the OSS-CONTRIBUTIONS markers in the
same style as the rest of the profile.

Your own wording for a PR can be kept in scripts/oss_overrides.json.
"""

import html
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

USERNAME = os.environ.get("GH_USERNAME", "subham-sahu06")
INCLUDE_OWNERS = {o.strip().lower() for o in os.environ.get("INCLUDE_OWNERS", "").split(",") if o.strip()}
ROOT = Path(__file__).resolve().parent.parent
README = ROOT / "README.md"
OVERRIDES = ROOT / "scripts" / "oss_overrides.json"
START = "<!-- OSS-CONTRIBUTIONS:START -->"
END = "<!-- OSS-CONTRIBUTIONS:END -->"

MERGED_BADGE = ('<img src="https://img.shields.io/badge/Merged-FE428E?style=flat-square'
                '&logo=github&logoColor=141321" alt="Merged" />')
OPEN_BADGE = ('<img src="https://img.shields.io/badge/In%20Review-141321?style=flat-square'
              '&logo=github&logoColor=F8D847" alt="In review" />')


def fetch_prs(token):
    query = f"author:{USERNAME} type:pr -user:{USERNAME}"
    items, page = [], 1
    while True:
        url = ("https://api.github.com/search/issues?"
               + urllib.parse.urlencode({"q": query, "per_page": 100, "page": page,
                                         "sort": "created", "order": "desc"}))
        req = urllib.request.Request(url, headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "oss-contributions-updater",
        })
        with urllib.request.urlopen(req) as resp:
            data = json.load(resp)
        items.extend(data.get("items", []))
        if len(items) >= data.get("total_count", 0) or not data.get("items") or page >= 10:
            return items
        page += 1


def to_rows(items, overrides):
    rows = []
    for it in items:
        repo = it["repository_url"].split("/repos/", 1)[1]  # owner/name
        owner, name = repo.split("/")
        if INCLUDE_OWNERS and owner.lower() not in INCLUDE_OWNERS:
            continue  # only show the organizations listed in INCLUDE_OWNERS
        number = it["number"]
        merged = bool((it.get("pull_request") or {}).get("merged_at"))
        if it["state"] == "closed" and not merged:
            continue  # closed without merge: don't show
        key = f"{repo}#{number}"
        ov = overrides.get(key, {})
        rows.append({
            "merged": merged,
            "created": it["created_at"],
            "org": ov.get("org", owner),
            "sub": ov.get("sub", ""),
            "link_text": f"{name} #{number}",
            "url": it["html_url"],
            "desc": ov.get("desc", html.escape(it["title"])),
        })
    # merged first, then newest first inside each group
    rows.sort(key=lambda r: r["created"], reverse=True)
    rows.sort(key=lambda r: not r["merged"])
    return rows


def render(rows):
    out = [START, "<table>", "<tr><th>Organization</th><th>Contribution</th><th>Status</th></tr>"]
    for r in rows:
        org = f"<b>{html.escape(r['org'])}</b>"
        if r["sub"]:
            org += f"<br/><sub>{html.escape(r['sub'])}</sub>"
        out += [
            "<tr>",
            f"<td>{org}</td>",
            f'<td><a href="{r["url"]}">{html.escape(r["link_text"])}</a>: {r["desc"]}</td>',
            f"<td>{MERGED_BADGE if r['merged'] else OPEN_BADGE}</td>",
            "</tr>",
        ]
    out += ["</table>", END]
    return "\n".join(out)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        sys.exit("GITHUB_TOKEN is not set")
    overrides = json.loads(OVERRIDES.read_text()) if OVERRIDES.exists() else {}
    rows = to_rows(fetch_prs(token), overrides)
    text = README.read_text()
    if START not in text or END not in text:
        sys.exit("Markers not found in README.md")
    before, rest = text.split(START, 1)
    _, after = rest.split(END, 1)
    new_text = before + render(rows) + after
    if new_text != text:
        README.write_text(new_text)
        print(f"README updated with {len(rows)} contributions")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
