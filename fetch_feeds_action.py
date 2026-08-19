#!/usr/bin/env python3
"""
GitHub Actions 端:拉取 sentinel/feeds.md 里的全部 RSS 源,写 feeds_items.json。
feed 列表从 sentinel/feeds.md 的表格提取(遇到"## 测过不可用"停止)。
"""
import json, re, sys, urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

UA = {"User-Agent": "Mozilla/5.0 (compatible; dcs-sentinel-rss/1.0)"}

def feed_urls():
    urls = []
    for line in open("sentinel/feeds.md", encoding="utf-8"):
        if line.startswith("## 测过不可用"):
            break
        m = re.search(r"\|\s*(https://\S+)\s*\|", line)
        if m:
            urls.append(m.group(1))
    return urls

def text(el, *names):
    for n in names:
        found = el.find(n)
        if found is not None and (found.text or found.get("href")):
            return (found.text or found.get("href")).strip()
    return ""

def parse(content, source):
    items = []
    root = ET.fromstring(content)
    # RSS 2.0
    for it in root.iter("item"):
        items.append({
            "title": text(it, "title"),
            "url": text(it, "link", "guid"),
            "pubDate": text(it, "pubDate", "{http://purl.org/dc/elements/1.1/}date"),
            "source": source})
    # Atom
    ns = "{http://www.w3.org/2005/Atom}"
    for it in root.iter(f"{ns}entry"):
        link = it.find(f"{ns}link")
        items.append({
            "title": text(it, f"{ns}title"),
            "url": link.get("href", "") if link is not None else "",
            "pubDate": text(it, f"{ns}published", f"{ns}updated"),
            "source": source})
    return [i for i in items if i["title"] and i["url"]]

def main():
    all_items, errors = [], []
    for u in feed_urls():
        source = re.sub(r"^https?://(www\.)?", "", u).split("/")[0]
        try:
            req = urllib.request.Request(u, headers=UA)
            content = urllib.request.urlopen(req, timeout=25).read()
            got = parse(content, source)
            all_items.extend(got)
            print(f"{source}: {len(got)} items")
        except Exception as e:
            errors.append(f"{source}: {e}")
    out = {"fetched_at": datetime.now(timezone.utc).isoformat(),
           "count": len(all_items), "errors": errors, "items": all_items}
    json.dump(out, open("feeds_items.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"total {len(all_items)} items, {len(errors)} errors")
    if errors:
        print("\n".join(errors), file=sys.stderr)

if __name__ == "__main__":
    main()
