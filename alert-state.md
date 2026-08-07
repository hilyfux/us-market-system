# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-08T04:55:00+08:00

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

## Pending close signals

- **BE 高位破位收盘确认（2026-08-07）— 触发并已执行 止盈-减仓50%**：官方收盘 **219.34（−4.20%）同时跌破 8/5 低 222.59 与 8/6 低 221.21**，即 8/6 登记的两条数值触发条件全中。质地佐证：日内冲高 240.18 后收在日低区（距日高 −8.7%）、成交 **14.75M 放量**（8/6 11.84M / 8/5 13.22M）、收盘低于 8/4 收盘 228.11 —— 8/6 判定持有的三条理由今日全部反转。ACT-003 双要件齐备（盈利 +6.07% ＋ 收盘确认的高位风险）→ **卖出 24.179084 股 @219.34（trade 2026-08-07-BE-止盈减仓50-01），realized +303.44**。论点未破（AI 分布式电源；8/6 MiTAC 合作扩大）→ 减半而非平仓；剩余 24.179084 股带 SIZE_EXCEPTION 标记继续持有。**SIGNAL CLEARED。** 后续观察：若收盘再跌破 212.20（8/7 低）→ 按 ACT-002/003 复评剩余半仓；若收复 228.11（8/4 收盘）以上则视为破位失败。
- **MP Q2 价格确认（2026-08-07）— CLEARED（基本面 + 价格双确认）**：收 **51.11 +7.62%**（日内 48.17–53.47，量 12.27M ≈ 前日 2 倍），是 8/6 盘后 Q2 超预期（营收 $108.49M vs 共识 $95.95M、adj EBITDA 首次转正 +$28.5M）的收盘价格确认。📊 前瞻 beat_confirm 命中已回填 decision-log 与标的页。ACT-005 封锁解除，动作＝持有（无衰竭收盘，CORE-004 不按涨幅止盈）。当日增量：Trump 在国务院召集矿业 CEO 谈国防关键矿产供应链（Reuters 8/7）。
- **KTOS 强势延续（2026-08-07）— 无待确认项**：收 **60.77 +5.85%**（日内 56.25–61.09，收在日高附近），Javelin 下一代导引头合同（8/6）后的第二日跟进；累计 +29.46%，全书最强仓。ACT-003 不触发 → 持有。
- **ETN 除息日（2026-08-07）— 无衰竭**：$1.10 除息日仍收 **448.65 +0.10%**（技术性下调后仍收涨）→ ACT-003 不触发，持有。⚠️ 账务（**仍待用户裁定，本次未擅改模型**）：C2 恒等式未建模股息，24.956686 × $1.10 = **$27.45** 现金流入未入账；今日 ETN 收涨故无可见净值损耗，但该缺口会随每次除息累积。
- **GEV 累计亏损延续（2026-08-07）**：收 **990.11 −1.02%**，日内 963.55–1013.20，累计 **−2.10%**，组合唯一亏损仓、连续第 3 日跑输。业务面未破（Q2 订单 +88%、backlog $176B、FY26 指引二次上调）→ 情绪/估值回吐 ≠ 公司破坏（L-005），持有。若出现收盘确认的论点破坏按 ACT-002 评估。
- **MSFT 建仓第 2 日（2026-08-07）**：收 **499.99 +0.03%**（日内 498.7–505.2），累计 +2.57%；止损计划 <437.00 未触及、距现价 −12.6% → 持有。确定性替换样本 2，仍不据小样本下结论。
- **2026-08-07 settlement — VERIFIED same night**（T+~50min，恢复当晚结算）：8/8 双源，最大跨源偏差 0.39% ≤1%（AV GLOBAL_QUOTE 4 名 + stockanalysis At-close 戳 4 名，互为交叉核对；stockscan 结算日线为第二源）；valuation_date → 2026-08-07；wallet **105,917.66（+1,017.55，+0.97% vs SPY +0.61% → +0.36pp）**；**累计 +5.92%，连续第 5 日新高**；C1–C7 diff ≤0.000001、W1 lag=0。**1 笔成交**（BE 止盈-减仓50%）。环境 **RISK_ON**（VIX 15.30 < 16；SPY 773.26 创收盘新高，远在 MA50 上方）→ 上限 90%，仓位率 82.32% → **77.31%**，槽位 8/8。数据缺口：VIX 与 US10Y 今晚仅单源（TradingEconomics）= PARTIAL，已登记 data/post-close.md。

