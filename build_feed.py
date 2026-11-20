"""Builds site/feed.xml (Pinterest RSS auto-publish) + site/index.html from pins.json.
Usage: python3 build_feed.py https://<user>.github.io/<repo>"""
import json, sys, os, html
from email.utils import format_datetime
from datetime import datetime, timezone
D = os.path.dirname(os.path.abspath(__file__)); base = sys.argv[1].rstrip("/")
now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
allpins = sorted([p for p in json.load(open(os.path.join(D, "pins.json"))) if p["added"] <= now], key=lambda p: p["added"], reverse=True)
OUTD = os.environ.get("FEED_OUT", os.path.join(D, "site"))
done = set(json.load(open(os.path.join(D, "csv_uploaded.json"))))  # already pinned via CSV, keep out of RSS to avoid duplicates
pins = [p for p in allpins if p["img"] not in done]
e = html.escape
items = []
for p in pins:
    url = f"{base}/{p['img']}"; dt = format_datetime(datetime.fromisoformat(p["added"].replace("Z", "+00:00")))
    items.append(f"""<item><title>{e(p['title'])}</title><link>{e(p['link'])}</link>
<description>{e(p['desc'])}</description><guid isPermaLink="false">{e(p['img'])}</guid><pubDate>{dt}</pubDate>
<enclosure url="{e(url)}" type="image/jpeg" length="0"/><media:content url="{e(url)}" medium="image" type="image/jpeg"/></item>""")
open(os.path.join(OUTD, "feed.xml"), "w").write(f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/"><channel>
<title>Savranne Studio</title><link>https://savranne.gumroad.com</link>
<description>3D print files, tattoo flash, T-shirt graphics and digital design assets by Savranne Studio.</description>
{''.join(items)}
</channel></rss>""")
cards = "".join(f'<a href="{e(p["link"])}"><img src="{e(p["img"])}" alt="{e(p["title"])}" loading="lazy"></a>' for p in allpins)
open(os.path.join(OUTD, "index.html"), "w").write(f"""<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="p:domain_verify" content="eba83c65fcf619c9b961a91070c22f1e"/><title>Savranne Studio</title><style>body{{margin:0;font-family:sans-serif;background:#f4efe6;color:#222}}h1{{padding:20px 16px 0}}
.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:12px;padding:16px}}img{{width:100%;border-radius:8px}}</style></head>
<body><h1>Savranne Studio</h1><p style="padding:0 16px">Digital design assets and 3D print files. Shop: <a href="https://savranne.gumroad.com">savranne.gumroad.com</a></p><div class="g">{cards}</div></body></html>""")
print(len(items), "items")
