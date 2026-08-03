# Simulated Wallet

schema_version: 2.0
base_currency: USD
initial_capital: 100000.000000
last_reconciled_at: 2026-08-04T05:05:00+08:00
valuation_date: 2026-08-03
valuation_status: VERIFIED
valuation_source: 2026-08-03 official regular-session closes, settled SAME NIGHT at T+~60min. All 8 names verified by 2 independent settled sources: stockanalysis quote pages ("At close: Aug 3, 2026, 4:00 PM EDT" stamp on every page) + Google Finance beta "Closed: Aug 3, 4:00 PM GMT-4" stamps, 0.00% on 7 names; ABT second source roic.ai 107.16 (Δ0.04%). Prev-close cross-check vs verified 7/31 closes 0.00% on 8/8. AV free quota exhausted all ET-day (25 req/day), web sources only. No trades this session.
prior_valuation_date: 2026-07-31 (superseded)

## Balances

| item | USD |
|---|---:|
| cash | 20171.506542 |
| GEV market value | 9954.296209 |
| ETN market value | 10936.768506 |
| ABT market value | 10316.937584 |
| PWR market value | 10755.968590 |
| MP market value | 9768.784299 |
| BE market value | 10557.555238 |
| KTOS market value | 10483.707799 |
| RMBS market value | 8107.730966 |
| total market value | 80881.749190 |
| total assets | 101053.255732 |
| cumulative P&L | 1053.255732 |
| realized P&L | 171.506542 |
| unrealized P&L | 881.749190 |
| position ratio | 80.038737% |

## Position accounting

| symbol | quantity | cost | cost basis | reference close | market value | unrealized P&L |
|---|---:|---:|---:|---:|---:|---:|
| GEV | 9.887457 | 1011.38 | 10000.000000 | 1006.76 | 9954.296209 | -45.703791 |
| ETN | 24.956686 | 400.69 | 10000.000000 | 438.23 | 10936.768506 | 936.768506 |
| ABT | 96.311964 | 103.83 | 10000.000000 | 107.12 | 10316.937584 | 316.937584 |
| PWR | 15.812950 | 632.39 | 10000.000000 | 680.20 | 10755.968590 | 755.968590 |
| MP | 222.828109 | 44.88 | 10000.000000 | 43.84 | 9768.784299 | -231.215701 |
| BE | 48.358168 | 206.79 | 10000.000000 | 218.32 | 10557.555238 | 557.555238 |
| KTOS | 213.040191 | 46.94 | 10000.000000 | 49.21 | 10483.707799 | 483.707799 |
| RMBS | 87.926808 | 113.73 | 10000.000000 | 92.21 | 8107.730966 | -1892.269034 |

## Validation

`cash + market_value = 20171.506542 + 80881.749190 = 101053.255732`

`total_assets - initial_capital = 1053.255732`

Accounting difference: `0.000000`, within the required USD 0.05 tolerance. C1–C7 revalidated after the 2026-08-03 POST_CLOSE settlement.

**POST_CLOSE 2026-08-03 — settlement (no trades).** Broad risk-on rally (SPY +1.42% to 757.67; QQQ +1.76%; IWM +1.72%; VIX 15.86; US10Y 4.69% −5bp; strong ISM-manufacturing / industrial tape): total assets **98,160.72 → 101,053.26 (+2,892.53, +2.95%)**, beating SPY by +1.52pp; cumulative P&L **flips positive for the first time**: −1.84% → **+1.05%**. All 8 names green — drivers (mv Δ): BE +604.96 (+6.08%, premarket weakness falsified at close), ETN +574.75 (+5.55%, touched new 52-wk high 438.76 intraday), KTOS +556.03 (+5.60%, eve of Q2), MP +550.39 (+5.97%), PWR +203.04 (TD Cowen/Mizuho PT raises), GEV +162.85, ABT +136.76, RMBS +103.75. Actions: all 8 持有 — ETN strong close, no exhaustion → ACT-003 twin conditions unmet, no profit-taking on price alone (CORE-004); BE PREMARKET_RISK verdict = false alarm (L-005 noise call correct); KTOS Q2 tomorrow 8/4 AH (L-002 hold-into-earnings), MP Q2 8/6 (ACT-005 event blockade). Regime **RISK_ON** (VIX 15.86 < 16, SPY 757.67 > MA50 ~745, breadth broad: IWM +1.72%) → 90% ceiling; position ratio 80.04% within ceiling; slots 8/8.

