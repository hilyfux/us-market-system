# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-13T04:53:00+08:00

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

## Pending close signals

> 纪律 L-015/L-016：每条离场判据都必须写成**次日收盘可判定的具体数值**，禁止凭形态印象决定；部分止盈时必须同时为剩余仓写下一档数值。以下为 **2026-08-12 POST_CLOSE 更新**（当日正式收盘 VERIFIED），供 2026-08-13 及之后的收盘逐日判定。

**本场基准**：SPY 772.47 +0.25%｜QQQ 723.70 +0.73%｜IWM 302.68 +0.56%｜VIX 14.55 −4.8%｜US10Y ⚠️ 当日收盘无核准源（官方日频最新 8/10=4.72%，盘中读得约 4.66–4.69%，显式标注不臆造）。7 月 CPI 与预期一致（同比 3.4%、核心 2.5%）。环境 **RISK_ON**（VIX 14.55 < 16，SPY 距 52 周高 776.85 仅 −0.57%），仓位上限 90%，当前仓位率 82.37% 未触顶。组合当日 **−0.07% vs SPY +0.25%（−0.32pp）**——8/11 替换对以来首个跑输日，两只逆市下跌仓（MSFT/MP）的美元亏损盖过六只上涨仓。

### 盘中标记的收盘裁定（ACT-002/003）

- **LLY（10:00 开盘报告 🚨 待收盘确认）→ 未确认**。判据「官方收盘 < 1185.71 即 8/10 突破失败」；实际收盘 **1220.28（+0.43%）**，高出判据 2.91%；日内最低 1191.08 一度距判据仅 0.45%，随后一路回升转涨。判定：**突破未失败，持有**。
- **LNG（15:30 提示守 265.16）→ 未确认**。早间盘中**曾实际失守**（日低 262.01），收盘 **268.11（+1.01%）** 收复并高出该线 1.11%。判定：**持有**。这是「盘中失守-收盘收复」的第一个干净样本——若按盘中价行动会在日低附近砍掉一个收涨的仓，收盘确认纪律（ACT-002/003）的价值被实测。
- **MP（15:30 提示守 52.90）→ 未确认**。判据「收盘 < 52.90（或 < 52.66）且放量」；实际收盘 **54.11（−2.05%）**，高出 52.90 判据 2.29%，日低 53.50 未及判据。判定：**持有**。
- **KTOS（衰竭判据第 4 轮登记，本轮判定＝未确认）**：判据「收盘 < 61.34 或 < 58.90 且放量」；实际收盘 **63.82（+0.14%）** 微创本轮收盘新高，日内 62.10–64.22。**量 3.38M 较 8/11 的 2.74M 放大 23%**——与 HYP-002「缩量新高」形态相反，该假设干净样本数维持 1。判定：**持有**。

### 逐仓次日判据（2026-08-13 收盘可判定）

