# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-14T00:54:00+08:00

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
| POSTCLOSE+2026-08-11 | 2026-08-12T04:48:20+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-11 | 2026-08-12T09:08:20+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-12 | 2026-08-12T20:41:46+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-12+1000 | 2026-08-12T22:18:07+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-12+1230 | 2026-08-13T00:48:40+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-12+1530 | 2026-08-13T04:02:13+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-12 | 2026-08-13T04:45:33+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-12 | 2026-08-13T08:43:25+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-13 | 2026-08-13T20:36:56+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-13+1030 | 2026-08-13T22:46:25+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-13+1230 | 2026-08-14T00:50:53+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-13+1530 | 2026-08-14T03:37:31+08:00 | enterprise_wechat | errcode=0 |

## Pending close signals

> 纪律 L-015/L-016：每条离场判据都必须写成**次日收盘可判定的具体数值**，禁止凭形态印象决定；部分止盈时必须同时为剩余仓写下一档数值。以下为 **2026-08-13 POST_CLOSE 更新**（当日正式收盘 VERIFIED），供 2026-08-14 及之后的收盘逐日判定。

**本场基准**：SPY 777.88 +0.70%（收盘新高，盘中 779.37 创 52 周新高）｜QQQ 732.07 +1.16%｜IWM 303.50 +0.26%｜VIX 14.63 +0.55%｜US10Y ⚠️ 当日收盘无核准源（官方日频最新 8/11=4.70%，显式缺口不臆造）。环境 **RISK_ON**（VIX 14.63 < 16，SPY 创收盘新高），仓位上限 90%，当前仓位率 82.34% 未触顶。组合当日 **−0.14% vs SPY +0.70%（−0.84pp）**——连续第 2 个跑输日：QQQ 领涨的大盘股行情里，电力/工业腿（KTOS/ETN/PWR）与 LLY/LNG 五仓齐跌，MP +2.86% 一仓独扛。

### 盘中标记的收盘裁定（ACT-002/003）

- **ETN（判据「收盘 < 459.03 → 衰竭复核」触发）→ 复核裁定＝持有**。收 **453.33（−1.44%）**，低于复核线 1.24%——价格要件成立，但量能要件不成立：量 1.14M 较 8/12 的 1.64M **缩 31%**，非放量出货；保留的减仓判据「连续两日收在 446.50 下方且放量」未触及（收盘高出 1.53%）；且同日 PWR 同跌、QQQ 领涨＝板块轮动有解释。按登记的判据阶梯，只收紧数值、不凭形态减仓（L-015）。**次日判据收紧：官方收盘 < 452.50（8/13 低）且放量 → ACT-003 评估减仓；<446.50 双日放量判据保留。**
- **KTOS（判据「收盘 < 62.10 或 < 61.34 且放量」）→ 未确认（第 5 轮证伪）**。盘中**实际失守 62.10**（日低 61.84）后收盘收回 **62.79（−1.61%）**，量 2.56M 较 8/12 的 3.38M **缩 24%**、无放量要件。这是**第二个「盘中失守-收盘收复」干净样本**（继 LNG 8/12）——收盘确认纪律再次避免在日低附近砍仓。判定：**持有**。
- **MP（判据「收盘 < 53.50 或 < 52.66 且放量」）→ 未确认**。收 **55.66（+2.86%）** 全书当日最大正贡献，日低 53.25 未及判据，收复本周两日整理跌幅。判定：**持有**。
- **MSFT（8/12 登记复核「第 3 日逆市收跌且收盘 < 491.52 → 列最弱仓候选」）→ 未触发**。收 **496.88（+0.90%）**，两日逆市走弱就此止住，复核条件解除，不列入最弱仓候选。

### 逐仓次日判据（2026-08-14 收盘可判定）

