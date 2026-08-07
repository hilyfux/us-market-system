# US Stock Portfolio Ledger

schema_version: 2.0
base_currency: USD
slot_limit: 8
last_reconciled_at: 2026-08-05T05:30:00+08:00
price_as_of: 2026-08-04 regular close (VERIFIED same-night at T+~60–75min, 3rd consecutive same-night settlement; all 8 names 2 independent settled sources — GEV/ETN via Alpha Vantage settled OHLC (quota died after 3 calls) + roic/GF-beta cross-check ≤0.2%; ABT/PWR/MP/BE/KTOS/RMBS via stockanalysis "At close: Aug 4, 2026, 4:00 PM EDT" stamps + Google Finance beta "Closed: Aug 4, 4:00 PM GMT-4" stamps at 0.00% (ABT 2nd source roic.ai Δ0.18%); GF-beta edge cache is a lottery — kept rotating ?v= params until settled stamps appeared, per 8/3 method)
prior_price_as_of: 2026-08-03 regular close (superseded)

## Invariants

- This file is the only source of truth for positions and trade history.
- Position status is only `OPEN` or `CLOSED`.
- **2026-07-30 — unified simulated (demo) book.** Per user directive, ALL positions are now part of the single simulated account; the system actively trades all of them to grow the demo P&L. The former "advisory / 建议未执行 real positions" distinction is retired (the five were migrated into the simulated book at their recorded cost basis — see migration note below). Cost-basis corrections or migrations still require explicit user confirmation (CORE-002 intent preserved).
- Simulated trades require a unique `trade_id`, wallet update, and post-trade accounting validation.
- Initial capital stays US$100,000; max 8 positions. Migrated positions were booked at cost, debiting cash accordingly, so accounting conservation (C1–C6) holds across all 8.

## OPEN positions

