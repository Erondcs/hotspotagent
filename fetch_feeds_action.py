#!/usr/bin/env python3
"""
GitHub Actions 端 v2:拉取 sentinel/feeds.md 里的全部 RSS 源,写 feeds_items.json。
v2 变更:保留 RSS 自带摘要(description / content:encoded,去 HTML,<=600 字符);
对 26h 内且摘要过短的条目,顺手抓一次正文(<=1500 字符,上限 40 篇)——
云端会话因此不再需要 WebFetch 原文,零审批。
"""
import json, re, sys, time, urllib.request
import xml.etree.ElementTree as ET
from html import unescape
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0 Safari/537.36"}
BODY_FETCH_CAP = 40
CONTENT_NS = "{http://purl.org/rss/1.0/modules/content/}encoded"

def feed_urls():
    urls = []
    for line in open("sentinel/feeds.md", encoding="utf-8"):
        if line.startswith("## 测过不可用"):
            break
        m = re.search(r"\|\s*(https://\S+)\s*\|", line)
        if m:
            urls.append(m.group(1))
    return urls

def strip_html(s, limit):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<[^>]+>", " ", s)
    s = unescape(re.sub(r"\s+", " ", s)).strip()
    return s[:limit]

def text(el, *names):
    for n in names:
        found = el.find(n)
        if found is not None and (found.text or found.get("href")):
            return (found.text or found.get("href")).strip()
    return ""

def parse(content, source):
    items = []
    root = ET.fromstring(content)
    for it in root.iter("item"):
        summary = text(it, CONTENT_NS) or text(it, "description")
        items.append({
            "title": text(it, "title"),
            "url": text(it, "link", "guid"),
            "pubDate": text(it, "pubDate", "{http://purl.org/dc/elements/1.1/}date"),
            "source": source,
            "summary": strip_html(summary, 600) if summary else ""})
    ns = "{http://www.w3.org/2005/Atom}"
    for it in root.iter(f"{ns}entry"):
        link = it.find(f"{ns}link")
        summary = text(it, f"{ns}content", f"{ns}summary")
        items.append({
            "title": text(it, f"{ns}title"),
            "url": link.get("href", "") if link is not None else "",
            "pubDate": text(it, f"{ns}published", f"{ns}updated"),
            "source": source,
            "summary": strip_html(summary, 600) if summary else ""})
    return [i for i in items if i["title"] and i["url"]]

def parse_date(s):
    for fn in (parsedate_to_datetime,
               lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))):
        try:
            d = fn(s.strip())
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception:
            pass
    return None

def fetch_body(url):
    req = urllib.request.Request(url, headers=UA)
    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
    paras = re.findall(r"<p[^>]*>(.*?)</p>", html, flags=re.S | re.I)
    body = " ".join(strip_html(p, 400) for p in paras[:12])
    return re.sub(r"\s+", " ", body).strip()[:1500]

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
    # 对窗口内且摘要不足的条目补抓正文
    cutoff = datetime.now(timezone.utc) - timedelta(hours=26)
    fetched = tried = 0
    for it in all_items:
        if tried >= BODY_FETCH_CAP:
            break
        d = parse_date(it.get("pubDate", ""))
        if d is None or d < cutoff or len(it.get("summary", "")) >= 200:
            continue
        tried += 1
        try:
            body = fetch_body(it["url"])
            if len(body) > len(it.get("summary", "")):
                it["summary"] = body
                fetched += 1
        except Exception:
            pass
        time.sleep(0.2)
    print(f"bodies fetched {fetched}/{tried}")
    out = {"fetched_at": datetime.now(timezone.utc).isoformat(),
           "count": len(all_items), "errors": errors, "items": all_items}
    json.dump(out, open("feeds_items.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"total {len(all_items)} items, {len(errors)} errors")
    if errors:
        print("\n".join(errors), file=sys.stderr)

if __name__ == "__main__":
    main()
