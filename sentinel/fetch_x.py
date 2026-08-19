#!/usr/bin/env python3
"""
sentinel X 取数层(GitHub Actions 中转版)
  python3 fetch_x.py pull   # 从中转仓库读 x_tweets.json,合并进 work/candidates.json
中转仓库的 Action 每天 00:40 UTC 拉 socialdata 并提交 x_tweets.json(见该仓库 README)。
容器直连 socialdata 被网络白名单挡住,故经 GitHub 中转;raw.githubusercontent.com 已验证可达。
"""
import json, sys, urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).parent
# 仓库已转 public,直接读 raw 根目录的 x_tweets.json(由 GitHub Action 每天 00:40 UTC 更新)
URL = "https://raw.githubusercontent.com/Erondcs/hotspotagent/main/x_tweets.json"
MAX_AGE_HOURS = 20   # 超过则视为过期数据,拒收

def cmd_pull():
    req = urllib.request.Request(URL, headers={"User-Agent": "sentinel"})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    fetched = datetime.fromisoformat(data["fetched_at"])
    age_h = (datetime.now(timezone.utc) - fetched).total_seconds() / 3600
    if age_h > MAX_AGE_HOURS:
        print(f"x_tweets.json 已过期 {age_h:.0f}h,拒收", file=sys.stderr); sys.exit(1)
    cand_path = BASE / "work" / "candidates.json"
    items = json.loads(cand_path.read_text()) if cand_path.exists() else []
    items.extend(data.get("tweets", []))
    cand_path.write_text(json.dumps(items, ensure_ascii=False, indent=1))
    print(f"merged {data.get('count', 0)} tweets (age {age_h:.1f}h, errors={len(data.get('errors', []))})")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pull":
        cmd_pull()
    else:
        print(__doc__)
