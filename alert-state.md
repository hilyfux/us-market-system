# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-15T00:37:30+08:00

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
| POSTCLOSE+2026-08-13 | 2026-08-14T04:53:49+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-13 | 2026-08-14T08:40:40+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-14 | 2026-08-14T20:38:16+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-14+0930 | 2026-08-14T21:37:28+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-14+1000 | 2026-08-14T22:14:37+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-14+1230 | 2026-08-15T00:36:05+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-14+1530 | 2026-08-15T03:35:47+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-14 | 2026-08-15T04:47:04+08:00 | enterprise_wechat | errcode=0 |

## Pending close signals

> 纪律 L-015/L-016：每条离场判据都必须写成**次日收盘可判定的具体数值**，禁止凭形态印象决定；部分止盈时必须同时为剩余仓写下一档数值。以下为 **2026-08-14 POST_CLOSE 更新**（当日正式收盘 VERIFIED），供 2026-08-17（周一）及之后的收盘逐日判定。

**本场基准**：SPY 776.34 −0.20%（自周四收盘新高小幅回落）｜QQQ 731.07 −0.14%｜IWM 305.06 +0.51%（小盘领涨日）｜VIX ⚠️ 当日收盘无核准源（Cboe 端点仅给 11:17 ET 盘中快照 14.49，盘中各读数 14.4–14.6；显式缺口不臆造）｜US10Y ⚠️ 官方日频最新 8/12=4.68%，显式缺口。环境 **RISK_ON 沿用**（最后核准 VIX 14.63 < 16；今晚唯一动作是减仓，上限不构成约束），仓位上限 90%，当前仓位率 77.34%。组合当日 **+1.08% vs SPY −0.20%（+1.28pp）**——终结连续 2 个跑输日，累计 +8.63% 创新高：此前两天拖累的中小盘题材腿（稀土/防务/电力/LNG）今日集体领涨，结构选择的对称面兑现。

### 盘中标记的收盘裁定（ACT-002/003）

- **ETN（判据「收盘 < 452.50 且放量」触发）→ 止盈-减仓50% 已执行**。收 **451.51（−0.40%）** 低于线 0.22%；量 1.391M 较 8/13 的 1.140M **放大 22%**——两要件齐。佐证：自 8/12 冲高 478 起连续第 3 个收跌、收在昨日低点下方、且同论题 PWR 当日 +1.93%（8/13 的「板块轮动」解释今日不成立）。与 BE 8/7 先例同形（登记条件 + 放量 + 冲高失败）。成交 2026-08-14-ETN-止盈减仓50-01 @451.51，realized +634.10；剩余 12.478343 股（$5,000 成本基，SIZE_EXCEPTION）。
- **LLY（判据「收盘 < 1183.98（除息校正后突破失败线）」触发）→ 突破失败确认，持有**。今日除息 $1.73，收 **1180.16**（原始口径 −2.39%／除息口径 −2.25%），低于线 0.32%——**8/10 入场时的突破正式宣告失败**。日低 1171.20 距 Q2 涨幅作废线 1168.13 仅 0.26%。量能两源冲突（stockanalysis 1.77M＝缩 7% vs AV 2.11M＝放 11%），量能要件记不可判。突破失败线是复核触发器、不是止损（失效线 1113.95 余 −5.6%）→ 动作=持有，**明晨九维重评按最弱仓候选处理、扣动量分**。
- **KTOS（判据「收盘 < 61.84 或 < 61.34 且放量」）→ 未触发；HYP-002 窗口裁定＝不支持**。特朗普无人机进口关税消息（Barron's，板块催化非公司公告）推动高开 66.00、冲 67.10 后回落收 **64.58（+2.85%）**，量 5.43M **放大 112%**，为新的最高收盘。8/11 缩量新高的 3 日回吐窗口今收盘裁定：64.58 高于 62.42 基准 +3.46% → **回吐不成立，记 HYP-002 不支持样本**。
- **MP（判据「收盘 < 53.25 或 < 52.66 且放量」）→ 未触发**。稀土/关键矿产板块行情（盘中已核实无当日公司公告，L-018 无信息波动）收 **58.74（+5.53%）**，盘中冲 61.11 回落，量 10.79M 显著放大；收盘已高于德银目标价 58。