- MP Q2（2026-08-06 盘后）— **CLEARED（基本面 beat_confirm）2026-08-07 离线补结算**：营收 $108.49M vs 修正共识 $95.95M（+13.1%，YoY +89%）、adj EPS −$0.01 vs 共识 ~0.00、**adj EBITDA +$28.5M 转正（YoY +$41.0M）**；NdPr 产销与售价齐升、重稀土分离与磁材爬产、新增长期钆供应协议 → 📊 前瞻 beat_confirm 命中，已回填 decision-log 与标的页。ACT-005 财报封锁解除。**价格确认待 8/7 官方收盘**（8/7 盘前 49.39 +4.00%，盘前价不入账、不触发动作）。
- KTOS 8/5 冲高衰竭收盘确认 — **CLEARED（无衰竭）2026-08-06 收盘**：8/6 收 57.41 +3.74%，远高于昨收 55.34、距日高 59.095 仅 −2.85% → ACT-003 不触发，持有。增量正向硬事实：美陆军 Javelin 下一代导引头合同（GlobeNewswire 官宣）。
- **BE 高位回落收盘复核（2026-08-06）— 未触发，转 8/7 收盘观察**：8/6 冲高 249.45 后收 228.96（−2.29%，距日高 −8.2%）。ACT-003 判据未满足——收盘未跌破前日（8/5）低点 222.59、亦高于 8/4 收盘 228.11，且回落伴**缩量**（11.84M < 8/5 13.32M < 8/4 18.85M）→ 持有。**触发条件（8/7 官方收盘）**：收盘 < 222.59（8/5 低）或 < 221.21（8/6 低）即构成收盘确认的高位破位 → 按 ACT-003 评估减仓。
- BE 盘前弱势（2026-08-06 PREMARKET_RISK）— **方向被收盘证实（首个非误报样本）**：盘前 −3.49% → 盘中 V 型收复至 +1.01% → 收 228.96 −2.29%。方向对但**非价格破坏**（未破前日低、未破 8/4 收盘），维持持有；L-005「情绪≠破坏」判定不变，但盘前信号的样本库须记入本次「方向命中/幅度温和」一类。
- BE 诉讼「已立案观察」（2026-08-05 起）— **状态不变**：8/6 无公司实质财务影响的新披露、无收盘价格破坏 → 持有。减仓评估仍需②公司披露实质影响 或 收盘价格破坏确认（ACT-002）。
- ETN 52 周高复核（2026-08-06）— 第 **4** 日盘中新高 457.78、收 448.19（+0.20%）收涨无衰竭 → ACT-003 不触发，持有（CORE-004）。**今日 8/7 除息 $1.10**：收盘技术性下调约 −0.25%，勿误读为衰竭。⚠️ 账务：C2 恒等式未建模股息，$27.45 现金流入若不入账将在 8/7 结算表现为凭空净值损耗——**待用户裁定**，本次未擅改账务模型。
- MSFT 建仓首日结算（2026-08-06）— 收 499.86 +2.54%（未实现 +254.38），止损计划 <437.00 未触及、距现价 −12.6% → 持有。确定性替换首日为正贡献，样本 1，不据单日下结论。
- GEV 累计转负（2026-08-06）— 收 1000.30 −1.73%，跌破成本基 1011.38（累计 −1.10%，组合唯一亏损仓）。无已核实公司减值（Q2 订单 +88%/backlog $176B/FY26 指引二次上调论点未破）→ 情绪回吐 ≠ 公司破坏（L-005），持有；后续若出现收盘确认的论点破坏按 ACT-002 评估。
- **2026-08-06 settlement — VERIFIED（离线补结算，非当晚）**：8/8 双源 0.00%（Alpha Vantage GLOBAL_QUOTE + stockanalysis 比较工具，收盘/涨跌幅/成交量三项逐股精确一致）；valuation_date → 2026-08-06；wallet **104,900.12**（+167.34，+0.16% vs SPY −0.16% → +0.32pp）；**累计 +4.90%，连续第 4 日新高**；C1–C7 diff ≤0.000002、W1 lag=1（补结算后回到上限内）。**无交易**。缺口：本次结算因宿主机额度耗尽导致的定时任务停摆而未在当晚完成，已在 data/post-close.md 缺口表登记并关闭。
- KTOS 8/5 收盘价格确认 — **CLEARED（无衰竭收盘）2026-08-05 POST_CLOSE**：收 55.34 +6.69%（日高 62.34 回落 ~11.2% 留长上影，但收盘远高于昨收 51.87）→ 冲高衰竭未获收盘确认，ACT-003 不触发 → 持有，次日常规复核。
- ETN 52 周高复核（2026-08-05）— 第 3 日盘中新高 453.50、收 447.28（+0.56%）收涨无衰竭 → ACT-003 不触发，持有（CORE-004）。注意 8/7 除息 $1.10（收盘价将技术性下调，勿误读为衰竭）。
- BE 诉讼升级半触发（2026-08-05）— 集体诉讼**已由股东正式立案**（Bernstein Liebhard 8/4 官宣、多家律所 8/1 起诉状）：升级条件①法院立案＝满足；②公司披露实质财务影响＝未满足；收 234.33 +2.73% 无价格损伤 → 维持持有，状态「招揽噪声」→「已立案观察」；减仓评估需②成立或收盘价格破坏确认（ACT-002）。
- 2026-08-05 settlement — **VERIFIED same night**（连续第四晚）：8/8 双源 0.00–0.07%（stockanalysis At-close + AV 4 名/GF-beta 4 名）；valuation_date → 2026-08-05；wallet 104,732.78；C1–C7 diff=0；W1 lag=0；**累计 +4.73% 连续第 3 日新高**；环境 CHOPPY→RISK_ON（VIX 15.81），仓位率 80.74% 回上限内。No trades。MP Q2 明晚盘后（共识营收修正 ~$96M）。
- KTOS Q2（2026-08-04 盘后）— **CLEARED（基本面双超）2026-08-04 POST_CLOSE**：EPS $0.21 vs 共识 0.13–0.15、营收 $458.8M（+30.5% YoY）双超，AH +3.6%；📊 前瞻 beat_confirm 命中已回填 decision-log。价格确认待 8/5 官方收盘（若冲高衰竭收盘确认 → ACT-003 评估，否则持有）。
- ETN 52 周高复核（2026-08-04）— 第 2 日再创新高 444.69（盘中 451.96，+1.47%）强收盘：仍无衰竭/高位风险收盘确认 → ACT-003 不触发，持有（CORE-004）。次日续复核。
- BE 盘后律所征集（2026-08-04）— Bernstein Liebhard 等就 scandium 供应披露征集集体诉讼原告（AH −0.9%）：招揽阶段=噪声（L-005 口径），非核实公司破坏 → 持有；升级条件：法院立案 + 公司披露实质财务影响。
- 2026-08-04 settlement — **VERIFIED same night**（连续第三晚）：8/8 双源结算 0.00–0.2%（AV OHLC / stockanalysis At-close + GF-beta Closed 戳）；valuation_date → 2026-08-04；wallet 103,951.12；C1–C7 diff=0；W1 lag=0；**累计 +3.95% 连续第 2 日新高**；环境 RISK_ON→CHOPPY（VIX 16.41）。No trades。MP Q2 8/6 盘后（ACT-005 封锁）。
- BE 盘前弱势（2026-08-03 PREMARKET_RISK）— **CLEARED（误报）2026-08-03 POST_CLOSE**：官方收盘 218.32 +6.08%（双源 0.00%），盘前 −3.9% 未获收盘证实；L-005 噪声判定正确（全日盘中持续走强，尾盘 +7.15%）。
- ETN 52 周高复核（2026-08-03）— 盘中触及**新 52 周高 438.76**、收 438.23（+5.55%）强收盘：无衰竭/无高位风险收盘确认 → ACT-003 不触发，持有（CORE-004 不按涨幅止盈）。次日续复核。
- 2026-08-03 settlement — **VERIFIED same night**（连续第二晚）：8/8 双源结算 0.00%（stockanalysis At-close + Google Finance beta Closed；ABT 第二源 roic.ai Δ0.04%）；valuation_date → 2026-08-03；wallet 101,053.26；C1–C7 diff=0；W1 lag=0；**累计盈亏首次转正 +1.05%**。No trades。KTOS Q2 8/4 盘后（forecast 已登记，明晚 POST_CLOSE 回填）。

