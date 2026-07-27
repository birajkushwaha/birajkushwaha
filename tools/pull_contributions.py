import json
from pathlib import Path

import httpx
from lxml import html

USERNAME = "birajkushwaha"

URL = f"https://github.com/users/{USERNAME}/contributions"

OUT = Path("assets/contributions.json")

print("Downloading contribution graph...")

response = httpx.get(
    URL,
    headers={
        "User-Agent": "Mozilla/5.0"
    },
    timeout=30
)

response.raise_for_status()

tree = html.fromstring(response.text)

# GitHub now stores contribution data in <td> elements
cells = tree.xpath("//td[@data-date]")

days = []

for cell in cells:

    days.append({
        "date": cell.attrib.get("data-date"),
        "level": int(cell.attrib.get("data-level", 0)),
        "count": int(cell.attrib.get("data-count", 0))
        if cell.attrib.get("data-count") is not None
        else 0
    })

OUT.parent.mkdir(parents=True, exist_ok=True)

OUT.write_text(
    json.dumps(days, indent=2),
    encoding="utf-8"
)

print(f"Saved {len(days)} days -> {OUT}")