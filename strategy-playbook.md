# Strategy Playbook

VERSION: 2.0.0
last_updated: 2026-07-16

## CORE

- CORE-001 — The ledger is the only position/trade truth; the wallet covers simulated capital only.
- CORE-002 — Real position quantity or status changes only after explicit user execution confirmation.
- CORE-003 — No trade on unverified/stale/conflicting price data; the only allowed action is `持有` and the failure is recorded.
- CORE-004 — Never trade solely from a fixed percentage move or an intraday price touch.
- CORE-005 — State writes and accounting validation must succeed before a notification is sent.

## ACTIVE

### ACT-001 — Data-gate discipline

- Environment: all
- Trigger: source conflict over 1%, wrong date, delayed intraday quote over 20 minutes, or missing official close
- Action impact: block build/add/reduce/close; output `持有`; record DATA_FAILURE
- Sample count: system control rule
- Validation metric: zero trades using failed data
- Enabled: 2026-07-16
- Rollback: none; CORE safety control

### ACT-002 — Fundamental fact plus close confirmation

- Environment: all
- Trigger: verified thesis/fundamental impairment plus official-close technical confirmation
- Action impact: permit a stop-loss reduction/close with explicit proportion; real action remains unexecuted advice
- Sample count: system control rule
- Validation metric: every loss exit has both evidence classes
- Enabled: 2026-07-16
- Rollback: any exit lacking both evidence classes invalidates the signal

### ACT-003 — Profit exit quality gate

- Environment: profitable position
- Trigger: catalyst realization, trend exhaustion, or high-level price/volume risk confirmed at official close
- Action impact: permit explicit take-profit reduction/close percentage
- Sample count: system control rule
- Validation metric: no take-profit action on profit percentage alone
- Enabled: 2026-07-16
- Rollback: any percentage-only exit invalidates the signal

### ACT-004 — New-position risk sizing

- Environment: non-stress regime
- Trigger: score >=75, verified prior close, qualified trend, 3-day rise <=8%, explicit invalidation, calculable planned risk
- Action impact: initial position normally 5%; single-name <=20%; industry <=35%; planned trade risk <=1% of total assets
- Sample count: system control rule
- Validation metric: every new trade satisfies all gates
- Enabled: 2026-07-16
- Rollback: any failed gate blocks the trade

## HYPOTHESIS

- HYP-001 — Crowded-theme "sell the news" (post-beat close reversal)
  - Environment: crowded/high-expectation theme
  - Trigger: a name reports an earnings beat with raised guidance, yet the next official close fully retraces the event-driven gain (AH pop given back) alongside broad sell-side PT cuts
  - Proposed action impact: treat as an over-crowding/over-expectation signal — reduce willingness to chase that theme; do NOT force an exit (thesis intact) but avoid adds
  - Sample count: 1 (BE 2026-07-29) — needs >=3 independent trading days or 5 samples before promotion
  - Validation metric: names showing this pattern subsequently underperform their theme peers over the next 3–5 sessions
  - Enabled: no (HYPOTHESIS only)
  - Source lesson: lessons.md#L-011

New hypotheses need at least three independent trading days or five relevant samples before promotion.

## REJECTED

None recorded.

## Change log

- 2.0.0 — Consolidated action vocabulary, data gating, real/sim separation, accounting order, and strategy promotion requirements across morning, intraday and post-close tasks.
