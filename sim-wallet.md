# Simulated Wallet

schema_version: 2.0
base_currency: USD
initial_capital: 100000.000000
last_reconciled_at: 2026-08-05T05:30:00+08:00
valuation_date: 2026-08-04
valuation_status: VERIFIED
valuation_source: 2026-08-04 official regular-session closes, settled SAME NIGHT at T+~60–75min (3rd consecutive). All 8 names verified by 2 independent settled sources: GEV/ETN Alpha Vantage settled OHLC (+ roic/GF-beta ≤0.2%); ABT/PWR/MP/BE/KTOS/RMBS stockanalysis At-close stamps + Google Finance beta Closed-stamps 0.00% (ABT 2nd source roic.ai Δ0.18%). Prev-close cross-check vs verified 8/3 closes 0.00% on 8/8. AV free quota exhausted after 3 calls (25/day), web sources for the rest. No trades this session.
prior_valuation_date: 2026-08-03 (superseded)

## Balances

| item | USD |
|---|---:|
| cash | 20171.506542 |
| GEV market value | 10066.123348 |
| ETN market value | 11097.988697 |
| ABT market value | 10157.059723 |
| PWR market value | 10958.374350 |
| MP market value | 10577.650334 |
| BE market value | 11030.981702 |
| KTOS market value | 11050.394707 |
| RMBS market value | 8841.040544 |
| total market value | 83779.613405 |
| total assets | 103951.119947 |
| cumulative P&L | 3951.119947 |
| realized P&L | 171.506542 |
| unrealized P&L | 3779.613405 |
| position ratio | 80.595200% |

## Position accounting

| symbol | quantity | cost | cost basis | reference close | market value | unrealized P&L |
|---|---:|---:|---:|---:|---:|---:|
| GEV | 9.887457 | 1011.38 | 10000.000000 | 1018.07 | 10066.123348 | 66.123348 |
| ETN | 24.956686 | 400.69 | 10000.000000 | 444.69 | 11097.988697 | 1097.988697 |
| ABT | 96.311964 | 103.83 | 10000.000000 | 105.46 | 10157.059723 | 157.059723 |
| PWR | 15.812950 | 632.39 | 10000.000000 | 693.00 | 10958.374350 | 958.374350 |
| MP | 222.828109 | 44.88 | 10000.000000 | 47.47 | 10577.650334 | 577.650334 |
| BE | 48.358168 | 206.79 | 10000.000000 | 228.11 | 11030.981702 | 1030.981702 |
| KTOS | 213.040191 | 46.94 | 10000.000000 | 51.87 | 11050.394707 | 1050.394707 |
| RMBS | 87.926808 | 113.73 | 10000.000000 | 100.55 | 8841.040544 | -1158.959456 |

## Validation

`cash + market_value = 20171.506542 + 83779.613405 = 103951.119947`

`total_assets - initial_capital = 3951.119947`

Accounting difference: `0.000000`, within the required USD 0.05 tolerance. C1–C7 revalidated after the 2026-08-04 POST_CLOSE settlement.

