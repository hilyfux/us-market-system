# Simulated Wallet

schema_version: 2.0
base_currency: USD
initial_capital: 100000.000000
last_reconciled_at: 2026-08-08T04:55:00+08:00
valuation_date: 2026-08-07
valuation_status: VERIFIED
valuation_source: 2026-08-07 official regular-session closes, settled SAME NIGHT at T+~50min. 8/8 names verified by 2 independent settled sources, max cross-source spread 0.39% (limit 1%): GEV 990.11 / ETN 448.65 / ABT 107.81 / PWR 671.72 from Alpha Vantage GLOBAL_QUOTE (latest trading day = 2026-08-07), cross-checked by stockanalysis compare at 0.00–0.02%; MP 51.11 / BE 219.34 / KTOS 60.77 / MSFT 499.99 from stockanalysis "At close: Aug 7, 2026, 4:00 PM EDT" stamps (AV daily quota exhausted after 4 calls), cross-checked by stockscan.io settled daily rows (KTOS 0.00%, MSFT 0.13%, MP 0.24%, BE 0.39%). Prev-close anchors: all 8 equal the 2026-08-06 VERIFIED closes to the cent. Benchmarks SPY 773.26 / QQQ 723.03 / IWM 301.56 (stockanalysis ETF compare, cross-checked by the stockscan S&P 500 index tick +0.62% vs SPY +0.61%). VIX 15.30 and US10Y 4.676% are single-source (TradingEconomics, Aug/07 stamp) = PARTIAL (see data/post-close.md).
prior_valuation_date: 2026-08-06 (superseded)

## Balances

| item | USD |
|---|---:|
| cash | 24030.225125 |
| GEV market value | 9789.670050 |
| ETN market value | 11196.817174 |
| ABT market value | 10383.392839 |
| PWR market value | 10621.874774 |
| MP market value | 11388.744651 |
| BE market value | 5303.440285 |
| KTOS market value | 12946.452407 |
| MSFT market value | 10257.046855 |
| total market value | 81887.439035 |
| total assets | 105917.664159 |
| cumulative P&L | 5917.664159 |
| realized P&L | -969.774755 |
| unrealized P&L | 6887.438915 |
| position ratio | 77.312354% |

## Position accounting

| symbol | quantity | cost | cost basis | reference close | market value | unrealized P&L |
|---|---:|---:|---:|---:|---:|---:|
| GEV | 9.887457 | 1011.38 | 10000.000000 | 990.11 | 9789.670050 | -210.329950 |
| ETN | 24.956686 | 400.69 | 10000.000000 | 448.65 | 11196.817174 | 1196.817174 |
| ABT | 96.311964 | 103.83 | 10000.000000 | 107.81 | 10383.392839 | 383.392839 |
| PWR | 15.812950 | 632.39 | 10000.000000 | 671.72 | 10621.874774 | 621.874774 |
| MP | 222.828109 | 44.88 | 10000.000000 | 51.11 | 11388.744651 | 1388.744651 |
| BE | 24.179084 | 206.79 | 5000.000000 | 219.34 | 5303.440285 | 303.440285 |
| KTOS | 213.040191 | 46.94 | 10000.000000 | 60.77 | 12946.452407 | 2946.452407 |
| MSFT | 20.514504 | 487.46 | 10000.000120 | 499.99 | 10257.046855 | 257.046735 |

## Validation

`cash + market_value = 24030.225125 + 81887.439035 = 105917.664159`

`total_assets - initial_capital = 5917.664159`

`cash traceability (C2): 100000 - 75000.000120 + (-969.774755) = 24030.225125` ✓

`cumulative = realized + unrealized (C6): -969.774755 + 6887.438915 = 5917.664159` ✓

Accounting difference: `0.000000`, within the required USD 0.05 tolerance. C1–C7 revalidated after the 2026-08-07 BE take-profit halving. **BE now carries an explicit `SIZE_EXCEPTION` tag** (cost basis $5,000 = legitimate half position after a partial take-profit); every other position is exactly $10,000 (MSFT 10000.000120 = quantization only).

