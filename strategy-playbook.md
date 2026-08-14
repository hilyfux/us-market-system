# Strategy Playbook

VERSION: 2.1.1
last_updated: 2026-08-13

## CORE

- CORE-001 — The ledger is the only position/trade truth; the wallet covers simulated capital only.
- CORE-002 — Single simulated (demo) book (as of 2026-07-30): the system actively trades all positions (build/add/reduce/close in MORNING/POST_CLOSE with a unique trade_id and accounting validation). Redefining an existing position (cost correction, migrating in an externally-held position) still requires explicit user confirmation. The former advisory "real position" separation is retired.
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
- Action impact: initial position normally **10% of NAV (= $10,000 at $100k initial; proportional/balanced, user 2026-07-31)**; single-name <=20%; industry <=35%; planned trade risk <=1% of total assets. Anchored in code: `selection.BASE_INITIAL_PCT` (selftest-locked). High-beta names are halved by ACT-007 before this.
- Sample count: system control rule
- Validation metric: every new trade satisfies all gates
- Enabled: 2026-07-16
- Rollback: any failed gate blocks the trade

### ACT-005 — Event-timing gate (enter after confirmation, not before)

- Environment: new-position scan (build/add only; never affects holding existing positions)
- Trigger: the candidate has a binary catalyst (earnings) within 5 trading sessions → block initiation; wait for the post-event confirming official close
- Action impact: no new build/add inside the blackout; existing positions still `持有`
- Sample count: promoted from L-010 (ABT post-beat entry = only clearly profitable name; BE/RMBS pre-earnings entries bled)
- Validation metric: no new position initiated within 5 sessions before its earnings
- Enabled: 2026-07-30
- Rollback: revert if event-confirmed entries do not outperform pre-event entries over the next 10 fresh entries
- Implementation: `lib/selection.py: event_timing_gate` (selftest-locked)

### ACT-006 — Thesis-concentration cap at entry

- Environment: new-position scan
- Trigger: after the proposed build, combined **same-thesis** exposure (theme tag, not GICS industry) would exceed 25% of NAV
- Action impact: block the build (or halve it to fit); unregistered-theme names are conservatively rejected until tagged
- Sample count: promoted from L-009/L-012 (a single FOMC catalyst hit 45% of the book at once)
- Validation metric: no build leaves same-thesis exposure above 25% of NAV
- Enabled: 2026-07-30
- Rollback: adjust cap only via a documented review; never silently
- Implementation: `lib/selection.py: theme_cap_gate` + `THEME_TAGS` (selftest-locked)

### ACT-007 — Volatility-scaled sizing

