# Simulated Wallet

schema_version: 2.0
base_currency: USD
initial_capital: 100000.000000
last_reconciled_at: 2026-07-25T13:05:00+08:00
valuation_date: 2026-07-29
valuation_status: VERIFIED
valuation_source: 2026-07-29 official regular-session closes; wallet names GEV/ETN/ABT confirmed by 2 independent FRESH sources (stockanalysis history + Google Finance) at 0.00%; backfilled 2026-07-30 morning via history-page method (AV daily quota exhausted; roic/stocktitan/stockscan still lagged 7/28 at run time, so Google Finance served as the settled second source — all three names matched to the penny incl. OHLC)
prior_valuation_date: 2026-07-28 (superseded)

## Balances

| item | USD |
|---|---:|
| cash | 38843.348161 |
| GEV market value | 4317.472796 |
| ETN market value | 4354.538228 |
| ABT market value | 5463.925200 |
| PWR market value | 8421.364664 |
| MP market value | 7188.677520 |
| BE market value | 6694.329250 |
| KTOS market value | 9105.622172 |
| RMBS market value | 7200.867765 |
| total market value | 52746.797595 |
| total assets | 91590.145756 |
| cumulative P&L | -8409.854244 |
| realized P&L | 0.000000 |
| unrealized P&L | -8409.854244 |
| position ratio | 57.590036% |

## Position accounting

| symbol | quantity | cost | cost basis | reference close | market value | unrealized P&L |
|---|---:|---:|---:|---:|---:|---:|
| GEV | 4.7957 | 1042.60 | 4999.996820 | 900.28 | 4317.472796 | -682.524024 |
| ETN | 12.0331 | 415.52 | 4999.993712 | 361.88 | 4354.538228 | -645.455484 |
| ABT | 50.5919 | 98.83 | 4999.997477 | 108.00 | 5463.925200 | 463.927723 |
| PWR | 15.0076 | 631.02 | 9470.095752 | 561.14 | 8421.364664 | -1048.731088 |
| MP | 188.6792 | 45.46 | 8577.356432 | 38.10 | 7188.677520 | -1388.678912 |
| BE | 40.8814 | 206.73 | 8451.411822 | 163.75 | 6694.329250 | -1757.082572 |
| KTOS | 207.5119 | 46.96 | 9744.758824 | 43.88 | 9105.622172 | -639.136652 |
| RMBS | 86.9565 | 114.00 | 9913.041000 | 82.81 | 7200.867765 | -2712.173235 |

## Validation

`cash + market_value = 38843.348161 + 52746.797595 = 91590.145756`

`total_assets - initial_capital = -8409.854244`

Accounting difference: `0.000000`, within the required USD 0.05 tolerance. C1–C6 revalidated by preflight after the 2026-07-30 migration.

**Unified demo book — migration 2026-07-30 (no market trade; a booking of already-owned positions):** the five formerly-advisory names (PWR/MP/BE/KTOS/RMBS) were folded into the simulated account at their recorded cost basis (7/16-close proxy; RMBS at user-corrected 114.00), total cost basis $46,156.66. Cash was debited by that amount (85,000.011991 → 38,843.348161), initial capital held at $100,000. All 8 positions now count in market value and P&L and are actively traded. Sum(cost_basis) over 8 = 61,156.651839, so C2 (100,000 − sum cost_basis = cash) holds. Position ratio 57.59% is above the DEFENSIVE 50% ceiling — no new builds until it falls (ACT-004); existing positions are held/managed per ACT-002/003.

July 29 official closes passed the data gate (ACT-001) for GEV/ETN/ABT (≥2 independent fresh sources at 0.00%); the migrated names carry 7/29 closes from the same 7/30 backfill (Google Finance settled source), PROXY cost until real fills are provided.

**Settlement 2026-07-28 → 2026-07-29 (backfilled 2026-07-30 morning, no trades):** total assets 99599.08 → 99135.95 (−463.13); drivers: GEV −206.69, ETN −293.37, ABT +36.93. Broad risk-off day (FOMC held rates; SPY −1.54%, VIX +13% to 20.66, AI-power/semis/defense all sharply lower). ABT closed 108.00 (+0.68%), the only green name — 2nd consecutive close above the 104.76 take-profit but a fresh high on strength (not exhaustion) → held full (ACT-003/L-003). Book −0.47% vs SPY −1.54% (+1.08pp) — ABT's defensive character offset the GEV/ETN AI-power drag; this GAP-closing backfill also resolves the 2026-07-29 POST_CLOSE settlement gap.

**[HISTORICAL] Revaluation 2026-07-16 → 2026-07-24 (no trades):** total assets 99737.766259 → 99942.664497, **+204.898238**; cumulative P&L −262.233741 → −57.335503, i.e. the drawdown narrowed by USD 204.90 to −0.0573% of initial capital. Cash unchanged at 85000.011991 (zero trades). Position ratio 14.78% → 14.95%, far below the defensive-regime 50% ceiling, so ACT-004 is non-binding.

Driver attribution over the period (market-value deltas, sum = +204.898238): **ABT +214.003737**, **ETN +93.858180**, **GEV −102.963679**. ABT is the only position profitable against cost (+4.28%); ETN and GEV both remain below cost in absolute terms (−2.76% and −2.67% respectively) even though ETN's mark rose over this specific window. Relative to SPY (−1.58% over the same span) the simulated book gained, driven by ABT and ETN.

**Settlement 2026-07-24 → 2026-07-27 (backfilled 2026-07-28, no trades):** total assets 99942.66 → 99862.49 (−80.18); drivers: ABT +72.35, GEV −87.19, ETN −65.34. ABT closed 104.49, 0.26% below the 104.76 take-profit trigger (not hit).