**POST_CLOSE 2026-08-07 — settlement + take-profit (1 trade booked).** Broad risk-on tape into the July payrolls print (SPY +0.61% to 773.26, a new closing high; QQQ +1.17%; IWM +1.11%; VIX 15.30 → regime stays **RISK_ON**, ceiling 90%; US10Y 4.676%): total assets **104,900.12 → 105,917.66 (+1,017.55, +0.97%)**, beating SPY by +0.36pp; cumulative P&L **+4.90% → +5.92%, fifth consecutive all-time high**. Drivers (mv Δ): MP +806.64 (+7.62%, Q2 beat gets its price confirmation — revenue $108.49M vs $95.95M consensus, adj EBITDA positive; Trump hosted mining CEOs on critical-minerals supply chains), KTOS +715.82 (+5.85%, Javelin next-gen seeker award follow-through; now the strongest position at +29.46%), PWR +61.35 (+0.58%), ETN +11.48 (+0.10%, **ex-dividend $1.10 today** and still closed green — no exhaustion), MSFT +2.67 (+0.03%); ABT −14.45 (−0.14%), GEV −100.75 (−1.02%, the only losing position, cumulative −2.10%), BE −465.21 (−4.20%). **BE 止盈-减仓50% executed** (trade 2026-08-07-BE-止盈减仓50-01): sold 24.179084 sh @ 219.34, realized **+303.44**. The trigger was the numeric condition registered the previous night (close < 222.59 or < 221.21) — both hit, on expanding volume (14.75M vs 11.84M) and after a failed spike to 240.18, so the three reasons that justified holding on 8/6 all reversed. Thesis intact → halved, not exited; remaining 24.179084 sh (+6.07%) held with a SIZE_EXCEPTION tag. Cash 18,726.78 → 24,030.23; realized cum −1,273.22 → −969.77; position ratio 82.32% → **77.31%**; slots stay 8/8. Accounting note carried forward (still awaiting a user ruling): the C2 identity does not model dividends, so ETN's $27.45 ex-div cash inflow is not booked — no model change was made unilaterally.

**MORNING 2026-08-06 (valuation 2026-08-05) — deterministic replacement executed (2 trades).** First execution of the 2026-08-04 user-ruled replacement methodology: nine-dim rescore put RMBS at 68 (weakest, 2nd consecutive day) vs candidate MSFT 85 → diff +17 ≥ 5 gate. All three of yesterday's blockers cleared overnight: (1) regime back to RISK_ON (VIX 15.81 < 16, 2-source) → 90% ceiling, post-trade ratio 82.12% within; (2) MSFT 8/5 close 487.46 verified 2-source 0.00% OHLC-exact; (3) 3-day surge +4.89% ≤ 8% (464.72→487.65→492.81→487.46). **Sold RMBS 87.926808 sh @97.30** (trade 2026-08-05-RMBS-平仓-01), realized **−1,444.721582** — exit by relative-certainty ranking, not stop-loss; DDR5 thesis not impaired (entry timing was the recorded lesson). **Bought MSFT 20.514504 sh @487.46** (trade 2026-08-05-MSFT-建仓-01), cost basis 10,000.000120; planned stop official close < 437.00 (−10.35%, risk ≈1.0% NAV, close-confirmed); no fixed take-profit (ACT-003 only). Cash 20,171.51 → 18,726.78; realized cum +171.51 → −1,273.22; total assets unchanged 104,732.78 (trade at market); position ratio 80.74% → 82.12%. Slots stay 8/8; theme mix now ai_power 4 / defense 1 / rare_earth 1 / healthcare 1 / ai_software 1 (ai_memory exited).

**POST_CLOSE 2026-08-05 — settlement (no trades).** Consolidation day after two big risk-on sessions (SPY −0.20% to 769.79 after a new intraday 52-wk high 776.85; QQQ −0.90%; IWM −0.64%; VIX 15.81 back below 16 → regime CHOPPY→**RISK_ON**, ceiling 75%→90%; ISM services 54.1 vs 54.5 est, employment sub-index 47.4 weak; NFP Friday): total assets **103,951.12 → 104,732.78 (+781.66, +0.75%)**, beating SPY by +0.95pp; cumulative P&L **+3.95% → +4.73%, third consecutive all-time high**. 5/8 green — drivers (mv Δ): KTOS +739.25 (+6.69%, post-earnings day-2 rally; intraday spike to 62.34 faded ~11% but the close held far above prior close → NO exhaustion-close confirmation, ACT-003 not triggered, held), BE +300.79 (+2.73%, class action now FILED but no company-disclosed financial impact and no price damage → held, status upgraded to filed-case watch), MP +98.04 (+0.93%, Q2 tomorrow AH; consensus revenue corrected ~$935M→~$96M — bad source caught by the pre-earnings recheck), ETN +64.64 (+0.56%, 3rd straight day touching a new 52-wk high 453.50; ex-div $1.10 on 8/7), ABT +24.08 (+0.24%); GEV −1.09 (−0.01%), PWR −158.29 (−1.44%, post-earnings consolidation), RMBS −285.76 (−3.23%, semis pullback; $100M ASR = supportive IR). Actions: all 8 持有. HYP-001 window (7/29→8/5) adjudicated COUNTER — BE +43.1% vs theme peers (GEV +13.1%, ETN +23.6%); remains HYPOTHESIS with lowered confidence. Regime **RISK_ON** (VIX 15.81 < 16; SPY >> MA50 ~747) → 90% ceiling; position ratio 80.74% back WITHIN ceiling (over-ceiling flag cleared); slots 8/8.

