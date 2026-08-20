# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-21T04:52:00+08:00

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
| PREMARKET+2026-08-20 | 2026-08-20T20:37:49+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-20 | 2026-08-21T04:51:38+08:00 | enterprise_wechat | errcode=0 |
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
| MORNING+2026-08-14 | 2026-08-15T08:46:59+08:00 | enterprise_wechat | errcode=0 |
| HEARTBEAT+2026-08-15 | 2026-08-15T20:03:23+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-17 | 2026-08-17T20:37:05+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-17+1000 | 2026-08-17T22:06:24+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-17+1230 | 2026-08-18T00:36:56+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-17+1530 | 2026-08-18T03:39:38+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-17 | 2026-08-18T04:46:53+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-17 | 2026-08-18T08:40:47+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-18 | 2026-08-18T20:42:16+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-18+1000 | 2026-08-18T22:09:10+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-18+1230 | 2026-08-19T00:37:08+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-18+1530 | 2026-08-19T03:39:30+08:00 | enterprise_wechat | errcode=0 |
| POSTCLOSE+2026-08-18 | 2026-08-19T04:46:06+08:00 | enterprise_wechat | errcode=0 |
| MORNING+2026-08-18 | 2026-08-19T08:45:01+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-19 | 2026-08-19T20:37:34+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-19+0930 | 2026-08-19T21:39:48+08:00 | enterprise_wechat | errcode=0 |
| INTRADAY+2026-08-19+1000 | 2026-08-19T22:13:56+08:00 | enterprise_wechat | errcode=0 |
| PREMARKET+2026-08-20 | 2026-08-20T20:37:49+08:00 | enterprise_wechat | errcode=0 |

## Pending close signals

> **⚠️ 離場判定の照合口径＝公式收盘（official close < X，用户裁定で確定）**：以下の判据に書かれた閾値は既存の官方收盘ベースの建て値で、**次日の正式收盘で逐日判定する**（POST_CLOSE の検証も正式收盘）。2026-08-17 の口径統一で一時 CLOSING 窓の盤中価に読替えたが、「この価格は取引専用であり翌日の取引戦略分析には含まれない・取引価格とポジション保有成本にのみ影響を与える」との用户裁定で過剰と判断され**差し戻し**——離場判定は従来どおり公式收盘（約定フィル価格が引け20分前価であることは離場判定には影響しない）。数値閾値は一切改変しない（下記のまま維持）。

> 纪律 L-015/L-016：每条离场判据都必须写成**次日收盘可判定的具体数值**，禁止凭形态印象决定；部分止盈时必须同时为剩余仓写下一档数值。以下为 **2026-08-17 POST_CLOSE 更新**（当日正式收盘 VERIFIED），供 2026-08-18（周二）及之后的收盘逐日判定。

**本场基准**（2026-08-17 收盘，当晚 VERIFIED）：SPY 772.67 −0.47%（日内 772.51–776.78）｜QQQ 729.87 −0.16%｜IWM 304.06 −0.34%｜VIX ⚠️ 暂值 15.03（Cboe 延迟报价 16:08 ET 戳，+0.78 vs 前收 14.25 自洽；早于 16:15 结算＝未定稿，次晨定稿页回补）｜US10Y ⚠️ 官方日频未及 8/17（盘中 TE ~4.727%，内部记录）。环境 **RISK_ON 沿用**（VIX 各读数 < 16；SPY 远高于 50/200 日参考线），仓位上限 90%，当前仓位率 77.70%。组合当日 **−0.15% vs SPY −0.47%（+0.32pp）**，累计 +8.47%（距 8/14 ATH −0.16pp）；无交易，替换冻结中（CLOSING 窗发火无执行指令）。

### 盘中标记的收盘裁定（ACT-002/003）——2026-08-17 五项全部未确认

