#!/usr/bin/env python3
"""Fetch tech/AI news from credible RSS feeds, tagged by tier.

Tiers:
  first_party — AI labs / companies announcing their own work (highest signal)
  premium     — top-tier publishers and curated AI analysis
  general     — solid mainstream tech reporting

Outputs JSON to stdout. Each item:
  {tier, source, title, url, summary, published_at}

Items are sorted by tier (first_party first) and then by published_at desc.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

USER_AGENT = "Mozilla/5.0 (compatible; linkedin-post-agent/0.2)"

SOURCES = [
    ("first_party", "Anthropic",        "https://www.anthropic.com/news/rss.xml"),
    ("first_party", "OpenAI",           "https://openai.com/blog/rss.xml"),
    ("first_party", "DeepMind",         "https://deepmind.google/blog/rss.xml"),
    ("first_party", "Meta AI",          "https://ai.meta.com/blog/rss/"),
    ("first_party", "Hugging Face",     "https://huggingface.co/blog/feed.xml"),
    ("premium",     "MIT Tech Review",  "https://www.technologyreview.com/feed/"),
    ("premium",     "Reuters Tech",     "https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best&best-sectors=technology"),
    ("premium",     "The Batch",        "https://www.deeplearning.ai/the-batch/feed/"),
    ("general",     "Ars Technica",     "https://feeds.arstechnica.com/arstechnica/index"),
    ("general",     "The Verge",        "https://www.theverge.com/rss/index.xml"),
    ("general",     "404 Media",        "https://www.404media.co/rss/"),
    # Analyst notes: slower cadence, high CXO credibility, often synthesise
    # multiple stories into a single take. IDC has no public RSS — surface
    # via WebSearch in the cxo-tech-brief agent instead.
    ("analyst",     "Gartner Blogs",    "https://blogs.gartner.com/feed/"),
    ("analyst",     "Forrester Blogs",  "https://go.forrester.com/blogs/feed/"),
]


def http_get(url, timeout=15):
    req = urllib.request.Request(url, headers={
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/atom+xml, application/xml, text/xml, */*",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def _strip_ns(root):
    for el in root.iter():
        if isinstance(el.tag, str) and "}" in el.tag:
            el.tag = el.tag.split("}", 1)[1]


def parse_date(s):
    if not s:
        return None
    s = s.strip()
    if not s:
        return None
    try:
        dt = parsedate_to_datetime(s)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except (TypeError, ValueError):
        pass
    try:
        dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        return None


def fetch_rss(tier, name, url, limit=8):
    try:
        body = http_get(url)
    except Exception as e:
        print(f"warn: {name} fetch failed: {e}", file=sys.stderr)
        return []
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        print(f"warn: {name} parse failed: {e}", file=sys.stderr)
        return []
    _strip_ns(root)

    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()
        pub = parse_date(item.findtext("pubDate") or "")
        if title:
            items.append({
                "tier": tier,
                "source": name,
                "title": title,
                "url": link,
                "summary": desc[:500],
                "published_at": pub,
            })
        if len(items) >= limit:
            break

    if not items:
        for entry in root.iter("entry"):
            title = (entry.findtext("title") or "").strip()
            link_el = entry.find("link")
            link = link_el.get("href") if link_el is not None else ""
            summary = (entry.findtext("summary") or entry.findtext("content") or "").strip()
            pub = parse_date(entry.findtext("published") or entry.findtext("updated") or "")
            if title:
                items.append({
                    "tier": tier,
                    "source": name,
                    "title": title,
                    "url": link,
                    "summary": summary[:500],
                    "published_at": pub,
                })
            if len(items) >= limit:
                break

    return items


def _sort_key(item):
    tier_rank = {"first_party": 0, "premium": 1, "general": 2}.get(item["tier"], 99)
    if item.get("published_at"):
        ts = datetime.fromisoformat(item["published_at"]).timestamp()
    else:
        ts = 0
    return (tier_rank, -ts)


def main():
    all_items = []
    for tier, name, url in SOURCES:
        all_items.extend(fetch_rss(tier, name, url))

    all_items.sort(key=_sort_key)

    out = {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "count": len(all_items),
        "items": all_items,
    }
    json.dump(out, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