- Environment: new-position scan
- Trigger: candidate is high-beta/high-volatility
- Action impact: halve the nominal starting size (base 10% → 5%, i.e. $10,000 → $5,000 at $100k) before applying ACT-004/ACT-006
- Sample count: promoted from L-008 (equal-weight sizing across high-vol names turned one week's tape into the entire cost basis)
- Validation metric: every high-beta new entry is sized at ≤ half the base
- Enabled: 2026-07-30
- Rollback: revert if half-sizing measurably worsens risk-adjusted return without reducing drawdown
- Implementation: `lib/selection.py: volatility_scaled_size` (selftest-locked)

> ACT-005/006/007 run together in `selection.screen_new_position()` during the MORNING opportunity scan, upstream of ACT-004's score/risk gates. They encode the daily-review purpose: reflection → codified rule → measurable on the ledger.

## HYPOTHESIS

- HYP-001 — Crowded-theme "sell the news" (post-beat close reversal)
  - Environment: crowded/high-expectation theme
  - Trigger: a name reports an earnings beat with raised guidance, yet the next official close fully retraces the event-driven gain (AH pop given back) alongside broad sell-side PT cuts
  - Proposed action impact: treat as an over-crowding/over-expectation signal — reduce willingness to chase that theme; do NOT force an exit (thesis intact) but avoid adds
  - Sample count: 2 mixed (1 support, 1 counter) — BE 2026-07-29 set the sell-the-news close; BE 2026-07-30 (+26.5% on Mizuho upgrade to Outperform, just 1 session later) is a **counter-sample** (sharp mean-reversion, not continued underperformance). Net evidence inconclusive; still needs >=3 independent trading days or 5 samples before promotion. Do NOT reject on the single counter-day (no single-day overfit). Tracking (window 7/29 + 3-5 sessions, through ~8/5): 7/31 BE -0.63% while theme peers rose (GEV +0.85%, PWR +1.43%, ETN +7.32%) = weak supporting observation for the underperformance metric; still inconclusive. **Window adjudication 2026-08-05 POST_CLOSE (7/29 + 5 sessions, window complete): COUNTER** — BE closed 234.33 on 8/5, +43.1% vs the 7/29 sell-the-news close 163.75, strongly OUTPERFORMING theme peers over the full window (GEV +13.1%, ETN +23.6%, PWR ~+16%); the validation metric (subsequent 3-5 session underperformance) failed. Tally: 1 weak single-day support vs 1 full-window counter → confidence lowered; remains HYPOTHESIS (not REJECTED — needs 3 consecutive failures / more samples; next test = the next crowded-theme post-beat reversal close). **2026-08-10 POST_CLOSE: no new sample** — no holding produced the pattern (an earnings beat whose next official close fully retraces the event gain); tally unchanged at 1 weak support vs 1 full-window counter, status stays HYPOTHESIS at lowered confidence.
  - Validation metric: names showing this pattern subsequently underperform their theme peers over the next 3–5 sessions
  - Enabled: no (HYPOTHESIS only)
  - Source lesson: lessons.md#L-011

- HYP-002 — New closing high on contracting volume (缩量新高)
  - Environment: a position makes its highest close since entry
  - Trigger: the new closing high is set on volume materially BELOW the prior session's volume (staged threshold: −25% or more)
  - Proposed action impact: none by itself — it is a *quality-of-advance* marker, not an exit. Use it to (a) require the ACT-003 numeric exhaustion criterion to be tightened to the new session's low, and (b) reduce willingness to add to that name.
  - Sample count: 2 staged 2026-08-11 (KTOS +2.10% to a new high on 2.74M vs 4.10M = −33%; ETN +3.22% to its highest close since entry on 1.81M, prior-session volume not captured — recorded as incomplete, must be filled before this counts as a second clean sample). **2026-08-14 adjudication of the KTOS clean sample: AGAINST** — the 3-session give-back window closed with KTOS at 64.58, +3.46% above the 62.42 pre-high base (no give-back; the tariff catalyst on day 3 is a confound, recorded). Clean samples: 1 adjudicated (against), 0 pending.
  - Validation metric: names showing the pattern give back the new-high advance within the next 3 sessions more often than names making new highs on expanding volume; measured against each name's own theme peers
  - Enabled: no (HYPOTHESIS only — 1 clean sample, needs ≥3 independent trading days)
  - Source lesson: extends L-015 (numeric criteria over pattern impressions) — this deliberately does NOT create a discretionary exit, only a criterion-tightening input
  - Explicit anti-overfit note: staged from a single session; if the next two occurrences do not show the give-back, mark REJECTED rather than loosening the definition.

New hypotheses need at least three independent trading days or five relevant samples before promotion.

## REJECTED

None recorded.

## Change log

- 2026-08-14 (no version bump, VERSION stays 2.1.1) — **Settlement + one take-profit trade; no rule changed.** **ETN 止盈-减仓50% @451.51** (realized +634.10) — the first exit executed purely off the registered criteria ladder: the 8/13-tightened two-leg criterion (close < 452.50 AND expanding volume) hit exactly one session after the volume leg's absence justified a hold — the ladder discriminated correctly on both nights, a strong L-015 positive pair. **LLY breakout-failure line confirmed** (1180.16 < ex-div-corrected 1183.98): entry-day breakout officially failed on day 5; review trigger only, stop 1113.95 intact — flagged weakest-candidate for the next rescore. **HYP-002 adjudicated AGAINST on its only clean sample** (KTOS closed the 3-session window +3.46% above base; tariff-catalyst confound recorded): stays HYPOTHESIS, confidence lowered, needs fresh clean samples before any promotion path. Close-confirmed-exit evidence (ACT-002/003) unchanged at 2 clean recovery samples.
- 2026-08-13 (no version bump, VERSION stays 2.1.1) — **Settlement only, no trades.** No CORE/ACT rule changed. Both intraday flags adjudicated at the close: **ETN** hit its registered review line (453.33 < 459.03) but the ACT-003 volume leg was absent (volume −31%) and the preserved 446.50 two-day reduction criterion was untouched → hold, with the next-day line tightened to 452.50-with-volume — the registered criteria ladder was followed rather than a pattern impression (L-015). **KTOS** breached 62.10 intraday (low 61.84) and recovered to close 62.79 on −24% volume → **5th consecutive falsification** of the exhaustion registration and the **second clean intraday-breach-then-close-recovery sample** (after LNG 8/12) — accumulating direct evidence for close-confirmed exits (ACT-002/003). **HYP-002 (缩量新高)**: no new clean sample today (LLY's expanding-volume decline is the opposite shape on the downside; the KTOS 8/11 sample's 3-session give-back window closes at the 8/14 close — adjudicate then); clean-sample count stays 1. HYP-001 unchanged (HYPOTHESIS, lowered confidence).
- 2026-08-12 (no version bump, VERSION stays 2.1.1) — **Settlement only, no trades.** No CORE/ACT rule changed. All four registered close criteria adjudicated 未确认 with room (LLY 1220.28 vs 1185.71; LNG 268.11 vs 265.16 after an intraday breach to 262.01 — first clean intraday-breach-then-close-recovery sample supporting close-confirmed exits; MP 54.11 vs 52.90; KTOS 63.82 — 4th consecutive falsification of the exhaustion registration). **HYP-002 (缩量新高) clean-sample count stays 1**: today's marginal new high came on volume expanding 23%, the opposite shape, so it is not a sample. HYP-001 unchanged (HYPOTHESIS, lowered confidence).
- 2026-08-11 (no version bump, VERSION stays 2.1.1) — **Settlement + one staged hypothesis.** No CORE/ACT threshold or rule changed; no trades booked. Two intraday pending flags resolved as 未确认 (MP 收盘 55.24 远高于 52.66 判据；LLY 收盘 1215.02 高于 1185.71 突破失败线). Added **HYP-002 缩量新高** (not enabled, 1 clean sample) and registered ETN's first numeric exhaustion criterion. Separately, a real defect was fixed outside the playbook: `integrity.CheckResult` could not construct non-numeric expected/actual, so the **P4/P5 provenance guards had zero detection power** — fixed and locked by a new selftest assertion, and `stockscan.io` was given the `stamp_check` quirk after it served late-July tape for 5 of 8 names today (L-022).

- 2026-08-10 (no version bump, VERSION stays 2.1.1) — **Settlement-only maintenance.** No CORE/ACT threshold or rule changed; no trades booked. Two new lessons recorded in `knowledge/lessons.md` but deliberately NOT promoted to rules (1 sample each, below the >=3 independent trading days / 5 samples bar): **L-017** settlement pricing must first pass a same-source self-consistency check (quote header reproducible from prev close +/- stated change; history row finalised; full-day volume) before cross-source comparison — on 8/10 the stockanalysis quote header and its own provisional history row disagreed on PWR (660.86 vs 664.36) and ETN (444.96 vs 446.69) and roic.ai copied the same mid-session snapshot, so a naive "two sites agree" test would have booked PWR 1.1% wrong; **L-018** any single-day holding move >=5% must have its driving fact named in the review, or be explicitly logged as an information-free move — MP rose 6.95% on a day whose only dated company item was a Deutsche Bank target cut 61->58. **L-019** proxy-cost positions must be excluded from the entry-timing score used to judge method effectiveness (MP B+ and GEV D share the same 7/16-close proxy origin). HYP-001 unchanged (no new sample).

- 2.1.1 (2026-07-31) — **Initial position sizing restored to the balanced $10,000 plan.** ACT-004 base initial changed from 5% → **10% of NAV (= $10,000 at $100k, proportional so it scales with equity)** per user; high-beta halved to 5%/$5,000 via ACT-007. Anchored in `selection.BASE_INITIAL_PCT` and selftest-locked. Applies to **new entries only** — existing positions were opened under mixed conventions (3 sim @ $5k, ABT $2.5k post-trim, 5 migrated @ ~$8.5–9.9k) and are NOT force-rebalanced (equal-weighting to $10k each would need ~$80k invested = 82% ratio, far above the DEFENSIVE 50% ceiling, and would add to losers / undo the ABT take-profit).
- 2.1.0 (2026-07-30) — **First selection-strategy iteration promoted from daily reviews.** Codified three enforced entry gates from L-008/L-009/L-010/L-012: ACT-005 event-timing (no initiation ≤5 sessions before earnings; wait for the confirming close), ACT-006 thesis-concentration cap (same-theme exposure ≤25% NAV at entry), ACT-007 volatility-scaled sizing (half-size high-beta). Backed by `lib/selection.py` (deterministic) and selftest (13 new locking assertions). Rationale: the only clearly profitable name (ABT) was the one entered *after* earnings confirmation; the deep drawdowns came from pre-earnings entries stacked into one 45%-concentrated theme. HYP-001 (sell-the-news) intentionally NOT promoted — only 1 sample, below the ≥3-day/5-sample bar.
- 2.0.0 — Consolidated action vocabulary, data gating, real/sim separation, accounting order, and strategy promotion requirements across morning, intraday and post-close tasks.