| symbol | status | opened_on | cost | quantity | cost_basis | last_close | close_date | market_value | unrealized_pnl | data_status | thesis |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| GEV | OPEN | BASELINE_MIGRATED | 1011.38 | 9.887457 | 10000.000000 | 1000.30 | 2026-08-06 | 9890.423237 | -109.576763 | VERIFIED | **2026-07-31 均衡加仓 @981.98 至 $10k 成本基（+5.091757 股/$5000）**. Grid/power-gen capex. **Q2 REPORTED 7/22 pre-open**: EPS $2.47 adj vs $3.17 cons (MISS), revenue $11.1B vs $10.8B (BEAT), orders $24.2B +88% YoY, backlog $176B, "mostly sold out through 2030", FY26 revenue guidance RAISED to $45.5–46.5B (2nd consecutive raise). Drag: wind orders −40%, offshore cost, tariff risk. Reaction 7/22 −8.69% → 7/23 +4.69% → 7/24 −1.59%. Closed below 50d MA 1033.10 |
| PWR | OPEN | 2026-07-08 (migrated 7-30) | 632.39 | 15.812950 | 10000.000000 | 667.84 | 2026-08-06 | 10560.520528 | 560.520528 | VERIFIED | **2026-07-31 均衡加仓 @657.98 至 $10k 成本基（+0.805350 股/$529.90）**. Grid/data-center electrical infra; record backlog. Q2 7/30 BIG BEAT (adj EPS $4.24 vs $3.31; FY26 guide raised to $16.45–16.95); 7/31 Guggenheim upgrade to Buy (PT 800), +1.43% follow-through. Migrated from advisory→sim 2026-07-30; cost = 7/16 close proxy |
| MP | OPEN | 2026-07-08 (migrated 7-30) | 44.88 | 222.828109 | 10000.000000 | 47.49 | 2026-08-06 | 10582.106896 | 582.106896 | VERIFIED | **2026-07-31 均衡加仓 @41.66 至 $10k 成本基（+34.148909 股/$1422.64）**. US rare-earth supply chain 🚨; oversupply sentiment, no verified impairment (L-005); Q2 Aug 6. Migrated 2026-07-30; cost = 7/16 close proxy |
| BE | OPEN | 2026-07-10 (migrated 7-30) | 206.79 | 48.358168 | 10000.000000 | 228.96 | 2026-08-06 | 11072.086145 | 1072.086145 | VERIFIED | **2026-07-31 均衡加仓 @207.12 至 $10k 成本基（+7.476768 股/$1548.59）**. Distributed power for AI; Q2 (7/28) record beat but price fully retraced next close (L-011); no impairment → hold. Migrated 2026-07-30; cost = 7/16 close proxy |
| KTOS | OPEN | 2026-07-10 (migrated 7-30) | 46.94 | 213.040191 | 10000.000000 | 57.41 | 2026-08-06 | 12230.637365 | 2230.637365 | VERIFIED | **2026-07-31 均衡加仓 @46.17 至 $10k 成本基（+5.528291 股/$255.24）**. Defense/unmanned order growth. **Q2 REPORTED 8/4 AH: EPS $0.21 vs cons $0.13–0.15 (BEAT), rev $458.8M vs ~$411M (+30.5% YoY, +19.1% organic), AH +3.6%** — thesis upgraded order-flow→execution; 7/29 insider-selling headline = noise pending confirmation (L-005). Migrated 2026-07-30; cost = 7/16 close proxy |
| MSFT | OPEN | 2026-08-05 | 487.46 | 20.514504 | 10000.000120 | 499.86 | 2026-08-06 | 10254.379969 | 254.379849 | VERIFIED | **确定性替换入场（2026-08-06 MORNING 执行，trade 2026-08-05-MSFT-建仓-01）**：九维 85 分 vs 最弱仓 RMBS 68 分（+17 ≥ 5 门槛）。AI 软件/云 hyperscaler：Q4 FY26（7/29 盘前）EPS $4.74 vs $4.24 BEAT、营收 $90.01B vs $87.63B BEAT，Azure 增长确认，8/3 +4.93% 收复 YTD 跌幅（26 年最强修复段），8/5 −1.09% 温和整理＝非追高入场点。3 日涨幅 +4.89% ≤8% 过涨幅门；beta 1.10 非高波动全仓 $10k；ai_software 论题敞口 10.00% ≤25%。风险：OpenAI 营收集中（FY26 AI 收入 ~70% 来自 OpenAI，8/5 披露）、Stifel 唯一 Hold PT 450。止损计划 official close < 437.00（−10.35%，风险 ≈1% NAV，收盘确认）；止盈仅按 ACT-003 收盘衰竭确认，不按涨幅。 |
| ETN | OPEN | BASELINE_MIGRATED | 400.69 | 24.956686 | 10000.000000 | 448.19 | 2026-08-06 | 11185.337098 | 1185.337098 | VERIFIED | **2026-07-31 均衡加仓 @386.89 至 $10k 成本基（+12.923586 股/$5000.01）**. Electrification and data-center power management; thesis intact, no verified impairment. Best relative performer among laggards (+3.55pp vs SPY in gap). Dividend $1.10 declared 7/21. **Q2 REPORTED 7/31 pre-open: record beat** — adj EPS $3.15 vs $3.08, rev $8.53B vs $8.16B (+21% sales), organic-growth & EPS guidance RAISED, Mobility/Dana spin-off on track; +7.32% to 415.20, position flipped to profit (+3.6%) |
| ABT | OPEN | 2026-07-17 | 103.83 | 96.311964 | 10000.000000 | 107.96 | 2026-08-06 | 10397.839633 | 397.839633 | VERIFIED | **2026-07-31 均衡加仓 @105.61 至 $10k 成本基（+71.016014 股/$7500.00，用户指令：所有标的一律 $10k，覆盖此前"保留半仓"判断）**. **Thesis CONFIRMED and strengthened.** Q2 (7/16) EPS $1.31 vs $1.28 beat, revenue $12.59B vs $12.52B, FY26 adj EPS raised to $5.45–5.60. Since entry: broad PT raises (JPM 120, BofA 115, Citi 112, Daiwa 92→103), no downgrades; 7/24 +2.29% on TWO legal wins (shareholder formula suit dismissed; 7th Circuit appeal won). New risks: 7/17 cybersecurity incidents (cancer diagnostics + LabCentral) with patient class actions; 7/24 FreeStyle Libre 3 class action. Stop-loss (official close < 95.86) NOT hit. **2026-07-30 close 105.61 fell below the prior-day (7/29) low 106.97** = close-confirmed exhaustion/reversal (ACT-003) after two closes above the 104.76 take-profit and the lone red name on a broad risk-on day → **止盈-减仓50% executed @105.61** (trade 2026-07-30-ABT-止盈减仓50-01, realized +171.51). Remaining 25.29595 sh held, +6.86% vs cost. NOW HALF POSITION. |

