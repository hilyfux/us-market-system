# US Stock Portfolio Ledger

schema_version: 2.0
base_currency: USD
slot_limit: 8
last_reconciled_at: 2026-07-25T13:05:00+08:00
price_as_of: 2026-07-29 regular close (VERIFIED; wallet names GEV/ETN/ABT 2 independent fresh sources — stockanalysis history + Google Finance — 0.00%; backfilled 2026-07-30 morning via history-page method after AV daily quota exhausted; roic/stocktitan/stockscan still lagged 7/28 at run time)
prior_price_as_of: 2026-07-28 regular close (superseded)

## Invariants

- This file is the only source of truth for positions and trade history.
- Position status is only `OPEN` or `CLOSED`.
- **2026-07-30 — unified simulated (demo) book.** Per user directive, ALL positions are now part of the single simulated account; the system actively trades all of them to grow the demo P&L. The former "advisory / 建议未执行 real positions" distinction is retired (the five were migrated into the simulated book at their recorded cost basis — see migration note below). Cost-basis corrections or migrations still require explicit user confirmation (CORE-002 intent preserved).
- Simulated trades require a unique `trade_id`, wallet update, and post-trade accounting validation.
- Initial capital stays US$100,000; max 8 positions. Migrated positions were booked at cost, debiting cash accordingly, so accounting conservation (C1–C6) holds across all 8.

## OPEN real positions

_None. All formerly-advisory real positions were migrated into the simulated book on 2026-07-30 (see migration note below and the simulated table)._

## OPEN simulated positions

| symbol | status | opened_on | cost | quantity | cost_basis | last_close | close_date | market_value | unrealized_pnl | data_status | thesis |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| GEV | OPEN | BASELINE_MIGRATED | 1042.60 | 4.7957 | 4999.996820 | 900.28 | 2026-07-29 | 4317.472796 | -682.524024 | VERIFIED | Grid/power-gen capex. **Q2 REPORTED 7/22 pre-open**: EPS $2.47 adj vs $3.17 cons (MISS), revenue $11.1B vs $10.8B (BEAT), orders $24.2B +88% YoY, backlog $176B, "mostly sold out through 2030", FY26 revenue guidance RAISED to $45.5–46.5B (2nd consecutive raise). Drag: wind orders −40%, offshore cost, tariff risk. Reaction 7/22 −8.69% → 7/23 +4.69% → 7/24 −1.59%. Closed below 50d MA 1033.10 |
| PWR | OPEN | 2026-07-08 (migrated 7-30) | 631.02 | 15.0076 | 9470.095752 | 561.14 | 2026-07-29 | 8421.364664 | -1048.731088 | VERIFIED | Grid/data-center electrical infra; record backlog. Q2 2026-07-30 pre-open — hold into earnings (L-002). Migrated from advisory→sim 2026-07-30; cost = 7/16 close proxy |
| MP | OPEN | 2026-07-08 (migrated 7-30) | 45.46 | 188.6792 | 8577.356432 | 38.10 | 2026-07-29 | 7188.677520 | -1388.678912 | VERIFIED | US rare-earth supply chain 🚨; oversupply sentiment, no verified impairment (L-005); Q2 Aug 6. Migrated 2026-07-30; cost = 7/16 close proxy |
| BE | OPEN | 2026-07-10 (migrated 7-30) | 206.73 | 40.8814 | 8451.411822 | 163.75 | 2026-07-29 | 6694.329250 | -1757.082572 | VERIFIED | Distributed power for AI; Q2 (7/28) record beat but price fully retraced next close (L-011); no impairment → hold. Migrated 2026-07-30; cost = 7/16 close proxy |
| KTOS | OPEN | 2026-07-10 (migrated 7-30) | 46.96 | 207.5119 | 9744.758824 | 43.88 | 2026-07-29 | 9105.622172 | -639.136652 | VERIFIED | Defense/unmanned order growth; Q2 Aug 4; 7/29 insider-selling headline = noise pending confirmation (L-005). Migrated 2026-07-30; cost = 7/16 close proxy |
| RMBS | OPEN | 2026-07 (migrated 7-30) | 114.00 | 86.9565 | 9913.041000 | 82.81 | 2026-07-29 | 7200.867765 | -2712.173235 | VERIFIED | DDR5/AI-memory; Q2 (7/27) beat, Q3 guide soft; no company catalyst → hold. Migrated 2026-07-30; cost = user-corrected 114.00 |
| ETN | OPEN | BASELINE_MIGRATED | 415.52 | 12.0331 | 4999.993712 | 361.88 | 2026-07-29 | 4354.538228 | -645.455484 | VERIFIED | Electrification and data-center power management; thesis intact, no verified impairment. Best relative performer among laggards (+3.55pp vs SPY in gap). Dividend $1.10 declared 7/21. Q2 due Jul 31 pre-open |
| ABT | OPEN | 2026-07-17 | 98.83 | 50.5919 | 4999.997477 | 108.00 | 2026-07-29 | 5463.925200 | 463.927723 | VERIFIED | **Thesis CONFIRMED and strengthened.** Q2 (7/16) EPS $1.31 vs $1.28 beat, revenue $12.59B vs $12.52B, FY26 adj EPS raised to $5.45–5.60. Since entry: broad PT raises (JPM 120, BofA 115, Citi 112, Daiwa 92→103), no downgrades; 7/24 +2.29% on TWO legal wins (shareholder formula suit dismissed; 7th Circuit appeal won). New risks: 7/17 cybersecurity incidents (cancer diagnostics + LabCentral) with patient class actions; 7/24 FreeStyle Libre 3 class action. Stop-loss (official close < 95.86) NOT hit. 2026-07-29 close 108.00 = 2nd consecutive close above 104.76 take-profit, but a fresh high on strength (only green name on a broad risk-off day) — not exhaustion → held full, no trim (ACT-003/L-003); +9.28% vs cost |

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

None recorded.

## Trade history

The GEV and ETN positions are migrated confirmed baselines. No synthetic trade IDs were created because their original execution dates were not confirmed. Future trades must use `YYYY-MM-DD-SYMBOL-ACTION-NN` and must never duplicate an existing ID.

| trade_id | trade_date | symbol | action | quantity | price | gross_value | planned_stop | planned_take_profit | planned_risk | status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-07-17-ABT-建仓-01 | 2026-07-17 | ABT | 建仓 | 50.5919 | 98.83 | 4999.997477 | 95.86 | 104.76 | 150.257943 | SIMULATED_EXECUTED |

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