- **KTOS**：**官方收盘 < 62.10（8/12 低）或 < 61.34（8/11 低）且放量 → 按 ACT-003 评估减仓。** 市值 13,596.22 = **12.63% NAV，全书最大**，累计 **+35.96%**；单只 20% 上限仍有余量。
- **MP**：**官方收盘 < 53.50（8/12 低）或 < 52.66（8/10 低）且放量 → 按 ACT-003 评估。** 连续第 2 个收跌日（−2.05%），量 5.55M 较 8/11 的 6.13M 略缩；8/12 公司参加 Canaccord 成长大会（既定日程，纪要谈探矿延寿与产能爬坡，无新财务指引）。累计 +20.57%。
- **LLY 失效线（建仓后第 3 个交易日，未触发）**：**官方收盘 < 1115.68** 不变，余量 **−8.57%**；突破失败线 **< 1185.71**、Q2 涨幅作废线 **< 1169.86** 均不变。今日 +0.43% 止住两连跌，但量 1.52M 继续萎缩（6.40M→2.92M→2.09M→1.52M）。当日公司事实：**起诉六家非法销售 retatrutide 黑市药的公司**并呼吁平台/支付方/监管协同封杀（公司 PR 8/12）——护城河防御动作，论点支持项，非离场条件。**⚠️ 8/14（后日）除息 $1.73**：当日收盘价将技术性下调约 0.14%，勿误读为走弱；若收盘贴近判据须先按除息口径校正再裁定。
- **ETN 冲高回吐后的新判据（本轮新登记）**：8/12 盘中 **478.00 创 52 周新高**后回吐几乎全部涨幅，收 **459.96（+0.15%）**，贴近日低 459.03（收在区间下沿 4.9% 处），量 1.64M。**次日判据：官方收盘 < 459.03（8/12 低）→ 按 ACT-003 进入衰竭复核；既有判据保留：连续两日收在 446.50 下方且放量 → 评估减仓。** 8/12 无公司公告。累计 +14.79%。
- **LNG 失效线（建仓后第 2 个交易日，未触发）**：**官方收盘 < 254.76** 不变，余量 **−5.02%**；结构破坏线 **< 256.14** 不变；**首次失守线前移至 < 262.01（8/12 低）**。今日已实测「盘中失守 265.16 后收盘收复」，CPI 与预期一致、利率回落对高杠杆结构友好。累计 +1.01%。
- **MSFT 止损线（建仓后第 6 个交易日，未触发）**：**官方收盘 < 437.00** 不变，余量 **−11.26%**。连续第 2 日逆市走弱（−2.26%，今日全书最弱，量 27.3M 放大），软件/芯片跷跷板日（SOX +2.49%）。当日消息：研究员公开 Windows 零日漏洞（TechCrunch）＝安全叙事、非财务披露；正面＝富国 PT 650→**700（街最高）**。无经营减值事实，ACT-002 要件不成立。**次日复核动作：若 8/13 连续第 3 日逆市收跌且收盘 < 491.52（8/12 低），MORNING 九维重评并列入最弱仓候选。** 累计 +1.02%。
- **PWR（无待确认信号）**：收 **678.02（+1.11%）**，午前冲高 695.51 后回落，量 1,012,521。无当日公司公告（最近事实仍是 8/7 KeyBanc 升级至 Overweight 目标 807）。累计 +7.22%。
- **ABT（无待确认信号）**：收 **110.91（+1.08%）**，贴近日高 111.28，连续第 2 日走强，量 6.50M。8/12 公司稿《We Give Blood》Big Ten 献血活动＝营销类 PR，非财务事实；最新实质进展仍是 8/11 与 Google 的血糖数据合作。累计 +6.82%。

### 长期登记项

- **NVDA 离场后待验证（L-020，重要）**：8/11 以 217.50 平仓（realized −152.76）。**8/26 Q2 财报实际结果须回填账本 CLOSED 行与标的页**，检验「卖出全书最强基本面」的替换是否正确——替换方法论目前最贵的一次赌注。
- **GEV 离场后跟踪（非交易指令）**：8/10 以 990.85 平仓、已实现 −203.01。跟踪其相对 SPY 与相对 LLY 的后续表现，用于验证替换门 5 分阈值是否过于激进。
- **⚠️ 账务缺口（第 12 次登记，仍待用户裁定，本轮同样未擅改模型）**：C2 恒等式 `cash = initial − Σcost_basis + realized` **未建模股息**。已发生：ETN 2026-08-07 除息 $1.10 × 24.956686 股 = **$27.45**。后日发生：LLY 2026-08-14 除息 $1.73 × 8.117278 = **$14.04**，届时缺口累计 **$41.49**。修复需用户裁定口径（计入现金 / 计入已实现 / 不建模并显式标注），系统不单方面改账务模型。
- **⚠️ 技术指标缺口（第 3 次登记）**：MA20/MA50/MA200 自 2026-07-30 起未能刷新（`data/analytics.md` as-of 仍是 2026-07-27）。今晚 AV 配额已重置并被 POST_CLOSE 结算消耗约 14 次（11 报价 + 1 国债 + 2 失败端点），MA 补算仍未执行。当前所有离场判据均为**收盘价与前低**的显式数值，不依赖均线，不阻断交易；均线一栏不得被当作现值引用。补救路径：明晨 MORNING 若配额余量足够则补算，或接入含 full 日线的源。
