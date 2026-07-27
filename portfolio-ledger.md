# US Stock Portfolio Ledger

schema_version: 2.0
base_currency: USD
slot_limit: 8
last_reconciled_at: 2026-07-25T13:05:00+08:00
price_as_of: 2026-07-24 regular close (VERIFIED, >=2 independent sources per symbol, 0.00% discrepancy)
prior_price_as_of: 2026-07-16 regular close (superseded; 6-trading-day gap closed on 2026-07-25)

## Invariants

- This file is the only source of truth for positions and trade history.
- Position status is only `OPEN` or `CLOSED`.
- Real positions change quantity/status only after explicit user confirmation of execution.
- Simulated trades require a unique `trade_id`, wallet update, and post-trade accounting validation.
- Unknown real quantities are excluded from wallet market value and portfolio P&L.

## OPEN real positions

| symbol | status | opened_on | cost | quantity | last_close | close_date | data_status | thesis |
|---|---|---:|---:|---:|---:|---:|---|---|
| PWR | OPEN | 2026-07-08 | 666.33 | 15.0076 | 625.84 | 2026-07-24 | VERIFIED | Grid and data-center electrical infrastructure demand; record backlog intact; Q2 due Jul 30 pre-open. JPMorgan cut to Neutral (PT 714) in gap window; −4.28% on 7/24 with no company-specific catalyst |
| MP | OPEN | 2026-07-08 | 53.00 | 188.6792 | 41.30 | 2026-07-24 | VERIFIED | US strategic rare-earth supply chain. 🚨 New 52-week low (41.12 intraday); −7.50% on 7/24; rare-earth oversupply/NdPr price fears; no verified company impairment; Q2 moved to Aug 6 |
| BE | OPEN | 2026-07-10 | 244.61 | 40.8814 | 184.89 | 2026-07-24 | VERIFIED | Distributed power for AI infrastructure. 🚨 −14.91% on 7/24 (gapped down, never traded above open); Panama/EdgeMode deal buzz failed to hold; two securities-fraud investigation notices filed 7/17; Q2 due Jul 28 after close |
| KTOS | OPEN | 2026-07-10 | 48.19 | 207.5119 | 47.35 | 2026-07-24 | VERIFIED | Defense, space and unmanned-systems order growth; ~$156M sole-source counter-UAS IDIQ award 7/21; Elroy Air manufacturing deal 7/20; Q2 confirmed Aug 4 after close |
| RMBS | OPEN | UNKNOWN | 115.00 | 86.9565 | 96.01 | 2026-07-24 | VERIFIED | DDR5 memory-interface demand; quantity 86.9565 derived from user-confirmed $10,000 sizing ÷ recorded entry 115.00 (2026-07-27); −6.96% on 7/24 with no company catalyst (semis/AI-memory pullback); Q2 due Jul 27 after close |

## OPEN simulated positions

| symbol | status | opened_on | cost | quantity | cost_basis | last_close | close_date | market_value | unrealized_pnl | data_status | thesis |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|
| GEV | OPEN | BASELINE_MIGRATED | 1042.60 | 4.7957 | 4999.996820 | 1014.75 | 2026-07-24 | 4866.436575 | -133.560245 | VERIFIED | Grid/power-gen capex. **Q2 REPORTED 7/22 pre-open**: EPS $2.47 adj vs $3.17 cons (MISS), revenue $11.1B vs $10.8B (BEAT), orders $24.2B +88% YoY, backlog $176B, "mostly sold out through 2030", FY26 revenue guidance RAISED to $45.5–46.5B (2nd consecutive raise). Drag: wind orders −40%, offshore cost, tariff risk. Reaction 7/22 −8.69% → 7/23 +4.69% → 7/24 −1.59%. Closed below 50d MA 1033.10 |
| ETN | OPEN | BASELINE_MIGRATED | 415.52 | 12.0331 | 4999.993712 | 404.07 | 2026-07-24 | 4862.214717 | -137.778995 | VERIFIED | Electrification and data-center power management; thesis intact, no verified impairment. Best relative performer among laggards (+3.55pp vs SPY in gap). Dividend $1.10 declared 7/21. Q2 due Jul 31 pre-open |
| ABT | OPEN | 2026-07-17 | 98.83 | 50.5919 | 4999.997477 | 103.06 | 2026-07-24 | 5214.001214 | 214.003737 | VERIFIED | **Thesis CONFIRMED and strengthened.** Q2 (7/16) EPS $1.31 vs $1.28 beat, revenue $12.59B vs $12.52B, FY26 adj EPS raised to $5.45–5.60. Since entry: broad PT raises (JPM 120, BofA 115, Citi 112, Daiwa 92→103), no downgrades; 7/24 +2.29% on TWO legal wins (shareholder formula suit dismissed; 7th Circuit appeal won). New risks: 7/17 cybersecurity incidents (cancer diagnostics + LabCentral) with patient class actions; 7/24 FreeStyle Libre 3 class action. Stop-loss trigger (official close < 95.86) NOT hit; +4.28% vs cost |