- **MP（判据「收盘 < 56.15 且放量」）→ 未确认**。盘中低 56.14 触线，收 **58.51（−0.39%）** 高于线 +4.2%；量 5.50M 较 8/14 的 10.79M **缩 49%**——两要件皆不成立。收盘确认纪律第 3 个「盘中失守-收盘收复」正样本（盘中卖出会在全书第二大浮盈上过早离场）。
- **ETN（判据「收盘 < 449.01 且放量」）→ 未确认**。盘中低 449.00 触线，收 **455.40（+0.86%）** 高于线 +1.4%；量 1.53M 较 1.39M +10%，价要件不成立。第 4 个「盘中失守-收盘收复」正样本。Trane 数据中心合作官方稿为当日公司事实。
- **KTOS（判据「< 62.65 复核／< 62.42 且放量」）→ 未触发**。收 **63.29（−2.00%）**，日低 62.88 > 62.65；量 3.39M 较 5.43M **缩 38%**——连续第二日缩量回落，无衰竭确认（CORE-004 不因回落本身卖出）。GEK800 获军用编号 F143-ZZ-100 + JASSM EMD 合同（公司官方稿，当日持仓中唯一公司事实利好）vs Truist 135→104 下调。
- **LNG（首失守线 262.01，信息性）→ 未触及**。收 **266.93（−1.73%）**，日低 264.74。Mizuho 273→300 上调，无公司利空。
- **MSFT（无判据线，仅记录）**：收 **480.35（−3.04%）**，量 28.3M 放大；Guardian「2.2M 芯片缺口」调查发酵 vs WF $700/JPM $625 上调对冲。**未实现转负 −1.46%，成全书唯一亏损仓**——明晨九维按最弱仓候选处理（分析侧结论，非交易指令）。止损线 437 余 −9.0%。

### 逐仓次日判据（2026-08-18 收盘可判定）

- **PWR**：**官方收盘 < 690.51（8/17 低）且放量 → 衰竭复核（信息性）**。今日 +5.33% 放量 +107% 创入场以来最高收盘（无当日公司公告，KeyBanc 升级延续发酵）——大阳线次日的对称盯防；CORE-004 不因涨幅本身卖出。累计 +14.22%，市值 11,421.85 = 10.53% NAV（全书第三）。
- **KTOS**：**官方收盘 < 62.88（8/17 低）→ 衰竭复核；< 62.42（8/10 收盘基准）且放量 → ACT-003 评估减仓。** 市值 13,483.31 = **12.43% NAV，全书最大**，累计 +34.83%。
- **MP**：**官方收盘 < 56.14（8/17 低）且放量 → ACT-003 评估减仓。** 累计 +30.38%，市值 13,037.67 = 12.02% NAV（第二）。
- **ETN（剩余半仓）**：**官方收盘 < 449.00（8/17 低）且放量 → 评估再减仓/平仓**；「连续两日收在 446.50 下方且放量 → 评估」判据保留。累计 +13.65%（SIZE_EXCEPTION 半仓）。
- **MSFT 止损线（建仓后第 9 个交易日，未触发）**：**官方收盘 < 437.00** 不变，余量 **−9.02%**。**8/20 除息 $0.91/股**（届时 C2 股息缺口第三次发生，+$18.67，仍待用户裁定口径）。
- **LNG 失效线（建仓后第 5 个交易日，未触发）**：**官方收盘 < 254.76** 不变（余量 −4.6%）；结构破坏线 **< 256.14**、首失守线 **< 262.01** 均不变。
- **TSM（建仓后第 1 个交易日，未触发）**：**失效线 official close < 406.11**（余量 −5.8%）；**首失守复核线 < 424.10（8/14 低，信息性）**。首日收 430.97（+1.08%）高于建仓价 426.35；日低 426.80 未触任何线。
- **ABT（无待确认信号）**：收 **110.37（−0.79%）**，随大盘回落，量 9.84M；无当日实质公司公告（NACHC 营养合作为营销类 PR）。累计 +6.30%。

### 长期登记项

