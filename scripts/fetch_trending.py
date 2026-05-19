#!/usr/bin/env python3
"""Fetch trending tech/business posts from Reddit + RSS feeds.

Prints a JSON object to stdout with a list of items. Each item has:
  title, url, source, score (nullable), summary
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

USER_AGENT = "linkedin-post-agent/0.1 (by /u/anonymous)"

REDDIT_SUBS = ["popular", "news", "worldnews", "business", "technology"]
RSS_FEEDS = [
    ("BBC", "https://feeds.bbci.co.uk/news/rss.xml"),
    ("NPR", "https://feeds.npr.org/1001/rss.xml"),
    ("Google News", "https://news.google.com/rss"),
    ("The Guardian", "https://www.theguardian.com/international/rss"),
    ("Hacker News", "https://hnrss.org/frontpage"),
]


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def fetch_reddit(sub, limit=8):
    url = f"https://www.reddit.com/r/{sub}/top.json?t=day&limit={limit}"
    try:
        data = json.loads(http_get(url))
    except Exception as e:
        print(f"warn: reddit {sub} failed: {e}", file=sys.stderr)
        return []
    items = []
    for child in data.get("data", {}).get("children", []):
        d = child.get("data", {})
        if d.get("stickied") or d.get("over_18"):
            continue
        title = (d.get("title") or "").strip()
        if not title:
            continue
        items.append({
            "title": title,
            "url": d.get("url_overridden_by_dest") or f"https://reddit.com{d.get('permalink', '')}",
            "source": f"r/{sub}",
            "score": d.get("score"),
            "summary": (d.get("selftext") or "")[:400].strip(),
        })
    return items


def _strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]


def fetch_rss(name, url, limit=8):
    try:
        body = http_get(url)
    except Exception as e:
        print(f"warn: rss {name} failed: {e}", file=sys.stderr)
        return []
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print(f"warn: rss {name} parse failed: {e}", file=sys.stderr)
        return []

    _strip_ns(root)
    items = []

    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()
        if title:
            items.append({
                "title": title,
                "url": link,
                "source": name,
                "score": None,
                "summary": desc[:400],
            })
        if len(items) >= limit:
            break

    if not items:
        for entry in root.iter("entry"):
            title = (entry.findtext("title") or "").strip()
            link_el = entry.find("link")
            link = link_el.get("href") if link_el is not None else ""
            summary = (entry.findtext("summary") or entry.findtext("content") or "").strip()
            if title:
                items.append({
                    "title": title,
                    "url": link,
                    "source": name,
                    "score": None,
                    "summary": summary[:400],
                })
            if len(items) >= limit:
                break

    return items


def main():
    all_items = []
    for sub in REDDIT_SUBS:
        all_items.extend(fetch_reddit(sub))
    for name, url in RSS_FEEDS:
        all_items.extend(fetch_rss(name, url))

    out = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(all_items),
        "items": all_items,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
