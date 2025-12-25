#!/usr/bin/env python3
"""Generate an RSS 2.0 feed.xml from items.json (simple starter).

Usage:
  python make_rss.py

Output:
  feed.xml in the current directory.
"""

import json
import datetime
from email.utils import format_datetime
from pathlib import Path
from xml.sax.saxutils import escape

def parse_dt(value: str) -> datetime.datetime:
    # Accept ISO 8601 strings, with or without timezone.
    # If timezone missing, assume UTC.
    dt = datetime.datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt.astimezone(datetime.timezone.utc)

def cdata(html: str) -> str:
    # Basic CDATA wrapper; avoids breaking RSS when HTML contains entities.
    # NOTE: If your HTML can include ']]>' you'll need a more robust split.
    return f"<![CDATA[{html}]]>"

def main() -> None:
    p = Path(__file__).with_name("items.json")
    data = json.loads(p.read_text(encoding="utf-8"))

    now = datetime.datetime.now(datetime.timezone.utc)
    title = data.get("title", "Untitled Feed")
    link = data.get("link", "")
    desc = data.get("description", "")
    self_url = data.get("self_url", "")
    language = data.get("language", "en")

    items = data.get("items", [])
    # Sort newest first when possible
    def sort_key(it):
        published = it.get("published") or it.get("pubDate") or ""
        try:
            return parse_dt(published)
        except Exception:
            return datetime.datetime(1970,1,1,tzinfo=datetime.timezone.utc)
    items = sorted(items, key=sort_key, reverse=True)

    parts = []
    parts.append('<?xml version="1.0" encoding="UTF-8"?>')
    parts.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    parts.append("  <channel>")
    parts.append(f"    <title>{escape(title)}</title>")
    if link:
        parts.append(f"    <link>{escape(link)}</link>")
    parts.append(f"    <description>{escape(desc)}</description>")
    parts.append(f"    <language>{escape(language)}</language>")
    parts.append(f"    <lastBuildDate>{format_datetime(now)}</lastBuildDate>")
    if self_url:
        parts.append(f'    <atom:link href="{escape(self_url)}" rel="self" type="application/rss+xml" />')

    for it in items:
        it_title = it.get("title", "Untitled")
        it_link = it.get("link", "")
        it_guid = it.get("guid") or it_link
        published = it.get("published") or it.get("pubDate") or now.isoformat()
        try:
            pub_dt = parse_dt(published)
        except Exception:
            pub_dt = now
        description_html = it.get("description_html") or it.get("description") or ""

        parts.append("    <item>")
        parts.append(f"      <title>{escape(it_title)}</title>")
        if it_link:
            parts.append(f"      <link>{escape(it_link)}</link>")
        if it_guid:
            # Treat as permalink if it looks like a URL
            is_permalink = "true" if it_guid.startswith("http") else "false"
            parts.append(f'      <guid isPermaLink="{is_permalink}">{escape(it_guid)}</guid>')
        parts.append(f"      <pubDate>{format_datetime(pub_dt)}</pubDate>")
        if description_html:
            parts.append(f"      <description>{cdata(description_html)}</description>")
        parts.append("    </item>")

    parts.append("  </channel>")
    parts.append("</rss>")

    out = Path(__file__).with_name("feed.xml")
    out.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"Wrote {out}")

if __name__ == "__main__":
    main()