- **NVDA 离场后待验证（L-020，重要）**：8/11 以 217.50 平仓（realized −152.76）。**8/26 Q2 财报实际结果须回填账本 CLOSED 行与标的页**，检验「卖出全书最强基本面」的替换是否正确——替换方法论目前最贵的一次赌注。8/17 快照：NVDA 收 225.01（离场后 **+3.45%**）vs 接替腿 LNG +0.57% → delta **−2.89pp**。
- **GEV 离场后跟踪（非交易指令）**：8/10 以 990.85 平仓、已实现 −203.01。跟踪其相对 SPY 与相对 LLY 的后续表现，用于验证替换门 5 分阈值是否过于激进。8/17 快照：GEV 收 1079.00（离场后 **+8.90%**）vs 接替腿 LLY **−3.96%** → delta **−12.85pp，全部 5 组替换对中最重反例**。
- **LLY 离场后跟踪（L-020，2026-08-15 新增）**：8/14 收盘价 1180.16 平仓（realized −420.31，−4.20%）。跟踪相对 SPY 与相对 TSM 表现；**orforglipron FDA 决议为其最大后续催化**，若离场后大涨须如实计入替换方法论反例档案。本次为 +5 恰在边界的替换（第 5 次执行），是 5 分阈值审计的关键样本。8/17 快照：LLY 收 1183.16（离场后 **+0.25%**）vs 接替腿 TSM **+1.08%** → delta **+0.83pp，5 组中唯一正值**。
- **⚠️ 账务缺口（第 15 次登记，仍待用户裁定，本轮同样未擅改模型）**：C2 恒等式 `cash = initial − Σcost_basis + realized` **未建模股息**。已发生：ETN 2026-08-07 除息 $1.10 × 24.956686 股 = **$27.45**（除息时点全仓在手）；LLY 2026-08-14 除息 $1.73 × 8.117278 = **$14.04**（今日发生）。缺口累计 **$41.49**；**MSFT 8/20 除息 $0.91 × 20.514504 = $18.67 将成第三笔**（届时累计 $60.16）。修复需用户裁定口径（计入现金 / 计入已实现 / 不建模并显式标注），系统不单方面改账务模型。
- **✅ 技术指标缺口（2026-08-15 MORNING 关闭 MA20/50）**：ABT 106.13/97.28、LNG 262.31/251.36、LLY 1180.37/1167.86（AV SMA 端点，as-of 8/14）——8 仓 MA20/50 欠账清零（TSM 由本晨 50 日收盘实算 412.14/425.16）。**MA200 需付费 full 端点，维持显式缺口**，判据不依赖均线、不阻断交易。
- **✅ VIX 收盘核准缺口（2026-08-15 MORNING 关闭）**：Cboe 定稿页（Trade Data as of August 14, 2026, data as of 8:15 PM）给出 8/14 收盘 **14.25（−0.38，与前收 14.63 自洽）** → 缺口回补，RISK_ON 以确定性输入重确认。教训沿用：结算时点（T+50min）Cboe 尚未定稿，**次晨回补是该源的标准路径**（与「历史页次晨回补」同型）；结算轮若再缺，登记缺口即可、无需当晚强取。**⚠️ VIX 8/17 同型缺口在册**：结算轮 Cboe 延迟报价 15.03（16:08 ET 戳，早于 16:15 结算），暂值自洽但未定稿，次晨（8/18 MORNING）按定稿页回补。**⚠️ US10Y 8/17 官方日频未及**（盘中 TE ~4.727% 仅内部记录），缺口沿用。


## MORNING 2026-08-18（估值 2026-08-17）——缺口回补 + 九维重评/扫描，无交易