**POST_CLOSE 2026-08-04 — settlement (no trades).** Second consecutive broad risk-on day (SPY +1.79% to 771.24; QQQ +3.40%; IWM +1.85%; VIX 16.41 — back above 16 → regime RISK_ON→**CHOPPY**, ceiling 90%→75%; US10Y 4.63% −5bp): total assets **101,053.26 → 103,951.12 (+2,897.86, +2.87%)**, beating SPY by +1.08pp; cumulative P&L **+1.05% → +3.95%**, second consecutive all-time high. 7/8 green — drivers (mv Δ): MP +808.87 (+8.28%, rare-earth policy narrative + pre-earnings squeeze), RMBS +733.31 (+9.04%, 4th recovery day, reclaimed 100), KTOS +566.69 (+5.41%, eve-of-print bid), BE +473.43 (+4.48%), PWR +202.41 (+1.88%), ETN +161.22 (+1.47%, new 52-wk high 444.69), GEV +111.83; ABT −159.88 (−1.55%, lone red, defensives out of rotation). Actions: all 8 持有 — **KTOS Q2 reported AH: EPS $0.21 vs cons 0.13–0.15 BEAT, rev $458.8M (+30.5% YoY) BEAT, AH +3.6%** (L-002 hold-into-earnings positive sample #4; manage after tomorrow's confirming close); ETN 2nd straight new high, no exhaustion → ACT-003 unmet (CORE-004); BE AH law-firm class-action solicitations = noise pending verification (L-005); MP Q2 8/6 (ACT-005 blockade). Regime **CHOPPY** (VIX 16.41 ≥ 16; SPY >> MA50 745.89 actual / MA200 ~700 ref) → 75% ceiling; position ratio 80.60% **above ceiling** (legacy user-authorized balanced plan) → no forced sell, new builds blocked; slots 8/8.

**POST_CLOSE 2026-08-03 — settlement (no trades).** Broad risk-on rally (SPY +1.42% to 757.67; QQQ +1.76%; IWM +1.72%; VIX 15.86; US10Y 4.69% −5bp; strong ISM-manufacturing / industrial tape): total assets **98,160.72 → 101,053.26 (+2,892.53, +2.95%)**, beating SPY by +1.52pp; cumulative P&L **flips positive for the first time**: −1.84% → **+1.05%**. All 8 names green — drivers (mv Δ): BE +604.96 (+6.08%, premarket weakness falsified at close), ETN +574.75 (+5.55%, touched new 52-wk high 438.76 intraday), KTOS +556.03 (+5.60%, eve of Q2), MP +550.39 (+5.97%), PWR +203.04 (TD Cowen/Mizuho PT raises), GEV +162.85, ABT +136.76, RMBS +103.75. Actions: all 8 持有 — ETN strong close, no exhaustion → ACT-003 twin conditions unmet, no profit-taking on price alone (CORE-004); BE PREMARKET_RISK verdict = false alarm (L-005 noise call correct); KTOS Q2 tomorrow 8/4 AH (L-002 hold-into-earnings), MP Q2 8/6 (ACT-005 event blockade). Regime **RISK_ON** (VIX 15.86 < 16, SPY 757.67 > MA50 ~745, breadth broad: IWM +1.72%) → 90% ceiling; position ratio 80.04% within ceiling; slots 8/8.

**POST_CLOSE 2026-07-31 — settlement (no trades).** Risk-on big-tech day (SPY +0.72% to 747.03; QQQ +0.65%; IWM −0.48%; VIX −6.44% to 15.99): total assets **97,127.42 → 98,160.72 (+1,033.30, +1.06%)**, beating SPY by +0.34pp; cumulative P&L improved −2.87% → **−1.84%**. Driver: ETN Q2 record beat (+7.32%, mv +706.52, flipped to profit +362.02); PWR +148.33 (Guggenheim upgrade), RMBS +123.98, KTOS +91.61, GEV +82.16, ABT +8.67; MP −64.62, BE −63.35. All 8 actions = 持有 (ETN catalyst realized but close strong, no exhaustion → ACT-003 not triggered). Regime RISK_ON (boundary: VIX 15.99, SPY back above 50d ref 744.72) → 90% ceiling; position ratio 79.45% now within ceiling; slots 8/8, no new builds possible.

**Correction 2026-07-31 (user override): ABT topped up to the uniform $10,000.** The earlier decision to keep ABT at its trimmed $2,500 was my own judgment and contradicted the explicit "every target = $10,000" directive — corrected: bought 71.016014 sh @ 105.61 ($7,500.00, trade 2026-07-31-ABT-均衡加仓-01). All 8 positions now carry exactly $10,000 cost basis (Σ = $80,000); cash 27,671.51 → 20,171.51; position ratio **79.23%** (user-authorized override of the DEFENSIVE ceiling for the balanced plan). A new preflight check (C7 sizing uniformity) now fails loudly if any OPEN position's cost basis deviates from the $10k standard without an explicit SIZE_EXCEPTION tag.

**Balance rebalance 2026-07-31 (user-directed; 7 add trades booked).** Per user instruction to restore the balanced $10,000-per-position plan, 7 positions were topped up to **$10,000 cost basis** each by buying at 7/30 official closes (GEV/ETN/PWR/MP/BE/KTOS/RMBS). ABT kept at its trimmed $2,500 (re-adding would merely reverse the 7/30 take-profit at the same price — pointless churn). Buys total **$13,843.35**; cash 41,514.85 → 27,671.51; Σ(cost_basis) 58,656.65 → 72,500.00. **Rebalancing at market does not change total assets (97,127.42), unrealized (−3,044.08) or cumulative P&L (−2,872.58)** — it only redeploys cash to equalize sizes. Position ratio **57.26% → 71.51%** — an **explicit, user-authorized override** of the DEFENSIVE 50% ceiling and of the "don't add to losers" discipline (ACT-002/L-005), accepted to build balanced per-name trade data for strategy optimization. New builds remain blocked (over cap). This is out-of-band (not a MORNING/POST_CLOSE run); each add carries a trade_id.

**Realized-P&L accounting (first realized trade — C2 extended 2026-07-31):** with a non-zero realized P&L, cash is sourced as `initial − Σ(cost_basis) + realized`. C2 was extended to this identity (backward-compatible: identical to the old form while realized = 0; all 150 selftests green). Here `100000 − 58656.653101 + 171.506542 = 41514.853441 = cash` ✓; C6 `realized 171.506542 + unrealized −3044.082635 = −2872.576093 = cumulative` ✓.

**MORNING 2026-07-30 — settlement + take-profit (trade booked).** 7/29 → 7/30 broad risk-on rally (SPY +1.68% to 741.69; VIX −17.3% to 17.09; Nasdaq +2.78%, SOX +8.2%; PCE inflation cooled). Total assets **91,590.15 → 97,127.42 (+5,537.28, +6.05%)**; cumulative P&L improved −8.41% → **−2.87%**. Drivers (mv Δ): PWR +1,453 (Q2 big beat, +17.26%), BE +1,773 (+26.49%, Mizuho upgrade), MP +672, RMBS +592, KTOS +475, GEV +392, ETN +301; ABT position −22 after trim (stock −2.21%).
**ABT 止盈-减仓50% executed** (trade 2026-07-30-ABT-止盈减仓50-01): sold 25.29595 sh @ 105.61, proceeds 2,671.51, realized **+171.51**. Trigger: 7/30 official close 105.61 fell below the prior-day (7/29) low 106.97 — the pre-registered ACT-003 close-confirmed exhaustion/reversal after two closes above the 104.76 take-profit level, and ABT was the lone red name on a broad risk-on day (distribution). Remaining 25.29595 sh held (+6.86% vs cost). Position ratio 57.26% still above the DEFENSIVE 50% ceiling → ACT-004 keeps new builds blocked; satchel 8/8.

**[HISTORICAL] Settlement 2026-07-28 → 2026-07-29 (backfilled 2026-07-30, no trades):** total assets 99599.08 → 99135.95 (−463.13); ABT the only green name (108.00). GAP closed.
