# X 监控账号池 v1(约 70 个)

> 规则:A/B 层全收(24h 内原创,转推不收);C 层点赞 ≥50 才收。
> 注意:本文件中所有"at+用户名"都会被脚本当作监控账号提取,备注里不要随手写 at 符号。
> 维护:改仓库根目录这份,提交后 Action 自动重跑生效。标"待核"的等下一轮输出核对。

## A. 竞对官方号 + 创始人(全收)

| 主体 | 账号 | 备注 |
|------|------|------|
| Rain | @raincards | 官方,已核 |
| Kulipa | @kulipa_xyz | 官方 |
| Immersve | @immersve | 官方 |
| Stripe | @stripe | 官方,已核 |
| Stripe 创始人 | @patrickc, @collision | Patrick 与 John Collison |
| Bridge 创始人 | @zachabrams | 待核(防同名) |
| Kast | @KAST_official | 官方,已核(旧号 KASTcard 弃用) |
| RedotPay | @RedotPay | 官方,已核 |
| Gnosis Pay | @gnosispay | 官方,已核 |
| Ether.fi | @ether_fi | 官方,已核 |
| Infini | @0xinfini | 官方,已核 |
| Reap | @Reap_hq | 收购后动向 |
| Holyheld | @holyheld | 官方 |
| Bleap | @bleapfinance | 官方 |
| Wirex | @wirexapp | 官方,已核 |
| Zero Hash | @zerohashX | 官方,已核 |
| Marqeta | @Marqeta | 官方 |
| Lithic | @Lithic | CaaS |
| Paymentology | @Paymentology | CaaS |

## B. 卡组织 / 稳定币发行方 / 支付基建 / 数字银行(全收)

| 主体 | 账号 | 备注 |
|------|------|------|
| Visa | @Visa, @VisaNews | 双号 |
| Visa Crypto 负责人 | @cuysheffield | Cuy Sheffield |
| Mastercard | @Mastercard, @MastercardNews | 双号 |
| Mastercard 数字资产负责人 | @RajDhamodharan | 待核 |
| Circle | @circle, @jerallaire | 官方 + CEO,已核 |
| Tether | @Tether_to, @paoloardoino | 官方 + CEO |
| Paxos | @Paxos | 已核 |
| Ethena | @ethena_labs | USDe |
| Agora | @withAUSD | AUSD,待核 |
| Usual | @usualmoney | 待核 |
| StraitsX | @StraitsX | 新加坡稳定币 |
| BVNK | @bvnkpay | 已被 Mastercard 收购 |
| Fireblocks | @FireblocksHQ | 已核 |
| MoonPay | @moonpay | 支付通道 |
| PayPal | @PayPal | 已核 |
| Cash App | @CashApp | Block 系 |
| Airwallex | @airwallex | 跨境 |
| Nium | @NiumGlobal | 待核 |
| Wise | @Wise | 跨境 |
| Adyen | @Adyen | 收单 |
| Revolut | @RevolutApp | 数字银行 |
| Nubank | @nubank | 拉美 |
| Chime | @Chime | 美国 neobank,稳定币传闻 |
| HashKey | @HashKeyGroup | 香港 |
| MetaMask | @MetaMask | 钱包卡 |
| Ledger | @Ledger | 钱包卡 |
| Trust Wallet | @TrustWallet | 钱包 |
| Nexo | @Nexo | 加密信贷卡 |
| Oobit | @oobit | tap-to-pay |
| 1inch | @1inch | DeFi 卡 |

## C. 交易所 / KOL / 投资人 / 记者 / 政策(点赞 ≥50 才收)

| 主体 | 账号 | 备注 |
|------|------|------|
| Kraken | @krakenfx | 营销多,降到 C 层 |
| Coinbase | @coinbase | |
| Bybit | @Bybit_Official | 待核 |
| OKX | @okx | |
| Crypto.com | @cryptocom | |
| Gemini | @Gemini | |
| Bitget Wallet | @BitgetWallet | |
| Simon Taylor | @sytaylor | Fintech Brainfood,已核 |
| Rob Hadick | @HadickM | Dragonfly |
| Dragonfly | @dragonfly_xyz | |
| a16z crypto | @a16zcrypto | |
| Pantera | @PanteraCapital | |
| Artemis | @artemis__xyz | 稳定币数据 |
| Nic Carter | @nic__carter | |
| Austin Campbell | @CampbellJAustin | 稳定币监管 |
| Nikhilesh De | @nikhileshde | CoinDesk 监管线 |
| Wu Blockchain | @WuBlockchain | 中文圈英文号 |
| 新加坡金管局 | @MAS_sg | 政策 |

## 粗筛规则(fetch_x_action.py 实现)
- A/B 层:全收(24h 内),转推不收
- C 层:点赞 ≥50 才收
- 全部条目带时间戳进 filter.py,窗口去重照旧