- ETN Q2 (7/31 pre-open) — **CLEARED (fundamentals + price, 2026-07-31 POST_CLOSE): thesis strengthened.** Record Q2: adj EPS $3.15 vs $3.08 cons (beat), revenue $8.53B vs $8.16B (+21% sales), organic-growth & EPS guidance RAISED, Mobility/Dana spin-off on track. Official close 415.20 +7.32% (2-source stockanalysis at-close + Google Finance, 0.00%); position flipped to profit (+3.6% vs cost 400.69). Strong close, no exhaustion → ACT-003 not triggered, held (no trim). "Hold into earnings" (L-002) positive sample #3.
- 2026-07-31 settlement — **VERIFIED same night** (first same-night VERIFIED settlement since 7/16): 8/8 closes 2-source 0.00% at T+~45min (quote pages carried settled "At close Jul 31" stamps); valuation_date advanced to 2026-07-31; wallet 98,160.72; C1–C7 diff=0; W1 lag=0. No trades.
- RMBS RED_PENDING_CLOSE (Q2 7/27) — **CLEARED 2026-07-28**: EPS beat verified, position held.
- BE Q2 (7/28 after close) — **CLEARED** (fundamentals). 7/29 price-confirmation **DONE (2026-07-30 morning backfill)**: verified close 163.75 (−1.85%, intraday 185.66→157.33) — the +12.7% AH pop fully retraced, broad PT cuts (Jefferies/BMO/Truist to Hold). Thesis intact (record quarter), no verified impairment → held (advisory); no stop triggered. Sell-the-news divergence confirmed (lessons L-011 / HYP-001).
- ABT take-profit 104.76 — **EXECUTED 2026-07-31 MORNING (止盈-减仓50%).** 7/30 official close 105.61 (2-source: stockanalysis history + Google Finance, 0.00%, OHLC-exact) fell BELOW the prior-day (7/29) low 106.97 — the pre-registered ACT-003 close-confirmed exhaustion/reversal after two closes above 104.76, ABT the lone red name on a broad risk-on day. Trade 2026-07-30-ABT-止盈减仓50-01: sold 25.29595 sh @105.61, realized **+171.51**. Remaining 25.29595 sh held (+6.86% vs cost). **SIGNAL CLEARED.**
- PWR Q2 (2026-07-30 pre-open) — **CLEARED (fundamentals), thesis strengthened.** adj EPS $4.24 vs $3.31 (big BEAT); FY26 adj EPS guide raised to $16.45-16.95 from $13.55-14.25; +17.26% to 657.98 (above cost proxy 631.02, flipped to profit +404.60). "Hold into earnings" (L-002) paid off. No exhaustion → hold, no trim. **Price VERIFIED 2026-07-31 (657.98, 2-source stockanalysis + stockscan).**
- 2026-07-30 settlement — **CLOSED → VERIFIED (2026-07-31 MORNING backfill)**: 8/8 closes settled by ≥2 independent sources; valuation_date advanced to 2026-07-30; wallet 97,127.42; C1–C6 diff=0; W1 lag=0. ABT take-profit executed (see above). Google Finance classic endpoint returned Dec stale cache for BE/RMBS (avoided; used stockscan.io instead) — logged as method lesson.
- 2026-07-29 settlement — **CLOSED → VERIFIED (2026-07-30 morning backfill)**: 8/8 closes settled; wallet names GEV 900.28 / ETN 361.88 / ABT 108.00 confirmed by 2 fresh independent sources (stockanalysis history + Google Finance) at 0.00% incl. OHLC. valuation_date advanced to 2026-07-29; wallet 99,135.95; C1–C6 diff=0; W1 lag=0.