- ✅ **VIX 8/17 定稿回补（昨晚在册缺口关闭）**：Cboe 延迟报价 16:15:01 结算戳 close **15.19（+0.94，与前收 14.25 精确自洽）**；昨晚暂值 15.03（16:08 戳）作废，8/17 正式收盘以 **15.19** 为准。环境 **RISK_ON 重确认**（15.19 < 16；SPY 772.67 远高于 50 日参考线），上限 90%，仓位率 77.70%。
- ✅ **US10Y 8/17 官方日频回补（昨晚在册缺口关闭）**：财政部日频 **4.72%**（8/14=4.68 → +4bp；20Y 5.30 / 30Y 5.31，长端抬升）。
- **九维重评（估值 8/17）**：LNG 84 · MSFT 82 · PWR 82 · ETN 81 · TSM 81 · KTOS 79 · MP 79 · **ABT 78（总分最弱）**。MSFT 昨晚预告的最弱仓候选处理完成：84→82（放量下跌、情绪扣分），但公司已否认芯片供给问题（Nadella：芯片在库、瓶颈为机房与电力）＝业务论点未破坏，论点侧排序非最弱。
- **全市场扫描（8 候选 / 7 主题 / 7 行业，催化窗 8/10–8/17）**：**AMAT 82**（8/13 Q3 纪录营收 $9.12B beat + Q4 指引 9.75–10.75B；8/17 +5.61% 收 ~507 ＝盘后回吐后的事件后确认收盘；**单源，未双源核实**）/ AVGO 81（9/2 财报 ~10 交易日）/ ANET 80 / RTX 78 / CVX 77 / GE 76 / GS 76 / ISRG 74。零售股（HD/TGT/LOW/WMT）本周财报＝事件临近不入围。
- **替换判定：不替换，全体持有**。最强候选 AMAT 82 vs 最弱 ABT 78 分差 +4，远低于所需；且替换冻结中（解冻条件＝8/26 NVDA 回填 + L-020 入档），MSFT（第10日）/LNG（第6日）/TSM（第2日）均在最低持有期内。无交易、不落账。
- **逐仓次日判据**：8/17 POST_CLOSE 登记的全部沿用不变（PWR <690.51 放量·信息性｜KTOS <62.88 复核、<62.42 放量评估｜MP <56.14 放量评估｜ETN <449.00 放量评估再减、双日 <446.50｜MSFT 止损 <437.00｜LNG 失效 <254.76｜TSM 失效 <406.11、复核 <424.10｜ABT 止损 <95.86）。
- **宏观周历（晨间核实）**：8/18 新屋开工/营建许可 08:30 ET、进出口价格 08:30、工业产出 09:15；**8/19 FOMC 7 月会议纪要**；零售财报周（HD/TGT/LOW/WMT，均非持仓）；**Jackson Hole 8/27–29（Warsh 首次主题演讲）**。
- 长期登记项不变：NVDA 8/26 回填（L-020）、GEV/LLY 离场后跟踪、股息账务缺口累计 $41.49（MSFT 8/20 除息 $0.91 将成第三笔，仍待用户裁定）、MA200 显式缺口。


## POST_CLOSE 2026-08-18（结算 PARTIAL：钱包估值未推进，次晨回补）——收盘裁定 + 次日判据

### 盘中/前日登记判据的收盘裁定（官方收盘 8/18，ACT-002/003）

