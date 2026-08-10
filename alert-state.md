# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-11T04:55:00+08:00

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

## Pending close signals

> 纪律 L-015/L-016：每条离场判据都必须写成**次日收盘可判定的具体数值**，禁止凭形态印象决定；部分止盈时必须同时为剩余仓写下一档数值。以下为 2026-08-10 POST_CLOSE 登记、供 2026-08-11 及之后的收盘逐日判定。

- **KTOS 冲高衰竭（第 2 次登记，本轮判定＝未确认）**：8/10 收 **62.42（+2.72%）**，日内 58.90–63.17，收在区间上沿 83% 处，量 **4.10M 较前日 4.79M 收缩 14%**。登记条件两条均未触发（收盘 < 今日低 58.90 或 < 8/7 低 56.25 且放量）→ ACT-003 双要件不齐、CORE-004 禁止仅因涨幅止盈 → **持有**。**次日判据（沿用并前移）：官方收盘 < 58.90（8/10 低）或 < 56.25（8/7 低），且成交量放大 → 按 ACT-003 评估减仓。** 集中度登记：市值 13,297.97 = **12.44% NAV，全书最大**，累计 +32.98%；单只 20% 上限尚有余量。
- **MP 连涨后的高位判据（本轮判定＝未确认）**：8/10 收 **54.66（+6.95%）**，日内 52.66–55.67，量 10.53M。条件（收盘 < 8/7 低 48.17 或 < 今日低 52.66 且放量）未触发 → **持有**。**次日判据：官方收盘 < 52.66（8/10 低）或 < 48.17（8/7 低）且放量 → 按 ACT-003 评估。** 须显式记录的事实：**8/10 唯一有日期的公司相关消息是 Deutsche Bank 把目标价从 61 下调至 58（维持 Buy），没有任何正向公司公告**——+6.95% 属情绪/技术性反弹，同业 USAR 当日为负，不是板块行情。收盘 54.66 距被下调后的目标 58 仅 −5.8%，即价格已接近卖方新锚。
- **NVDA 失效线（建仓后第 2 个交易日，本轮判定＝未触发）**：失效条件 **官方收盘 < 200.75** 不变；8/10 收 **217.55（−2.86%）**，余量 **+8.36%**。当日事实：与 Apollo / BlackRock GIP / Blackstone / Brookfield / Goldman Sachs / KKR 组建独立算力融资平台、拟撬动 **>$500B 第三方资本**投向 AI 基建（CNBC/WSJ/FT 8/10），另有报道称拟向 Lancium 投入至多 $3B。**定性：这是第三方资金的融资载体，不是 NVDA 的资本开支、也不上 NVDA 资产负债表**；市场按「厂商融资式循环需求」解读而下跌（当日市值蒸发约 $1,300 亿）。**这属于资本配置与叙事争议，不构成经营层面减值**，ACT-002 的基本面要件不成立 → 持有。近端二元事件：**Q2 财报 2026-08-26（距 12 个交易日）**，进入 ≤5 个交易日窗口后按 L-002 只持有。
- **MSFT 止损线（建仓后第 4 个交易日，未触发）**：**官方收盘 < 437.00** 不变；8/10 收 **506.06（+1.21%）**，余量 **−13.6%**。当日增量：Maia 300 自研 AI 加速器据报秋季（可能 9 月）发布、2027 量产（The Information），Bernstein 目标价 647→660。论点（自研硅片＝AI 毛利率杠杆）强化。
- **GEV（全书唯一亏损仓，无退出信号）**：8/10 收 **990.85（+0.07%，累计 −2.03%）**，为连续 4 日跑输后**首次未跑输**大盘。无已核实的公司层面减值（Q2 订单 +88%、backlog $176B、「2030 年前基本售罄」、FY26 指引二次上调均未破）→ L-005 口径，不因价格弱势退出。九维仍为全书最弱，是下一轮替换比较的基准仓（门槛＝其分数 +5）。
- **PWR / ETN / ABT（无待确认信号）**：PWR 8/10 −1.62%（回吐 8/7 KeyBanc 升级至 Overweight、目标 807 的部分涨幅），ETN −0.82%，ABT +0.75%，均无新增负面硬事实、无触发条件。
- **⚠️ 账务缺口（第 9 次登记，仍待用户裁定，本轮同样未擅改模型）**：C2 恒等式 `cash = initial − Σcost_basis + realized` **未建模股息**；ETN 于 2026-08-07 除息 $1.10 × 24.956686 股 = **$27.45** 现金流入至今未入账。每次除息都会累积一次同类缺口。修复需用户裁定采用哪种口径（计入现金 / 计入已实现 / 不建模并显式标注），系统不单方面改账务模型。
