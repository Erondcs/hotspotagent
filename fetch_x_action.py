#!/usr/bin/env python3
"""
GitHub Actions 端:从 socialdata.tools 拉账号池过去 26h 推文,写 x_tweets.json。
账号池来自仓库根目录 x_accounts.md(## A./B./C. 分层,@handle 自动提取)。
env: SOCIALDATA_KEY
"""
import json, os, re, sys, time, urllib.request, urllib.parse
from datetime import datetime, timezone, timedelta

API = "https://api.socialdata.tools"
KEY = os.environ["SOCIALDATA_KEY"]
KOL_MIN_LIKES = 50

def get(path, params=None):
    url = f"{API}{path}" + (f"?{urllib.parse.urlencode(params)}" if params else "")
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {KEY}", "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())

def handles():
    text = open("x_accounts.md", encoding="utf-8").read()
    tier, out, seen = "?", [], set()
    for line in text.splitlines():
        m = re.match(r"^## ([ABC])\.", line)
        if m: tier = m.group(1)
        for h in re.findall(r"@([A-Za-z0-9_]{1,15})", line):
            if h.lower() not in seen:
                seen.add(h.lower()); out.append((h, tier))
    return out

def main():
    cutoff = datetime.now(timezone.utc) - timedelta(hours=26)
    since = int(cutoff.timestamp())
    tweets, errors = [], []
    for h, t in handles():
        try:
            res = get("/twitter/search", {
                "query": f"from:{h} since_time:{since} -filter:replies",
                "type": "Latest"})
            for tw in res.get("tweets", []):
                likes = tw.get("favorite_count", 0) or 0
                if t == "C" and likes < KOL_MIN_LIKES:
                    continue
                if tw.get("retweeted_status"):
                    continue
                tweets.append({
                    "title": f"[X @{h}] " + (tw.get("full_text") or tw.get("text", ""))[:280],
                    "url": f"https://x.com/{h}/status/{tw.get('id_str', tw.get('id'))}",
                    "pubDate": tw.get("tweet_created_at") or tw.get("created_at", ""),
                    "source": f"X/@{h} (tier {t}, ♥{likes})"})
        except Exception as e:
            errors.append(f"@{h}: {e}")
        time.sleep(0.3)
    out = {"fetched_at": datetime.now(timezone.utc).isoformat(),
           "count": len(tweets), "errors": errors, "tweets": tweets}
    json.dump(out, open("x_tweets.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{len(tweets)} tweets, {len(errors)} errors")
    if errors:
        print("\n".join(errors), file=sys.stderr)

if __name__ == "__main__":
    main()
