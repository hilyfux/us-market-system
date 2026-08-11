# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-11T22:07:00+08:00

## Rules

- `alert_key = symbol + fact_id + action + trigger_band`
- Suppress an identical successful alert for 24 hours.
- Record a key only after the webhook returns `errcode=0`.
- A failed send is recorded in system-state but is not retried and does not create a dedupe key.

## Active dedupe keys

| key | sent_at | channel | result |
|---|---|---|---|
| INTRADAY+2026-07-16+10 | 2026-07-16T10:30:52-04:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-07-17+08 | 2026-07-17T08:08:00+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-16+11 | 2026-07-16T11:31:01-04:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-24+1100 | 2026-07-24T23:07:46+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-07-27 | 2026-07-27T08:35:48-04:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-27+1000 | 2026-07-27T10:05:05-04:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-27+1230 | 2026-07-27T12:33:42-04:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-27+1530 | 2026-07-27T15:30:00-04:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-07-27 | 2026-07-28T04:36:44+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-07-27 | 2026-07-28T08:38:32+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-07-28 | 2026-07-28T20:34:00+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-28+1000 | 2026-07-28T22:05:19+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-28+1230 | 2026-07-29T00:33:49+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-28+1530 | 2026-07-29T03:34:29+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-07-28 | 2026-07-29T04:36:43+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-07-28 | 2026-07-29T08:44:38+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-07-29 | 2026-07-29T20:35:57+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-29+1000 | 2026-07-29T22:05:14+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-29+1230 | 2026-07-29T12:34:43-04:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-29+1530 | 2026-07-29T15:35:03-04:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-07-29 | 2026-07-30T04:43:51+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-07-29 | 2026-07-30T08:43:27+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-07-30 | 2026-07-30T20:34:45+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-30+1000 | 2026-07-30T22:05:05+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-30+1530 | 2026-07-30T15:35:00-04:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-07-30 | 2026-07-31T04:43:30+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-07-30 | 2026-07-31T08:54:23+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-07-31 | 2026-07-31T20:36:45+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-07-31+1000 | 2026-07-31T22:05:03+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-07-31 | 2026-08-01T04:46:31+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-07-31 | 2026-08-01T08:37:22+08:00 | enterprise_wechat | errcode=0 |
| HEARTBEAT+2026-08-01 | 2026-08-01T20:02:48+08:00 | enterprise_wechat | errcode=0 |
| HEARTBEAT+2026-08-02 | 2026-08-02T20:02:56+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-03 | 2026-08-03T20:37:20+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-03+1000 | 2026-08-03T22:08:41+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-03+1230 | 2026-08-04T01:23:25+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-03+1530 | 2026-08-04T03:34:54+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-03 | 2026-08-04T04:58:13+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-03 | 2026-08-04T08:37:01+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-04 | 2026-08-04T20:36:31+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-04+1000 | 2026-08-04T22:07:52+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-04+1230 | 2026-08-05T00:36:25+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-04+1530 | 2026-08-05T03:39:07+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-04 | 2026-08-05T04:50:24+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-04 | 2026-08-05T08:42:15+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-05 | 2026-08-05T20:36:48+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-05+1000 | 2026-08-05T22:07:07+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-05+1230 | 2026-08-06T00:38:40+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-05+1530 | 2026-08-06T03:38:20+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-05 | 2026-08-06T04:50:36+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-05 | 2026-08-06T08:44:28+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-06 | 2026-08-06T20:36:59+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-06+1000 | 2026-08-06T22:28:23+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-06+1230 | 2026-08-07T00:43:50+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-06 | 2026-08-07T17:41:21+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-06 | 2026-08-07T17:41:21+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-07 | 2026-08-07T20:37:01+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-07+1000 | 2026-08-07T22:05:20+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-07+1030 | 2026-08-07T22:34:27+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-07+1230 | 2026-08-08T00:33:53+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-07+1530 | 2026-08-08T03:33:33+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-07 | 2026-08-08T04:46:49+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-07 | 2026-08-08T08:43:41+08:00 | enterprise_wechat | errcode=0 |
| HEARTBEAT+2026-08-08 | 2026-08-08T20:03:10+08:00 | enterprise_wechat | errcode=0 |
| HEARTBEAT+2026-08-09 | 2026-08-09T20:02:35+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-10 | 2026-08-10T20:38:07+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-10+1000 | 2026-08-10T22:05:28+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-10+1230 | 2026-08-11T00:34:02+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-10+1530 | 2026-08-11T03:35:43+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-10 | 2026-08-11T04:50:00+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-10 | 2026-08-11T08:45:54+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-11 | 2026-08-11T20:37:27+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-11+1000 | 2026-08-11T22:06:48+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-11+1230 | 2026-08-12T00:38:22+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-11+1530 | 2026-08-12T03:45:05+08:00 | enterprise_wechat | errcode=0 |