**POST_CLOSE 2026-07-31 — settlement (no trades).** Risk-on big-tech day (SPY +0.72% to 747.03; QQQ +0.65%; IWM −0.48%; VIX −6.44% to 15.99): total assets **97,127.42 → 98,160.72 (+1,033.30, +1.06%)**, beating SPY by +0.34pp; cumulative P&L improved −2.87% → **−1.84%**. Driver: ETN Q2 record beat (+7.32%, mv +706.52, flipped to profit +362.02); PWR +148.33 (Guggenheim upgrade), RMBS +123.98, KTOS +91.61, GEV +82.16, ABT +8.67; MP −64.62, BE −63.35. All 8 actions = 持有 (ETN catalyst realized but close strong, no exhaustion → ACT-003 not triggered). Regime RISK_ON (boundary: VIX 15.99, SPY back above 50d ref 744.72) → 90% ceiling; position ratio 79.45% now within ceiling; slots 8/8, no new builds possible.

**Correction 2026-07-31 (user override): ABT topped up to the uniform $10,000.** The earlier decision to keep ABT at its trimmed $2,500 was my own judgment and contradicted the explicit "every target = $10,000" directive — corrected: bought 71.016014 sh @ 105.61 ($7,500.00, trade 2026-07-31-ABT-均衡加仓-01). All 8 positions now carry exactly $10,000 cost basis (Σ = $80,000); cash 27,671.51 → 20,171.51; position ratio **79.23%** (user-authorized override of the DEFENSIVE ceiling for the balanced plan). A new preflight check (C7 sizing uniformity) now fails loudly if any OPEN position's cost basis deviates from the $10k standard without an explicit SIZE_EXCEPTION tag.

**Balance rebalance 2026-07-31 (user-directed; 7 add trades booked).** Per user instruction to restore the balanced $10,000-per-position plan, 7 positions were topped up to **$10,000 cost basis** each by buying at 7/30 official closes (GEV/ETN/PWR/MP/BE/KTOS/RMBS). ABT kept at its trimmed $2,500 (re-adding would merely reverse the 7/30 take-profit at the same price — pointless churn). Buys total **$13,843.35**; cash 41,514.85 → 27,671.51; Σ(cost_basis) 58,656.65 → 72,500.00. **Rebalancing at market does not change total assets (97,127.42), unrealized (−3,044.08) or cumulative P&L (−2,872.58)** — it only redeploys cash to equalize sizes. Position ratio **57.26% → 71.51%** — an **explicit, user-authorized override** of the DEFENSIVE 50% ceiling and of the "don't add to losers" discipline (ACT-002/L-005), accepted to build balanced per-name trade data for strategy optimization. New builds remain blocked (over cap). This is out-of-band (not a MORNING/POST_CLOSE run); each add carries a trade_id.

**Realized-P&L accounting (first realized trade — C2 extended 2026-07-31):** with a non-zero realized P&L, cash is sourced as `initial − Σ(cost_basis) + realized`. C2 was extended to this identity (backward-compatible: identical to the old form while realized = 0; all 150 selftests green). Here `100000 − 58656.653101 + 171.506542 = 41514.853441 = cash` ✓; C6 `realized 171.506542 + unrealized −3044.082635 = −2872.576093 = cumulative` ✓.

**MORNING 2026-07-30 — settlement + take-profit (trade booked).** 7/29 → 7/30 broad risk-on rally (SPY +1.68% to 741.69; VIX −17.3% to 17.09; Nasdaq +2.78%, SOX +8.2%; PCE inflation cooled). Total assets **91,590.15 → 97,127.42 (+5,537.28, +6.05%)**; cumulative P&L improved −8.41% → **−2.87%**. Drivers (mv Δ): PWR +1,453 (Q2 big beat, +17.26%), BE +1,773 (+26.49%, Mizuho upgrade), MP +672, RMBS +592, KTOS +475, GEV +392, ETN +301; ABT position −22 after trim (stock −2.21%).
**ABT 止盈-减仓50% executed** (trade 2026-07-30-ABT-止盈减仓50-01): sold 25.29595 sh @ 105.61, proceeds 2,671.51, realized **+171.51**. Trigger: 7/30 official close 105.61 fell below the prior-day (7/29) low 106.97 — the pre-registered ACT-003 close-confirmed exhaustion/reversal after two closes above the 104.76 take-profit level, and ABT was the lone red name on a broad risk-on day (distribution). Remaining 25.29595 sh held (+6.86% vs cost). Position ratio 57.26% still above the DEFENSIVE 50% ceiling → ACT-004 keeps new builds blocked; satchel 8/8.

**[HISTORICAL] Settlement 2026-07-28 → 2026-07-29 (backfilled 2026-07-30, no trades):** total assets 99599.08 → 99135.95 (−463.13); ABT the only green name (108.00). GAP closed.