- **ETN（判据「收盘 < 449.00 且放量 → 评估再减仓」）→ 两要件成立，评估确认**。收 **431.33（−5.29%）**，量 1.71M 较 8/17 的 1.53M **+12% 放量**；同日 VRT −6.8%、NVT −7.1%＝电力设备板块集体回调，公司层面无利空（Aerospace 总裁任命、昨日 Trane 合作均非负面）。**按 v2.18 阶段边界，POST_CLOSE 不执行交易**：明晨 MORNING 九维复核后决定，如减仓在 8/19 CLOSING 执行落账。「连续两日 < 446.50」判据今日为第 1 日（431.33）。
- **TSM（复核线 < 424.10 信息性）→ 触发**。收 **413.41（−4.07%）**，日低 410.77 **未触** 406.11 失效线（余量 −1.8%）；半导体普跌（MU −7.0%）。持有，明晨重点复核；建仓第 3 个交易日、最低持有期内（第 3/15 日）。
- **PWR（<690.51 且放量·信息性）→ 未确认**。盘中低 688.38 触线，收 **696.15（−3.62%）** 高于线；量 1.536M 基本持平。第 5 个「盘中失守-收盘收复」正样本。
- **MP（<56.14 且放量）→ 未确认**。盘中低 55.60 破线，收 **56.67（−3.14%）** 收复；量 4.71M 较 5.50M **缩 14%**——两要件皆不成立。第 6 个「盘中失守-收盘收复」正样本。
- **KTOS（<62.88 复核 / <62.42 且放量评估）→ 复核触发、评估未确认**。收 **61.99（−2.05%）** 低于两线，但量 2.75M 较 3.39M **缩 19%**＝量能要件不成立（连续第三日缩量回落）。USMC Valkyrie BLOS 演示为当日公司事实利好。持有。
- **MSFT / ABT / LNG**：无判据触发。MSFT 收 481.63（+0.27%）逆科技板块收红；ABT 收 112.68（+2.09%）当日全书最佳；LNG 收 273.78（+2.57%）**创入场以来最高收盘**（Argus PT→330、Mizuho→300、UBS→340）。

### 逐仓次日判据（2026-08-19 收盘可判定）

- **ETN（评估已确认，待明晨复核）**：明晨九维复核减仓与否；**官方收盘 < 428.90（8/18 低）且放量 → 升级评估平仓**；「连续两日 < 446.50」今日已计第 1 日。
- **TSM**：失效线 **official close < 406.11** 不变（余量 −1.8%）；复核线移至 **< 410.77（8/18 低）**。
- **PWR**：**< 688.38（8/18 低）且放量 → 衰竭复核（信息性）**。
- **MP**：**< 55.60（8/18 低）且放量 → ACT-003 评估减仓**。
- **KTOS**：**< 61.00（8/18 低）→ 复核**；**< 62.42 且放量 → ACT-003 评估减仓**（保留）。
- **MSFT**：止损 **< 437.00** 不变（余量 −9.3%）；**8/20 除息 $0.91**（第三笔股息缺口 +$18.67 将发生，累计将达 $60.16，仍待用户裁定口径）。
- **LNG**：失效 **< 254.76**、结构破坏 **< 256.14**、首失守 **< 262.01** 均不变。
- **ABT**：止损 **< 95.86** 不变。

### 数据与估值状态（内部）

- **8/18 结算 = PARTIAL**：8/8 收盘价均取自 stockanalysis 详情页（全部「At close: Aug 18, 2026, 4:00 PM EDT」戳、同源自洽、prev 锚定 8/17 全对）；第二源 6/8 达成（PWR=AV 0.006%｜MP/MSFT/ETN/TSM=Google Finance 0.00%｜KTOS=stockscan 0.00% 当日戳）；**ABT/LNG 二源不可得**（AV 日配额耗尽、Google 旧缓存/盘中快照、stockscan LNG 冻结于 8/17、roic 未结算盘中价、stocktitan 空响应）→ 按 P1 与「valuation_date 只指 VERIFIED」规则，**钱包估值维持 2026-08-17**，8/18 mark-to-market 与影子帐簿快照（NVDA/LLY/GEV/BE/RMBS）延至 8/19 MORNING 历史页法回补后完成。
- **VIX 8/18 暂值 15.67**（Cboe 延迟报价 16:20:32 戳，prev 15.19 精确自洽）→ RISK_ON 维持（<16），**距 16 边界仅 0.33**——若明日破 16 → 上限降 75%，当前仓位率 77.4% 将成约束；次晨定稿页确认。**US10Y 8/18 官方日频未及**（缺口沿用）。SPY/QQQ/IWM 双源未取，次晨一并回补。