## Pending close signals

> 纪律 L-015/L-016：每条离场判据都必须写成**次日收盘可判定的具体数值**，禁止凭形态印象决定；部分止盈时必须同时为剩余仓写下一档数值。以下为 **2026-08-11 POST_CLOSE 更新**（当日正式收盘 VERIFIED），供 2026-08-12 及之后的收盘逐日判定。

**本场基准**：SPY 770.56 −0.32%｜QQQ 718.45 −0.34%｜IWM 300.99 +0.34%｜VIX 15.29 −1.10%｜US10Y 4.69%。环境 **RISK_ON**（VIX < 16，SPY 距 52 周高 776.85 仅 −0.81%，必在 50/200 日线之上；MA 精确值今日不可得——AV 免费额度已用尽、stockanalysis statistics 页取不到，显式标注不臆造），仓位上限 90%，当前仓位率 77.87% 未触顶。组合当日 **+0.79% vs SPY −0.32%（+1.11pp）**。

### 盘中标记的收盘裁定（ACT-002/003）

- **MP（10:00 开盘报告 🚨 待收盘确认）→ 未确认**。登记条件「正式收盘跌破 52.66 且放量」；实际收盘 **55.24（+1.06%）**，日内自 −2.54%（低 52.90）一路收复并收在区间上沿。判定：**误报，不触发任何减仓**，动作 `持有`。
- **LLY（15:30 盘中报告提出的今晚定论）→ 突破未失败**。判据「官方收盘 < 1185.71（8/7 收盘）即视为 8/10 突破失败」；实际收盘 **1215.02（−1.37%）**，高于判据 29.31（+2.47%）。判定：**未确认**，动作 `持有`。但确认了「缩量回落」的事实：成交 2.09M < 8/10 突破日 2.92M < 8/5 财报日 6.40M，连续两日缩量下跌。

### 逐仓次日判据（2026-08-12 收盘可判定）

