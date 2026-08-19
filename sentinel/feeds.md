# RSS 信息源(用 WebFetch 逐个拉取)

对每个 URL 用 WebFetch,prompt 固定为:
"这是 RSS XML。原样列出每个 item 的:标题 | 链接 | pubDate | 来源名。一行一条,不要总结,不要遗漏。没有 item 就说 empty。"

| Feed | 覆盖 | 备注 |
|------|------|------|
| https://www.coindesk.com/arc/outboundfeeds/rss/ | 全行业 | 已验证可用 |
| https://www.theblock.co/rss.xml | 全行业 | 已验证可用 |
| https://www.pymnts.com/category/cryptocurrency/feed/ | 支付视角 | 已验证可用 |
| https://www.ledgerinsights.com/feed/ | 企业区块链/银行 | 已验证可用 |
| https://decrypt.co/feed | 全行业 | 已验证可用 |
| https://blockworks.com/feed | 全行业 | 注意是 .com(.co 会 302) |
| https://cointelegraph.com/rss | 全行业 | 未验证,失败就跳过 |
| https://www.finextra.com/rss/headlines.aspx | 金融科技 | 已验证可用 |
| https://www.pymnts.com/feed/ | 支付全行业 | 已验证可用 |
| https://www.paymentsdive.com/feeds/news/ | 支付行业 | 已验证可用 |
| https://techcrunch.com/category/fintech/feed/ | fintech 创投 | 已验证可用 |
| https://www.paymentsjournal.com/feed/ | 支付垂直 | 已验证可用,更新快 |
| https://fintechnews.sg/feed/ | 新加坡/东南亚 fintech | 已验证可用,DCS 本地市场 |
| https://fintech.global/feed/ | fintech 融资/合规 | 已验证可用 |
| https://thefintechtimes.com/feed/ | fintech 综合 | 已验证可用,偏专题 |
| https://insights4vc.substack.com/feed | 稳定币卡深度(周更) | Substack,失败就跳过 |
| https://www.fintechwrapup.com/feed | fintech 深度(周更) | Substack,失败就跳过 |

## 测过不可用的(别再试)
thepaypers.com/rss(路径 404)、ffnews.com/feed(非 RSS)、fintechfutures.com/feed(404)、wublockchain substack(停更)、PR Newswire financial-services(噪音太大,含房地产等)、Google News RSS(robots 禁抓)、Bing News RSS(空返回)

## WebSearch 补充扫描(RSS 覆盖不到的 T1 公司)

对 T1 名单(见 watchlist.md)做逐家 WebSearch(加当前月份年份),**搜到的每条候选必须用 WebFetch 打开原文核实发布日期**,核实不了日期的直接丢弃。核实过的按同样格式追加进 work/candidates.json,和 RSS 条目一起过 filter.py。
