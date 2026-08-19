# 哨兵 (Sentinel) — DCS 竞对日度扫描 harness

架构移植自 TrendRadar / Horizon:**取数带时间戳 → 窗口/去重在代码里确定性完成 → LLM 只做终筛与撰写**。
解决纯 prompt 方案的根本问题:搜索引擎按相关度排序导致旧闻混入。

## 流水线(每天 09:00 Asia/Shanghai,定时任务自动执行)

```
feeds.md (8 个 RSS 源)
   │  WebFetch 拉取,RSS 自带精确 pubDate
   ▼
work/candidates.json          ← WebSearch 对 T1 公司补充扫描(须核实日期)也追加到这里
   │  python3 filter.py --hours 26
   │    · 解析 pubDate,强制时间窗口(26h,含 2h 重叠缓冲,重复靠去重解决)
   │    · keywords.json 预筛(公司名词边界匹配+上下文要求,主题词)
   │    · state/seen.json 去重(URL 规范化 + 标题指纹,保留 14 天)
   ▼
work/shortlist.json
   │  LLM 按 rules.md 终筛(五类事件+高管观点+安全事件),WebFetch 原文提炼事实
   ▼
reports/YYYY-MM-DD.md
   │  python3 push.py <report> "<标题>"(签名 + 推送 + 重试)
   ▼
Lark 群「竞对雷达」
```

## 文件说明
- `watchlist.md` — 56 家公司五档清单(人和 LLM 读,改监控范围改这里)
- `keywords.json` — filter.py 的预筛词表(加公司要同步改这里)
- `feeds.md` — RSS 源与拉取方式
- `rules.md` — 终筛标准与简报格式
- `filter.py` / `push.py` — 确定性代码层
- `state/seen.json` — 跨天去重状态(自动维护)
- `reports/` — 每日简报留档

## 已知限制
- 容器网络白名单只放行了 Lark,RSS 靠 WebFetch 代理拉取(可用但依赖小模型转录);若管理员放行新闻域名,filter 前可改为 curl 直拉,更快更稳
- 云环境极小概率被回收导致文件丢失;定时任务遇到目录缺失会向群里报错,届时找 Claude 用本 README + 备份 zip 重建
- 每天 09:00 是唯一扫描点,突发新闻最长延迟 24h;要更快可以把 cron 加密