- **KTOS 冲高衰竭（第 3 次登记，本轮判定＝未确认）**：8/11 收 **63.73（+2.10%）**，创本轮新高，日内 61.34–63.83。登记条件（收盘 < 58.90 或 < 56.25 且放量）两条均未触发 → **持有**。**同一登记连续两轮被证伪**，是 L-015「判据优于形态印象」的正面证据。须记录的反面事实：**放量不足——2.74M 显著低于 8/10 的 4.10M**，创新高却缩量。**次日判据（前移）：官方收盘 < 61.34（8/11 低）或 < 58.90（8/10 低），且成交量放大 → 按 ACT-003 评估减仓。** 集中度：市值 13,577.05 = **12.61% NAV，全书最大**，累计 **+35.77%**；单只 20% 上限仍有余量。
- **MP 高位判据（本轮判定＝未确认，见上）**：**次日判据：官方收盘 < 52.90（8/11 低）或 < 52.66（8/10 低）且放量 → 按 ACT-003 评估。** 当日无公司公告，成交 6.13M 较 8/10 的 10.53M 明显收缩，属跟随性反弹。累计 +23.08%。
- **LLY 失效线（建仓后第 2 个交易日，未触发）**：**官方收盘 < 1115.68** 不变，余量 **−8.17%**。**新增次日判据（把 15:30 的问题固化为数值）：官方收盘 < 1185.71（8/7 收盘）→ 判定 8/10 英国批准的突破失败，进入衰竭复核；若同时跌破 1169.86（8/6 收盘）则视为 Q2 财报涨幅亦作废，按 ACT-003 评估离场。** 提醒：**8/14 除息 $1.73**（见账务缺口）。
- **ETN 新高后的首条数值判据（本轮新登记）**：8/11 收 **459.29（+3.22%）**，为**入场以来最高收盘**，日内 446.50–463.75（盘中创 52 周新高，站方 52 周高字段 463.02 尚未刷新）。当日**没有任何以 8/11 为日期的公司公告**，唯一同日消息是「AI 的下一个瓶颈是电力而非芯片」的板块文章 → 归因为主题资金流，不计入论点兑现证据（L-018）。**次日判据：官方收盘 < 446.50（8/11 低）→ 按 ACT-003 进入衰竭复核；连续两日收在 446.50 下方且放量 → 评估减仓。** 累计 +14.62%。**次日复检动作（L-020）：明日必须复查 8/11 是否实有公司公告，查到即当场改写归因。**
- **NVDA 失效线（建仓后第 3 个交易日，未触发）**：**官方收盘 < 200.75** 不变；8/11 收 **217.50（−0.02%）**，余量 **+8.34%**。当日日内 216.20–222.20、成交 100.6M，全天大幅震荡但收平；唯一同日消息是 AI 数据中心供电架构升级计划（800VDC 方向），属产品路线图、非经营事实。近端二元事件：**Q2 财报 2026-08-26（距 11 个交易日）**，**8/19 起进入 ≤5 交易日窗口，届时按 L-002 只持有**。
- **MSFT 止损线（建仓后第 5 个交易日，未触发）**：**官方收盘 < 437.00** 不变；8/11 收 **503.81（−0.44%）**，余量 **−13.2%**，为当日全书最弱。同日消息：AI 发现 Windows 漏洞的速度快于修补速度（TipRanks，属叙事性负面、非披露事实），无公司层面减值 → 持有。
- **PWR（无待确认信号）**：8/11 收 **670.58（+1.47%）**，日内冲高 680.00 后回落，成交 937,829。无当日公司公告，最近事实仍是 8/7 KeyBanc 升级至 Overweight（目标 807）。累计 +6.04%。
- **ABT（无待确认信号，当日唯一有公司事实的持仓）**：8/11 收 **109.72（+1.01%）**，成交 6.49M。**同日公告：Abbott 与 Google 达成合作，把连续血糖数据与 AI 结合用于日常健康管理**（PRNewswire/TheFly）——属论点强化（器械+数据平台），不构成任何离场条件。累计 +5.67%。

### 长期登记项

- **GEV 离场后跟踪（非交易指令）**：8/10 以 990.85 平仓、已实现 −203.01。跟踪其相对 SPY 与相对 LLY 的后续表现，用于验证替换门 5 分阈值是否过于激进。
- **⚠️ 账务缺口（第 11 次登记，仍待用户裁定，本轮同样未擅改模型）**：C2 恒等式 `cash = initial − Σcost_basis + realized` **未建模股息**。已发生：ETN 2026-08-07 除息 $1.10 × 24.956686 股 = **$27.45**。3 日后发生：LLY 2026-08-14 除息 $1.73 × 8.117278 股 = **$14.04**，届时缺口累计 **$41.49**。每次除息都会再累积一次。修复需用户裁定口径（计入现金 / 计入已实现 / 不建模并显式标注），系统不单方面改账务模型。
- **⚠️ 技术指标缺口（第 2 次登记）**：MA20/MA50/MA200 自 2026-07-30 起未能刷新（Alpha Vantage 免费层 25 次/日额度在本轮运行前已被耗尽，`data/analytics.md` as-of 仍是 2026-07-27）。当前所有离场判据均为**收盘价与前低**的显式数值，不依赖均线，故不阻断交易；但均线一栏不得被当作现值引用。补救路径：AV 额度次日重置后在 MORNING 补算，或接入含 full 日线的源。