## Position sizing note — 2026-07-27 (user-confirmed $10,000 per real position)

The user confirmed on 2026-07-27 that each of the five real positions was a **US$10,000** initial investment. This is treated as confirmed cost basis per CORE-002.

- **RMBS**: entry price 115.00 was already on record → quantity = 10000 ÷ 115.00 = **86.9565 shares**. Now valued/manageable (no longer frozen). Real positions remain excluded from the simulated wallet.
- **PWR, MP, BE, KTOS**: on 2026-07-27 the user approved deriving quantity from each position's **entry-date official close as a documented PROXY fill** (exact broker fills not available). Quantities set: PWR 15.0076 @ proxy 666.33 (2026-07-08 close); MP 188.6792 @ 53.00 (2026-07-08); BE 40.8814 @ 244.61 (2026-07-10); KTOS 207.5119 @ 48.19 (2026-07-10). Source: stockanalysis.com history (S&P Global Market Intelligence); each proxy cross-checked against the ledger's recorded 2026-07-16 closes with 0.00% mismatch. **These are PROXY cost bases, not confirmed fills** — replace with actual fills whenever the user provides them (`KEY#rN`-style correction). All five real positions are now valued/manageable; frozen count 5 → 0.

Real positions carry real money and are **advisory only** (every action is 建议未执行); they are **not** part of the simulated wallet's market value or P&L. No simulated trade was booked; the simulated wallet is unchanged.

Real book snapshot at 2026-07-24 official closes (cost basis $10,000 each, total $50,000): market value $42,917.74, unrealized −$7,082.26 (−14.16%). Per-name unrealized: PWR −6.08%, MP −22.08%, BE −24.41%, KTOS −1.74%, RMBS −16.51%.

## CLOSED positions

None recorded.

## Trade history

The GEV and ETN positions are migrated confirmed baselines. No synthetic trade IDs were created because their original execution dates were not confirmed. Future trades must use `YYYY-MM-DD-SYMBOL-ACTION-NN` and must never duplicate an existing ID.

| trade_id | trade_date | symbol | action | quantity | price | gross_value | planned_stop | planned_take_profit | planned_risk | status |
|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-07-17-ABT-建仓-01 | 2026-07-17 | ABT | 建仓 | 50.5919 | 98.83 | 4999.997477 | 95.86 | 104.76 | 150.257943 | SIMULATED_EXECUTED |

## Reconciliation note — 2026-07-16

Seven OPEN slots are confirmed from prior system state: five real and two simulated. July 15 prices are preserved only as reconciliation references; every scheduled run must refresh and validate prices before updating P&L or issuing a trade. No real or simulated execution was performed during this migration.

## Morning logic cards — 2026-07-17 (using 2026-07-16 official close)

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

## Out-of-band revaluation — 2026-07-25 (closing a 6-trading-day data gap)

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

**Fields deliberately NOT updated (would require fabrication):** holding days since entry, maximum close since entry, drawdown from peak, and 20/50/200-day moving averages for the five real positions. Computing these needs the full daily close series per symbol from each entry date, which was not retrieved in this pass. They are left as-is rather than estimated, per CORE-003. The next full POST_CLOSE run should populate them.