**POST_CLOSE 2026-08-04 — settlement (no trades).** Second consecutive broad risk-on day (SPY +1.79% to 771.24; QQQ +3.40%; IWM +1.85%; VIX 16.41 — back above 16 → regime RISK_ON→**CHOPPY**, ceiling 90%→75%; US10Y 4.63% −5bp): total assets **101,053.26 → 103,951.12 (+2,897.86, +2.87%)**, beating SPY by +1.08pp; cumulative P&L **+1.05% → +3.95%**, second consecutive all-time high. 7/8 green — drivers (mv Δ): MP +808.87 (+8.28%, rare-earth policy narrative + pre-earnings squeeze), RMBS +733.31 (+9.04%, 4th recovery day, reclaimed 100), KTOS +566.69 (+5.41%, eve-of-print bid), BE +473.43 (+4.48%), PWR +202.41 (+1.88%), ETN +161.22 (+1.47%, new 52-wk high 444.69), GEV +111.83; ABT −159.88 (−1.55%, lone red, defensives out of rotation). Actions: all 8 持有 — **KTOS Q2 reported AH: EPS $0.21 vs cons 0.13–0.15 BEAT, rev $458.8M (+30.5% YoY) BEAT, AH +3.6%** (L-002 hold-into-earnings positive sample #4; manage after tomorrow's confirming close); ETN 2nd straight new high, no exhaustion → ACT-003 unmet (CORE-004); BE AH law-firm class-action solicitations = noise pending verification (L-005); MP Q2 8/6 (ACT-005 blockade). Regime **CHOPPY** (VIX 16.41 ≥ 16; SPY >> MA50 745.89 actual / MA200 ~700 ref) → 75% ceiling; position ratio 80.60% **above ceiling** (legacy user-authorized balanced plan) → no forced sell, new builds blocked; slots 8/8.

**POST_CLOSE 2026-08-03 — settlement (no trades).** Broad risk-on rally (SPY +1.42% to 757.67; QQQ +1.76%; IWM +1.72%; VIX 15.86; US10Y 4.69% −5bp; strong ISM-manufacturing / industrial tape): total assets **98,160.72 → 101,053.26 (+2,892.53, +2.95%)**, beating SPY by +1.52pp; cumulative P&L **flips positive for the first time**: −1.84% → **+1.05%**. All 8 names green — drivers (mv Δ): BE +604.96 (+6.08%, premarket weakness falsified at close), ETN +574.75 (+5.55%, touched new 52-wk high 438.76 intraday), KTOS +556.03 (+5.60%, eve of Q2), MP +550.39 (+5.97%), PWR +203.04 (TD Cowen/Mizuho PT raises), GEV +162.85, ABT +136.76, RMBS +103.75. Actions: all 8 持有 — ETN strong close, no exhaustion → ACT-003 twin conditions unmet, no profit-taking on price alone (CORE-004); BE PREMARKET_RISK verdict = false alarm (L-005 noise call correct); KTOS Q2 tomorrow 8/4 AH (L-002 hold-into-earnings), MP Q2 8/6 (ACT-005 event blockade). Regime **RISK_ON** (VIX 15.86 < 16, SPY 757.67 > MA50 ~745, breadth broad: IWM +1.72%) → 90% ceiling; position ratio 80.04% within ceiling; slots 8/8.

**POST_CLOSE 2026-07-31 — settlement (no trades).** Risk-on big-tech day (SPY +0.72% to 747.03; QQQ +0.65%; IWM −0.48%; VIX −6.44% to 15.99): total assets **97,127.42 → 98,160.72 (+1,033.30, +1.06%)**, beating SPY by +0.34pp; cumulative P&L improved −2.87% → **−1.84%**. Driver: ETN Q2 record beat (+7.32%, mv +706.52, flipped to profit +362.02); PWR +148.33 (Guggenheim upgrade), RMBS +123.98, KTOS +91.61, GEV +82.16, ABT +8.67; MP −64.62, BE −63.35. All 8 actions = 持有 (ETN catalyst realized but close strong, no exhaustion → ACT-003 not triggered). Regime RISK_ON (boundary: VIX 15.99, SPY back above 50d ref 744.72) → 90% ceiling; position ratio 79.45% now within ceiling; slots 8/8, no new builds possible.

**Correction 2026-07-31 (user override): ABT topped up to the uniform $10,000.** The earlier decision to keep ABT at its trimmed $2,500 was my own judgment and contradicted the explicit "every target = $10,000" directive — corrected: bought 71.016014 sh @ 105.61 ($7,500.00, trade 2026-07-31-ABT-均衡加仓-01). All 8 positions now carry exactly $10,000 cost basis (Σ = $80,000); cash 27,671.51 → 20,171.51; position ratio **79.23%** (user-authorized override of the DEFENSIVE ceiling for the balanced plan). A new preflight check (C7 sizing uniformity) now fails loudly if any OPEN position's cost basis deviates from the $10k standard without an explicit SIZE_EXCEPTION tag.

**Balance rebalance 2026-07-31 (user-directed; 7 add trades booked).** Per user instruction to restore the balanced $10,000-per-position plan, 7 positions were topped up to **$10,000 cost basis** each by buying at 7/30 official closes (GEV/ETN/PWR/MP/BE/KTOS/RMBS). ABT kept at its trimmed $2,500 (re-adding would merely reverse the 7/30 take-profit at the same price — pointless churn). Buys total **$13,843.35**; cash 41,514.85 → 27,671.51; Σ(cost_basis) 58,656.65 → 72,500.00. **Rebalancing at market does not change total assets (97,127.42), unrealized (−3,044.08) or cumulative P&L (−2,872.58)** — it only redeploys cash to equalize sizes. Position ratio **57.26% → 71.51%** — an **explicit, user-authorized override** of the DEFENSIVE 50% ceiling and of the "don't add to losers" discipline (ACT-002/L-005), accepted to build balanced per-name trade data for strategy optimization. New builds remain blocked (over cap). This is out-of-band (not a MORNING/POST_CLOSE run); each add carries a trade_id.

**Realized-P&L accounting (first realized trade — C2 extended 2026-07-31):** with a non-zero realized P&L, cash is sourced as `initial − Σ(cost_basis) + realized`. C2 was extended to this identity (backward-compatible: identical to the old form while realized = 0; all 150 selftests green). Here `100000 − 58656.653101 + 171.506542 = 41514.853441 = cash` ✓; C6 `realized 171.506542 + unrealized −3044.082635 = −2872.576093 = cumulative` ✓.

**MORNING 2026-07-30 — settlement + take-profit (trade booked).** 7/29 → 7/30 broad risk-on rally (SPY +1.68% to 741.69; VIX −17.3% to 17.09; Nasdaq +2.78%, SOX +8.2%; PCE inflation cooled). Total assets **91,590.15 → 97,127.42 (+5,537.28, +6.05%)**; cumulative P&L improved −8.41% → **−2.87%**. Drivers (mv Δ): PWR +1,453 (Q2 big beat, +17.26%), BE +1,773 (+26.49%, Mizuho upgrade), MP +672, RMBS +592, KTOS +475, GEV +392, ETN +301; ABT position −22 after trim (stock −2.21%).
**ABT 止盈-减仓50% executed** (trade 2026-07-30-ABT-止盈减仓50-01): sold 25.29595 sh @ 105.61, proceeds 2,671.51, realized **+171.51**. Trigger: 7/30 official close 105.61 fell below the prior-day (7/29) low 106.97 — the pre-registered ACT-003 close-confirmed exhaustion/reversal after two closes above the 104.76 take-profit level, and ABT was the lone red name on a broad risk-on day (distribution). Remaining 25.29595 sh held (+6.86% vs cost). Position ratio 57.26% still above the DEFENSIVE 50% ceiling → ACT-004 keeps new builds blocked; satchel 8/8.

**[HISTORICAL] Settlement 2026-07-28 → 2026-07-29 (backfilled 2026-07-30, no trades):** total assets 99599.08 → 99135.95 (−463.13); ABT the only green name (108.00). GAP closed.
