# X 监控账号池 v0(草稿)

> 状态:handle 均为待验证(接入 socialdata 后用 API 逐个核实,防止同名号/停更号)。
> 用法:fetch_x.py 每天拉各账号过去 24h 推文 → 进 filter 流水线 → 简报"社媒信号"节。
> 维护:加减账号改这个文件即可。

## A. 竞对官方号 + 创始人(最高优先级)

| 公司 | 账号(待验证) | 备注 |
|------|--------------|------|
| Rain | @raincards | 官方;另找 CEO Farooq Malik 个人号 |
| Kulipa | @kulipa_xyz | 官方;CEO Axel Cateland |
| Immersve | @immersve | 官方 |
| Bridge/Stripe | @stripe, @bridgexyz | Bridge 创始人 Zach Abrams 个人号也值得盯 |
| Kast | @kast | 官方;创始人 Daniel Bertoli? 待核 |
| RedotPay | @RedotPay | 官方 |
| Gnosis Pay | @gnosispay | 官方 |
| Ether.fi | @ether_fi | 官方;CEO Mike Silagadze |
| Infini | @0xinfini | 官方 |
| Reap/Kraken | @Reap_hq, @krakenfx | 收购后动向 |
| Holyheld | @holyheld | 官方 |
| Bleap | @bleapfinance | 官方 |
| Wirex | @wirexapp | 官方 |
| Zero Hash | @zerohashX | 官方 |
| Marqeta | @Marqeta | 官方 |

## B. 卡组织 / 稳定币发行方 / 基建

| 主体 | 账号(待验证) |
|------|--------------|
| Visa Crypto | @VisaNews + Cuy Sheffield(Visa crypto 负责人)个人号 |
| Mastercard | @MastercardNews + Raj Dhamodharan(数字资产负责人) |
| Circle | @circle + @jerallaire (CEO) |
| Tether | @Tether_to + @paoloardoino (CEO) |
| Paxos | @Paxos |
| BVNK | @bvnkpay |
| Fireblocks | @FireblocksHQ |
| PayPal Crypto | @PayPal |

## C. KOL / 分析师 / 数据号

| 人/号 | 方向 |
|-------|------|
| Simon Taylor (@sytaylor) | Fintech Brainfood 作者,稳定币支付评论最勤 |
| Paymentscan | 稳定币卡交易量数据 |
| Rob Hadick (@HadickM) | Dragonfly,支付/稳定币投资人 |
| Artemis (@artemis__xyz) | 稳定币数据 |
| Nic Carter (@nic__carter) | 稳定币宏观 |
| Austin Campbell (@CampbellJAustin) | 稳定币监管/银行 |
| Ran (@rgoldstein?) | 待定,补充支付记者 |
| CoinDesk payments 线记者 | 接入后按近期署名文章反查账号 |

## 粗筛规则(fetch_x.py 实现)
- 官方号/创始人:全收(24h 内),转推不收
- KOL:互动量阈值(如 点赞>50 或 转发>10)+ 关键词(stablecoin/card/payment/wallet/license)
- 全部条目带时间戳进 filter.py,窗口去重照旧