- **KTOS**：**官方收盘 < 61.84（8/13 低）或 < 61.34（8/11 低）且放量 → 按 ACT-003 评估减仓。** 市值 13,376.79 = **12.45% NAV，全书最大**，累计 **+33.77%**。HYP-002 观察：8/11 缩量新高（63.73）的 3 日回吐窗口 **8/14 收盘结束**——今收 62.79 已低于新高收盘，若 8/14 收盘 < 62.42（8/10 收盘＝新高前基准）则「回吐全部新高涨幅」成立，记入 HYP-002 支持样本；否则记不支持。
- **ETN**：**官方收盘 < 452.50（8/13 低）且放量 → ACT-003 评估减仓**；既有判据保留：连续两日收在 446.50 下方且放量 → 评估减仓。累计 +13.14%，8/12 长上影 + 8/13 缩量下跌，衰竭复核状态延续。
- **MP**：**官方收盘 < 53.25（8/13 低）或 < 52.66（8/10 低）且放量 → 按 ACT-003 评估。** 累计 +24.02%，收盘距德银下调后的目标 58 余 −4.0%。
- **LLY 失效线（建仓后第 4 个交易日，未触发）+ ⚠️ 明日除息校正**：**8/14 除息 $1.73**，全部判据按除息口径下修 $1.73 后裁定：突破失败线 **< 1183.98**（原 1185.71）、Q2 涨幅作废线 **< 1168.13**（原 1169.86）、失效线 **< 1113.95**（原 1115.68）。今日收 1209.00（−0.92%），距校正后突破失败线余 +2.11%。**质量标记转负**：量 1.90M 较 8/12 的 1.52M **放大 25%**，为入场以来首个放量下跌日——入场登记的「放量确认不足」隐忧升级为「放量方向为负」。当日无公司公告（最近事实仍是 8/12 起诉 retatrutide 黑市卖家）。
- **LNG 失效线（建仓后第 3 个交易日，未触发）**：**官方收盘 < 254.76** 不变（余量 −4.4%）；结构破坏线 **< 256.14**、首失守线 **< 262.01** 均不变（今日低 265.00 未及）。收 266.48（−0.61%）窄幅整理守住 265 一线。
- **MSFT 止损线（建仓后第 7 个交易日，未触发）**：**官方收盘 < 437.00** 不变，余量 **−12.05%**。今日 +0.90% 止住两日弱势，量 22.1M 较 8/12 的 27.3M 回落。
- **PWR（无待确认信号）**：收 **672.78（−0.77%）**，日内 671.64–684.87，量 803,917。无当日公司公告（最近事实仍是 8/7 KeyBanc 升级 Overweight 目标 807）。累计 +6.39%。
- **ABT（无待确认信号）**：收 **111.27（+0.32%）**，连续第 3 日走强，量 4.23M。无当日实质公司公告（最新实质进展仍是 8/11 Google Health 合作）。累计 +7.17%。

### 长期登记项

- **NVDA 离场后待验证（L-020，重要）**：8/11 以 217.50 平仓（realized −152.76）。**8/26 Q2 财报实际结果须回填账本 CLOSED 行与标的页**，检验「卖出全书最强基本面」的替换是否正确——替换方法论目前最贵的一次赌注。
- **GEV 离场后跟踪（非交易指令）**：8/10 以 990.85 平仓、已实现 −203.01。跟踪其相对 SPY 与相对 LLY 的后续表现，用于验证替换门 5 分阈值是否过于激进。
- **⚠️ 账务缺口（第 13 次登记，仍待用户裁定，本轮同样未擅改模型）**：C2 恒等式 `cash = initial − Σcost_basis + realized` **未建模股息**。已发生：ETN 2026-08-07 除息 $1.10 × 24.956686 股 = **$27.45**。明日发生：LLY 2026-08-14 除息 $1.73 × 8.117278 = **$14.04**，届时缺口累计 **$41.49**。修复需用户裁定口径（计入现金 / 计入已实现 / 不建模并显式标注），系统不单方面改账务模型。
- **⚠️ 技术指标缺口（第 4 次登记）**：MA20/MA50/MA200 自 2026-07-30 起未能刷新（`data/analytics.md` as-of 仍是 2026-07-27）。本晚 POST_CLOSE 消耗 AV 约 10 次（8 报价 + 1 国债 + 1 付费端点失败）。当前所有离场判据均为**收盘价与前低**的显式数值，不依赖均线，不阻断交易；均线一栏不得被当作现值引用。补救路径：明晨 MORNING 若配额余量足够则补算，或接入含 full 日线的源。