### 逐仓次日判据（2026-08-17 收盘可判定）

- **ETN（剩余半仓）**：**官方收盘 < 449.01（8/14 低）且放量 → 评估再减仓/平仓**；「连续两日收在 446.50 下方且放量 → 评估」判据保留。累计 +12.68%，衰竭序列已兑现一次减仓，剩余仓按阶梯管理。
- **KTOS**：**官方收盘 < 62.65（8/14 低）→ 衰竭复核；< 62.42（8/10 收盘基准）且放量 → ACT-003 评估减仓。** 关税催化日放量冲高回落（收在日区间下半段），需数值化盯防。市值 13,758.14 = **12.67% NAV，全书最大**，累计 **+37.58%**。
- **MP**：**官方收盘 < 56.15（8/14 低）且放量 → ACT-003 评估减仓。** 放量冲高回落 + 收盘已越过德银目标 58，与 KTOS 同待收盘检验。累计 +30.88%。
- **LLY（突破失败已确认）**：**官方收盘 < 1168.13 → Q2 涨幅作废确认（除息口径），明晨列替换候选优先级最高**；失效线 **< 1113.95** 不变（余 −5.6%）。累计 −4.20% 全书最弱。
- **LNG 失效线（建仓后第 4 个交易日，未触发）**：**官方收盘 < 254.76** 不变（余量 −6.2%）；结构破坏线 **< 256.14**、首失守线 **< 262.01** 均不变。收 271.64（+1.94%）为入场以来最高收盘。
- **MSFT 止损线（建仓后第 8 个交易日，未触发）**：**官方收盘 < 437.00** 不变，余量 **−11.79%**。收 495.40（−0.30%）窄幅整理。
- **PWR（无待确认信号）**：收 **685.78（+1.93%）**，日内 672.09–692.09，量 692,663。无当日公司公告。累计 +8.44%。
- **ABT（无待确认信号）**：收 **111.25（−0.02%）**，持平整理，量 5.57M。无当日实质公司公告。累计 +7.15%。

### 长期登记项

- **NVDA 离场后待验证（L-020，重要）**：8/11 以 217.50 平仓（realized −152.76）。**8/26 Q2 财报实际结果须回填账本 CLOSED 行与标的页**，检验「卖出全书最强基本面」的替换是否正确——替换方法论目前最贵的一次赌注。
- **GEV 离场后跟踪（非交易指令）**：8/10 以 990.85 平仓、已实现 −203.01。跟踪其相对 SPY 与相对 LLY 的后续表现，用于验证替换门 5 分阈值是否过于激进。
- **⚠️ 账务缺口（第 14 次登记，仍待用户裁定，本轮同样未擅改模型）**：C2 恒等式 `cash = initial − Σcost_basis + realized` **未建模股息**。已发生：ETN 2026-08-07 除息 $1.10 × 24.956686 股 = **$27.45**（除息时点全仓在手）；LLY 2026-08-14 除息 $1.73 × 8.117278 = **$14.04**（今日发生）。缺口累计 **$41.49**。修复需用户裁定口径（计入现金 / 计入已实现 / 不建模并显式标注），系统不单方面改账务模型。
- **⚠️ 技术指标缺口（第 5 次登记，部分修复）**：MA20/MA50/MA200 自 2026-07-30 起未能全量刷新（8/14 MORNING 已补 ETN MA20/50）。当前所有离场判据均为**收盘价与前低**的显式数值，不依赖均线，不阻断交易。本晚 POST_CLOSE 消耗 AV 约 12 次（配额今晚已复位：8 报价 + 3 基准 + 1 国债；INDEX_DATA 付费端点仍拒）。补救路径：明晨 MORNING 配额余量足够则继续补算。
- **⚠️ VIX 收盘核准缺口（2026-08-14 新增）**：8/14 VIX 收盘无核准源（Cboe 端点在结算时点仍返回 11:17 ET 盘中快照；AV INDEX_DATA 为付费端点）。盘中读数 14.4–14.6 一致低于 16，环境判定不受影响；后续结算若复现，考虑加入第二 VIX 源。
