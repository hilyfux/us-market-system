# Alert State

schema_version: 2.0
last_reconciled_at: 2026-07-30T21:02:38+08:00

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

## Pending close signals

- RMBS RED_PENDING_CLOSE (Q2 7/27) — **CLEARED 2026-07-28**: EPS beat verified, position held.
- BE Q2 (7/28 after close) — **CLEARED** (fundamentals). 7/29 price-confirmation **DONE (2026-07-30 morning backfill)**: verified close 163.75 (−1.85%, intraday 185.66→157.33) — the +12.7% AH pop fully retraced, broad PT cuts (Jefferies/BMO/Truist to Hold). Thesis intact (record quarter), no verified impairment → held (advisory); no stop triggered. Sell-the-news divergence confirmed (lessons L-011 / HYP-001).
- ABT take-profit 104.76 — **REVERSAL SIGNAL TRIGGERED 2026-07-30 (pending 2-source verify).** Observed 7/30 close 105.54 (−2.28%) is BELOW the prior-day (7/29) low 106.97 and was the only red name on a broad risk-on rebound day (SPY +1.68%) = the first official-close exhaustion/reversal after two closes above 104.76 → the pre-registered ACT-003 trigger ("收盘跌破前日低点") is MET. Still above 104.76 (+6.8% vs cost). **止盈-减仓50% AUTHORIZED but NOT executed** tonight: single approved source only (AV quota exhausted) → data gate ACT-001 blocks. Execute at 2026-07-31 MORNING once the 7/30 close is verified by ≥2 independent sources. → YELLOW_PENDING_CLOSE.
- PWR Q2 (2026-07-30 pre-open) — **CLEARED (fundamentals), thesis strengthened.** adj EPS $4.24 vs $3.31 consensus (big BEAT); FY26 adj EPS guide raised to $16.45-16.95 from $13.55-14.25; observed +16.8% to ~655.37 (above cost proxy 631.02, flipped to profit). "Hold into earnings" (L-002) paid off. No exhaustion → hold, no trim. Price VERIFIED pending 7/31 backfill.
- 2026-07-30 settlement — **GAP (open)**: POST_CLOSE at T+31min, AV exhausted + stockanalysis table-vs-realtime divergence on big movers → P1 (≥2 sources) unmet. valuation_date held at 2026-07-29. Backfill + ABT take-profit execution at 2026-07-31 MORNING (see data/post-close.md).
- 2026-07-29 settlement — **CLOSED → VERIFIED (2026-07-30 morning backfill)**: 8/8 closes settled; wallet names GEV 900.28 / ETN 361.88 / ABT 108.00 confirmed by 2 fresh independent sources (stockanalysis history + Google Finance) at 0.00% incl. OHLC. valuation_date advanced to 2026-07-29; wallet 99,135.95; C1–C6 diff=0; W1 lag=0.