## Position sizing note — 2026-07-27 (user-confirmed $10,000 per real position)

The user confirmed on 2026-07-27 that each of the five real positions was a **US$10,000** initial investment. This is treated as confirmed cost basis per CORE-002.

- **RMBS**: entry price **corrected 115.00 → 114.00 per user (2026-07-30)**; per user choice the quantity is held at **86.9565 shares** (not rescaled), so cost basis = 86.9565 × 114.00 = **$9,913.04** (previously $10,000 at 115.00). Now valued/manageable (no longer frozen). Real positions remain excluded from the simulated wallet.
- **PWR, MP, BE, KTOS**: proxy cost **re-referenced to the 2026-07-16 official close per user (2026-07-30)** — for positions without a confirmed fill, the 7/16 VERIFIED close is the recorded cost price. Per user choice the **share counts are kept** (not rescaled, same convention as RMBS), so cost basis floats off the earlier $10,000 anchor. Set: PWR 15.0076 @ 631.02 → basis $9,470.10; MP 188.6792 @ 45.46 → $8,577.36; BE 40.8814 @ 206.73 → $8,451.41; KTOS 207.5119 @ 46.96 → $9,744.76. (Superseded prior entry-date proxies: PWR 666.33/7-08, MP 53.00/7-08, BE 244.61/7-10, KTOS 48.19/7-10.) 7/16 closes are VERIFIED in data/post-close.md. **Still PROXY cost bases, not confirmed fills** — replace with actual fills whenever the user provides them (`KEY#rN`-style correction). All five real positions valued/manageable; frozen count 0. Real real-book cost basis total now $46,156.66 (incl. RMBS $9,913.04).

## Migration note — 2026-07-30 (unify advisory positions into the demo book)

Per user directive, the five formerly-advisory positions (PWR, MP, BE, KTOS, RMBS) were folded into the single simulated (demo) account, which the system now actively trades. Method (best-practice, honest P&L carry-over):

- **Initial capital unchanged at $100,000** (existing hard rule preserved).
- Each migrated position is booked at its **recorded cost basis** (7/16-close proxy; RMBS at user-corrected 114.00), i.e. treated as already purchased. Total migrated cost basis = **$46,156.66**.
- **Cash debited** by that amount: 85,000.011991 − 46,156.66 → **38,843.348161**. Combined with the pre-existing three sim names, sum(cost_basis) over all 8 = $61,156.65 and cash = 100,000 − 61,156.65 (C2 holds).
- Post-migration book (7/29 closes): market value **52,746.797595**, total assets **91,590.145756**, cumulative P&L **−8,409.854244 (−8.41%)**, position ratio **57.59%**.
- The "advisory / 建议未执行 / excluded from wallet" treatment is **retired**; all 8 are now tradeable sim positions (execution in MORNING/POST_CLOSE, exits close-confirmed per ACT-002/003).
- Note: 57.59% invested is above the DEFENSIVE 50% ceiling — a consequence of migration, not a new trade; ACT-004 blocks new builds until exposure falls or regime lifts. Costs remain PROXY until real fills are provided (`KEY#rN` correction).

