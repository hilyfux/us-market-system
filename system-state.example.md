# System State

schema_version: 2.0
system_name: us-stock-decision-system
state_root: /Users/linqing.wang/Desktop/Claude/us-stock-system
last_reconciled_at: 2026-07-25T13:36:00+08:00
last_successful_official_settlement: 2026-07-16
last_verified_revaluation: 2026-07-24 (out-of-band reconciliation performed 2026-07-25; NOT a POST_CLOSE settlement)
market_regime: DEFENSIVE (carried forward; 50% ceiling, non-binding at 14.95% invested)
strategy_version: 2.0.0
slot_limit: 8
slots_occupied: 8
slots_available: 0
slots_manageable: 3
slots_frozen: 5
slots_frozen_symbols: PWR, MP, BE, KTOS, RMBS
slots_note: 满槽。新机会只能通过替换进入。冻结 = 真实持仓且数量未知，占用额度但无法计市值/无法定量管理，占总额度 62.5%。旧字段 open_slots 语义不明（已占用还是可用？）已废弃，改由 lib/market_core.py: slot_report() 计算。

## Notification

channel: enterprise_wechat
webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=<YOUR_KEY_HERE>
success_condition: errcode=0
retry_policy: no_retry
ordering: state_write_then_send

## Task responsibilities

| task | role | may change simulated holdings | notification policy |
|---|---|---|---|
| us-market-system | Single ET-aware router for MORNING, PREMARKET, INTRADAY and POST_CLOSE | MORNING/POST_CLOSE: yes after all gates; INTRADAY: only if playbook explicitly permits; PREMARKET: no | Stage-specific deduplicated report after successful state write; premarket system failure must also be pushed |

## Health and recovery

- Previous root under `/Users/wanglinqing/Claude/Scheduled/...` was protected and unavailable to task runs.
- Canonical state migrated to a connected Documents folder on 2026-07-16.
- Migrated to new machine on 2026-07-17; canonical root is now `/Users/linqing.wang/Desktop/Claude/us-stock-system` (connected Desktop/Claude folder).
- Baseline contains five real OPEN positions and two simulated OPEN positions.
- July 15 closes are reconciliation references and must be refreshed before the next trade or official settlement.
- Historical task failures caused by certificate/authorization errors did not create trades or dedupe keys.
- If any required state file is inaccessible, malformed, or cross-file inconsistent: do not initialize elsewhere, do not trade, do not notify a normal report; write a local failure only if the canonical root is writable.

## Last reconciliation

status: PASS_WITH_REFERENCE_PRICES
cash_market_value_difference: 0.000000
trade_ids_added: 0
positions_changed: 0
notifications_sent: 1

## Intraday run — 2026-07-16T10:30:52-04:00

report_key: INTRADAY+2026-07-16+10
status: NOTIFIED
notification_result: errcode=0
market_status: NYSE_NASDAQ_NORMAL_CONTINUOUS
positions_evaluated: 7
trade_instructions_generated: 0
simulated_trades_executed: 0
accounting_status: PASS_NO_TRADE
quote_window: 2026-07-16T10:16:00-04:00 to 2026-07-16T10:17:06-04:00
note: Intraday quotes were within 20 minutes at evaluation; no action passed the playbook's fact-plus-confirmation gates. Real quantities remain unknown and intraday marks were not booked as official settlement values.

## Morning run — 2026-07-17T08:08:00+08:00

status: NOTIFIED
market_date: 2026-07-16
market_regime: DEFENSIVE
regime_position_limit: 50%
benchmarks: SPY 750.83; QQQ 705.89; IWM 295.59; VIX 16.73; US10Y 4.57%; NYSE decliners/advancers 1.08
positions_evaluated: 7 prior OPEN plus 1 new simulated position
position_actions: PWR 持有; MP 持有; BE 持有; KTOS 持有; RMBS 持有; GEV 持有; ETN 持有; ABT 建仓
simulated_trade_id: 2026-07-17-ABT-建仓-01
simulated_trade_value: 4999.997477
open_slots_after: 8
scan_coverage: 3 themes; 8 candidates; 5 industries
scan_leaders: ABT 87; PLD 85; USB 83; JPM 82; NDAQ 80; STT 79; CVX 78; ISRG 71
active_rules: ACT-001 PASS; ACT-002 no exit authorized; ACT-003 no profit exit authorized; ACT-004 ABT entry authorized
accounting_status: PASS
cash_market_value_difference: 0.000000
cumulative_pnl_difference: 0.000000
files_updated: portfolio-ledger.md; sim-wallet.md; system-state.md
notification_status: SENT
notification_result: errcode=0
notification_sent_at: 2026-07-17T08:08:00+08:00

## Post-close run — 2026-07-17T09:22:27+08:00

status: DATA_FAILURE
market_date: 2026-07-16
market_status: NYSE_NASDAQ_NORMAL_CLOSE_CONFIRMED
failure_gate: ACT-001
failure_reason: Independent regular-close sources conflicted with canonical VERIFIED marks by more than 1% for multiple symbols (including MP and ABT); official-close data could not be reconciled safely.
settlement_status: BLOCKED
positions_evaluated: 0
position_actions: 持有（data gate）
simulated_trades_executed: 0
trade_ids_added: 0
accounting_status: NOT_REVALUED_LAST_VERIFIED_STATE_PRESERVED
strategy_version: 2.0.0
files_updated: system-state.md
notification_status: NOT_SENT
notification_reason: DATA_FAILURE; normal post-close report prohibited; no retry attempted

## Intraday run — 2026-07-16T11:31:01-04:00

report_key: INTRADAY+2026-07-16+11
status: NOTIFIED
notification_result: errcode=0
notification_sent_at: 2026-07-16T11:31:01-04:00
market_status: NYSE_NASDAQ_NORMAL_CONTINUOUS
positions_evaluated: 8
trade_instructions_generated: 0
simulated_trades_executed: 0
accounting_status: PASS_NO_TRADE
quote_status: DATA_FAILURE_INTRADAY_NOT_VERIFIED_WITHIN_20_MINUTES
position_actions: PWR 持有; MP 持有; BE 持有; KTOS 持有; RMBS 持有; GEV 持有; ETN 持有; ABT 持有
risk_status: DATA_STALE_OR_UNVERIFIED_HOLD_ONLY
note: Exchanges were in normal continuous trading at 11:31 ET. Public indexed sources did not provide a complete, independently verified <=20-minute quote/volume set for all benchmarks and OPEN positions; ACT-001 therefore forced all actions to 持有. No intraday marks were booked as official settlement values.

> 模板：复制为 system-state.md 并填入真实 webhook。真实文件已被 .gitignore（含密钥 + 运行日志）。
