#!/usr/bin/env python3
"""
sentinel filter — 确定性过滤层(移植 TrendRadar 思路)
输入: work/candidates.json  [{"title","url","pubDate","source"}, ...]
处理: 1) 解析 pubDate,强制时间窗口(默认 26h,--hours 覆盖)
      2) 关键词预筛(keywords.json: 公司名词边界匹配 + 主题词)
      3) 对 state/seen.json 去重(URL 规范化 + 标题指纹),跨天有效
输出: work/shortlist.json(交给 LLM 终筛)+ 更新 state/seen.json
      stdout 打印统计,方便留痕
"""
import json, re, sys, hashlib, argparse
from pathlib import Path
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone, timedelta

BASE = Path(__file__).parent

def norm_url(u):
    u = u.strip().split("#")[0]
    u = re.sub(r"[?&](utm_[a-z]+|ref|src|source)=[^&]*", "", u)
    return u.rstrip("/?&").lower()

def title_fp(t):
    return hashlib.sha1(re.sub(r"\W+", "", t.lower()).encode()).hexdigest()[:16]

def parse_date(s):
    s = (s or "").strip()
    for fn in (parsedate_to_datetime,
               lambda x: datetime.fromisoformat(x.replace("Z", "+00:00"))):
        try:
            d = fn(s)
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except Exception:
            pass
    return None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hours", type=float, default=26.0)
    args = ap.parse_args()

    kw = json.loads((BASE / "keywords.json").read_text())
    companies = kw["companies"]
    need_ctx = set(kw["companies_need_context"]["names"])
    ctx_words = [c.lower() for c in kw["companies_need_context"]["context"]]
    topics = [t.lower() for t in kw["topics"]]

    cand_path = BASE / "work" / "candidates.json"
    items = json.loads(cand_path.read_text())
    seen_path = BASE / "state" / "seen.json"
    seen = json.loads(seen_path.read_text()) if seen_path.exists() else {}

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(hours=args.hours)
    out, stats = [], {"total": len(items), "bad_date": 0, "too_old": 0,
                      "no_keyword": 0, "duplicate": 0, "kept": 0}

    for it in items:
        title = (it.get("title") or "").strip()
        url = (it.get("url") or "").strip()
        if not title or not url:
            stats["bad_date"] += 1
            continue
        d = parse_date(it.get("pubDate", ""))
        if d is None:
            stats["bad_date"] += 1
            continue
        if d < cutoff:
            stats["too_old"] += 1
            continue

        tl = title.lower()
        hit = None
        if title.startswith("[X @"):
            hit = "x-account"   # 账号池推文已在 fetch_x.py 分层筛过,免关键词预筛
        for t in topics:
            if hit: break
            if t in tl:
                hit = f"topic:{t}"; break
        if not hit:
            for c in companies:
                if re.search(rf"\b{re.escape(c)}\b", title):
                    if c in need_ctx and not any(w in tl for w in ctx_words):
                        continue
                    hit = f"company:{c}"; break
        if not hit:
            stats["no_keyword"] += 1
            continue

        key_u, key_t = norm_url(url), title_fp(title)
        if key_u in seen or key_t in seen:
            stats["duplicate"] += 1
            continue
        seen[key_u] = seen[key_t] = now.isoformat()
        it["matched"] = hit
        it["parsed_date_utc"] = d.isoformat()
        out.append(it)
        stats["kept"] += 1

    # 清理 14 天前的去重记录,防止 state 无限膨胀
    horizon = now - timedelta(days=14)
    seen = {k: v for k, v in seen.items()
            if datetime.fromisoformat(v) > horizon}

    out.sort(key=lambda x: x["parsed_date_utc"], reverse=True)
    (BASE / "work" / "shortlist.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1))
    seen_path.write_text(json.dumps(seen))
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()