[HISTORICAL snapshot 2026-07-24 — superseded] Advisory book at 7/24: mv $42,917.74 (−14.16%).

## CLOSED positions

| symbol | status | opened_on | closed_on | cost | quantity | cost_basis | exit_price | gross_proceeds | realized_pnl | note |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| RMBS | CLOSED | 2026-07 (migrated 7-30) | 2026-08-05 | 113.73 | 87.926808 | 10000.000000 | 97.30 | 8555.278418 | -1444.721582 | **确定性替换退出（trade 2026-08-05-RMBS-平仓-01，2026-08-06 MORNING 执行 @8/5 官方收盘 97.30 VERIFIED）**：连续两日九维最弱仓（68 分），候选 MSFT 85 分 +17 ≥ 5 分门槛 → 卖最弱、买候选（用户 2026-08-04 裁定的替换方法论，不要求公司破坏）。业务论点（DDR5/AI-memory）未破——退出理由是相对确定性排序，非止损；8/5 −3.23% 随半导体回调、$100M ASR 为正向 IR。持仓期教训：入场时机在财报前高位（L-010 反例），成本 113.73 vs 区间低 82.81，最大浮亏 −27.4%，最终 −14.45% 离场。 |

## Trade history

The GEV and ETN positions are migrated confirmed baselines. No synthetic trade IDs were created because their original execution dates were not confirmed. Future trades must use `YYYY-MM-DD-SYMBOL-ACTION-NN` and must never duplicate an existing ID.

| trade_id | trade_date | symbol | action | quantity | price | gross_value | planned_stop | planned_take_profit | planned_risk | status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-07-17-ABT-建仓-01 | 2026-07-17 | ABT | 建仓 | 50.5919 | 98.83 | 4999.997477 | 95.86 | 104.76 | 150.257943 | SIMULATED_EXECUTED |
| 2026-07-30-ABT-止盈减仓50-01 | 2026-07-30 | ABT | 止盈-减仓50% | 25.29595 | 105.61 | 2671.505280 | — | — | — | SIMULATED_EXECUTED |
| 2026-08-05-RMBS-平仓-01 | 2026-08-05 | RMBS | 平仓 | 87.926808 | 97.30 | 8555.278418 | — | — | — | SIMULATED_EXECUTED |
| 2026-08-05-MSFT-建仓-01 | 2026-08-05 | MSFT | 建仓 | 20.514504 | 487.46 | 10000.000120 | 437.00 | — | 1035.161870 | SIMULATED_EXECUTED |

**Trade note — 2026-08-05 replacement pair (2nd/3rd realized-book trades).** executed_at 2026-08-06T08:31+08:00 (MORNING run); market_session_date 2026-08-05; valuation_source_date 2026-08-05. RMBS exit @97.30 (settlement-VERIFIED 2-source close), realized **−1,444.721582**; MSFT entry @487.46 (2-source verified: stockanalysis At-close + Google Finance beta Closed-stamp, 0.00%, OHLC-exact 496.36/498.24/485.68/487.46). Trigger = ACT-004 deterministic replacement (user ruling 2026-08-04): candidate MSFT nine-dim 85 vs weakest RMBS 68, diff +17 ≥ 5 (`replacement_gate` PASS); `screen_new_position` all gates PASS (ACT-005 last report 7/29, next >5 sessions; ACT-006 ai_software 10.00% ≤ 25%; ACT-007 beta 1.10 → full $10k). 3-day surge check +4.89% ≤ 8% (closes 464.72→487.65→492.81→487.46, primary stockanalysis history; 8/5 & 8/4 cross-confirmed by Google Finance, 8/3 +5% corroborated by GeekWire report). Yesterday's three blockers all cleared: regime RISK_ON (VIX 15.81 2-source), ratio 82.12% < 90% ceiling, closes 2-source. Cash 20,171.506542 → 18,726.784840; realized cum +171.506542 → **−1,273.215040**; total assets unchanged 104,732.780017 (trade at market). C1–C7 re-validated post-write.

