# Alert State

schema_version: 2.0
last_reconciled_at: 2026-08-04T08:38:00+08:00

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

## Pending close signals

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
