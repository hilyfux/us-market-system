# Simulated Wallet

schema_version: 2.0
base_currency: USD
initial_capital: 100000.000000
last_reconciled_at: 2026-07-25T13:05:00+08:00
valuation_date: 2026-07-24
valuation_status: VERIFIED
valuation_source: 2026-07-24 official regular-session closes, >=2 independent sources per symbol, 0.00% discrepancy
prior_valuation_date: 2026-07-16 (superseded; 6-trading-day gap closed 2026-07-25)

## Balances

| item | USD |
|---|---:|
| cash | 85000.011991 |
| GEV market value | 4866.436575 |
| ETN market value | 4862.214717 |
| ABT market value | 5214.001214 |
| total market value | 14942.652506 |
| total assets | 99942.664497 |
| cumulative P&L | -57.335503 |
| realized P&L | 0.000000 |
| unrealized P&L | -57.335503 |
| position ratio | 14.951225% |

## Position accounting

| symbol | quantity | cost | cost basis | reference close | market value | unrealized P&L |
|---|---:|---:|---:|---:|---:|---:|
| GEV | 4.7957 | 1042.60 | 4999.996820 | 1014.75 | 4866.436575 | -133.560245 |
| ETN | 12.0331 | 415.52 | 4999.993712 | 404.07 | 4862.214717 | -137.778995 |
| ABT | 50.5919 | 98.83 | 4999.997477 | 103.06 | 5214.001214 | 214.003737 |

## Validation

`cash + market_value = 85000.011991 + 14942.652506 = 99942.664497`

`total_assets - initial_capital = -57.335503`

Accounting difference: `0.000000`, within the required USD 0.05 tolerance. Both conservation identities recomputed at full precision on 2026-07-25 and both returned exactly 0.000000.

July 24 official closes passed the data gate (ACT-001): every symbol confirmed by >=2 independent sources at 0.00% discrepancy, correct session date, official regular close (after-hours prints explicitly excluded). Real positions remain intentionally excluded from market value because their quantities are UNKNOWN.

**Revaluation 2026-07-16 → 2026-07-24 (no trades):** total assets 99737.766259 → 99942.664497, **+204.898238**; cumulative P&L −262.233741 → −57.335503, i.e. the drawdown narrowed by USD 204.90 to −0.0573% of initial capital. Cash unchanged at 85000.011991 (zero trades). Position ratio 14.78% → 14.95%, far below the defensive-regime 50% ceiling, so ACT-004 is non-binding.

Driver attribution over the period (market-value deltas, sum = +204.898238): **ABT +214.003737**, **ETN +93.858180**, **GEV −102.963679**. ABT is the only position profitable against cost (+4.28%); ETN and GEV both remain below cost in absolute terms (−2.76% and −2.67% respectively) even though ETN's mark rose over this specific window. Relative to SPY (−1.58% over the same span) the simulated book gained, driven by ABT and ETN.