**Trade note — 2026-07-30-ABT-止盈减仓50-01 (first realized trade).** executed_at 2026-07-31T08:40+08:00; market_session_date 2026-07-30; valuation_source_date 2026-07-30 (2-source verified, stockanalysis history + Google Finance, 0.00%, OHLC-exact). Sold 25.29595 sh (half of 50.5919) @ 105.61 official close. Cost basis of sold half 2499.998738; proceeds 2671.505280; **realized P&L +171.506542**. Trigger = ACT-003 close-confirmed exhaustion/reversal: 7/30 close 105.61 < prior-day (7/29) low 106.97, third close in the 104.76+ zone turning down, ABT the lone red name on a broad risk-on day (distribution). Remaining ABT 25.29595 sh @ 98.83 (cost basis 2499.998739) held. Wallet realized_pnl 0 → 171.506542; C1–C6 re-validated diff=0 (C2 extended to realized-aware form, backward-compatible, selftest 147→150 green).

## Reconciliation note — 2026-07-16

Seven OPEN slots are confirmed from prior system state: five real and two simulated. July 15 prices are preserved only as reconciliation references; every scheduled run must refresh and validate prices before updating P&L or issuing a trade. No real or simulated execution was performed during this migration.

## [HISTORICAL] Morning logic cards — 2026-07-17（已被 knowledge/tickers/*.md 逻辑卡取代；仅存档）

| symbol | action | close trend / relative strength | verified catalyst and thesis | explicit take-profit condition | explicit stop-loss condition |
|---|---|---|---|---|---|
| PWR | 持有 | 631.02; short-term decline and weaker than SPY | Record backlog and raised outlook intact; Q2 due Jul 30 | 止盈-减仓25% only if catalyst realization or exhaustion is confirmed at an official close | 止损-减仓25% only if backlog/guidance materially deteriorates and an official close confirms trend failure |
| MP | 持有 | 45.46; sharp decline, very weak relative strength | Strategic US rare-earth thesis remains; no verified new impairment | 止盈-减仓25% after a verified catalyst is realized and the official close shows exhaustion | 止损-减仓25% only if government/financing support materially weakens and an official close confirms breakdown |
| BE | 持有 | 206.73; extreme short-term weakness | Raised guidance, Brookfield framework and Oracle agreement remain; Q2 due Jul 28 | 止盈-减仓25% if contract catalyst is realized and official-close price/volume shows exhaustion | 止损-减仓25% only if guidance/contracts materially reverse and an official close confirms breakdown |
| KTOS | 持有 | 46.96; short-term and relative weakness | Recent program funding, space award and capacity expansion support thesis | 止盈-减仓25% after award realization plus official-close exhaustion | 止损-减仓25% only if awards/funding materially deteriorate and an official close confirms failure |
| RMBS | 持有 | 101.42; below recorded cost and weaker than SPY | DDR5-9600 product thesis intact; Q2 due Jul 27 | 止盈-减仓25% only after recovery into profit plus catalyst realization and official-close exhaustion | 止损-减仓25% only if DDR5 demand/guidance deteriorates and an official close confirms breakdown |
| GEV | 持有 | 1036.22; below cost, short-term relative weakness | Grid contracts and research expansion intact; Q2 due Jul 22 | 止盈-减仓25% only after return to profit plus catalyst realization and official-close exhaustion | 止损-减仓25% only if orders/guidance deteriorate and an official close confirms trend failure |
| ETN | 持有 | 396.27; below cost, very weak relative strength | Electrification thesis intact; no verified fundamental impairment | 止盈-减仓25% only after return to profit plus catalyst realization and official-close exhaustion | 止损-减仓25% only if data-center/electrification outlook deteriorates and an official close confirms breakdown |
| ABT | 建仓 | 98.83; qualified positive 3-day trend, +7.30% and within 8% gate | Earnings beat and raised 2026 forecast; score 87 | 止盈-减仓50% at/above 104.76 only with catalyst realization or official-close exhaustion confirmation | 止损-平仓 only if forecast/earnings thesis materially reverses and official close is below 95.86 |

