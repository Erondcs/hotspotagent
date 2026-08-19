#!/usr/bin/env python3
"""
sentinel RSS 取数层(GitHub Actions 中转版)
  python3 fetch_feeds.py pull   # 从中转仓库读 feeds_items.json,合并进 work/candidates.json
RSS 由仓库 Action 每天 00:40 UTC 统一抓取(真解析器,时间戳可靠),云端会话零审批读取。
"""
import json, sys, urllib.request
from pathlib import Path
from datetime import datetime, timezone

BASE = Path(__file__).parent
URL = "https://raw.githubusercontent.com/Erondcs/hotspotagent/main/feeds_items.json"
MAX_AGE_HOURS = 20

def cmd_pull():
    req = urllib.request.Request(URL, headers={"User-Agent": "sentinel"})
    data = json.loads(urllib.request.urlopen(req, timeout=20).read().decode())
    fetched = datetime.fromisoformat(data["fetched_at"])
    age_h = (datetime.now(timezone.utc) - fetched).total_seconds() / 3600
    if age_h > MAX_AGE_HOURS:
        print(f"feeds_items.json 已过期 {age_h:.0f}h,拒收", file=sys.stderr); sys.exit(1)
    cand_path = BASE / "work" / "candidates.json"
    items = json.loads(cand_path.read_text()) if cand_path.exists() else []
    items.extend(data.get("items", []))
    cand_path.write_text(json.dumps(items, ensure_ascii=False, indent=1))
    print(f"merged {data.get('count', 0)} feed items (age {age_h:.1f}h, errors={len(data.get('errors', []))})")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pull":
        cmd_pull()
    else:
        print(__doc__)