ACTIVE rules: ACT-001 passed for verified closes; ACT-002 blocked exits because no position had both verified fundamental impairment and close confirmation; ACT-003 blocked profit exits because no qualifying catalyst realization/exhaustion was confirmed; ACT-004 authorized the ABT simulated entry. Market regime was classified as defensive, so the 50% position ceiling applies.

## [HISTORICAL] Out-of-band revaluation — 2026-07-25（结算历史现由 data/post-close.md 登记；仅存档）

**Type: REVALUATION ONLY — no trades executed, no trade_id created, no quantity changed.** This was not a scheduled stage run; it is a reconciliation authorized by the user to repair state that had been stale since the 2026-07-16 close. Per CORE-002 no real position changed, and per the intraday/out-of-band rule no simulated trade was booked.

Prices used: 2026-07-24 official regular-session closes, each confirmed by >=2 independent server-rendered sources with 0.00% cross-source discrepancy (details and URLs recorded in system-state.md).

| symbol | 7/16 close | 7/24 close | change | vs SPY (pp) | action taken |
|---|---:|---:|---:|---:|---|
| PWR | 631.02 | 625.84 | −0.82% | +0.76 | 持有（建议未执行；真实持仓） |
| MP | 41.30 ← 45.46 | 41.30 | −9.15% | −7.57 | 持有 + 🚨 观察（新 52 周低） |
| BE | 206.73 | 184.89 | −10.56% | −8.98 | 持有 + 🚨 观察（财报 7/28） |
| KTOS | 46.96 | 47.35 | +0.83% | +2.41 | 持有 |
| RMBS | 101.42 | 96.01 | −5.33% | −3.75 | 持有（财报 7/27） |
| GEV | 1036.22 | 1014.75 | −2.07% | −0.49 | 持有（财报已出，指引上调） |
| ETN | 396.27 | 404.07 | +1.97% | +3.55 | 持有 |
| ABT | 98.83 | 103.06 | +4.28% | +5.86 | 持有（论点强化，未触发 95.86 止损） |

Benchmarks 7/16 → 7/24: SPY 750.83 → 738.93 (−1.58%); QQQ 705.89 → 684.23 (−3.07%); IWM 295.59 → 291.17 (−1.50%); VIX 16.73 → 18.58 (+1.85); US10Y 4.57% → 4.68% (+11bp). NYSE breadth 7/24: 1,652 advancers vs 1,073 decliners (1.54:1 positive) while Nasdaq was 1.30:1 negative — a narrow AI/semiconductor de-rating, not broad risk-off. The genuine risk-off session was 7/23 (NYSE −2.99:1, VIX +12.4%).

**Exit-rule review (all 8 positions): no exit authorized.** ACT-002: no position combined verified fundamental impairment with official-close technical confirmation. ACT-003: no profit exit qualified — ABT is the only position in profit and neither catalyst-exhaustion nor its 104.76 take-profit level was confirmed at an official close (7/24 close 103.06). MP and BE are the two positions whose relative weakness is severe enough to warrant 🚨, but both lack verified company-level impairment: MP's decline is sector oversupply sentiment, and BE's is a failed deal rumour plus plaintiff-firm solicitations, neither of which is a verified fundamental break. Both are carried as 持有 with mandatory re-examination at the next official close, and BE's Q2 print on 7/28 is the decision point.

**[RESOLVED 2026-07-28]** 持有天数/入场后最高收盘/回撤/MA20/MA50 已由 Alpha Vantage 日线序列计算（锚点全对），见 `data/analytics.md`；MA200 因免费层限制暂缺（显式标注）。
