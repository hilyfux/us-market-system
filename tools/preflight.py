#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight — 每次运行开头必须执行的守卫。退出码非 0 表示不得进入正常阶段流程。

它把「系统无法报告自己没在跑」这一根本缺陷补上：
    路由 + 陈旧度 + 存活 + 队列健康 + outbox 可用性 + 调度对齐 + 账务
任何一项 ERROR 级失败都会被命名并升级，而不是静默继续。

用法：
    python3 tools/preflight.py                # 人读
    python3 tools/preflight.py --json         # 机读
"""
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "lib"))

import market_core as mc      # noqa: E402
import integrity as ig        # noqa: E402
import outbox as ob           # noqa: E402
import state as st            # noqa: E402

CAL = mc.TradingCalendar(
    holidays={"2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
              "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25"},
    early_closes={"2026-11-27": mc.EARLY_CLOSE, "2026-12-24": mc.EARLY_CLOSE},
)
REQUIRED_CRON = ({0, 30}, {0, 1, 2, 3, 4, 5, 8, 20, 21, 22, 23})


def run(now=None):
    now = now or datetime.now(timezone.utc)
    report = {"now_utc": now.isoformat(timespec="seconds"), "checks": [], "escalations": []}

    def add(res):
        report["checks"].append(repr(res))
        if not res.passed and res.severity == "ERROR":
            report["escalations"].append(res.name)

    # 1. 路由
    r = mc.route(now, CAL)
    report["stage"] = r["stage"]
    report["route_reason"] = r["reason"]
    report["checkpoint"] = r.get("checkpoint")
    report["et"] = r["et"].isoformat(timespec="seconds")

    # 2. outbox 可用性（失败即 ENQUEUE_PATH_UNAVAILABLE，不得改写别处）
    try:
        p = ob.assert_path_usable()
        report["outbox"] = p
        report["outbox_ok"] = True
    except (ob.EnqueuePathUnavailable, ob.TccProtectedPath) as e:
        report["outbox_ok"] = False
        report["escalations"].append("ENQUEUE_PATH_UNAVAILABLE")
        report["outbox_error"] = str(e)
        p = None

    # 3. 状态文件 + 陈旧度 + 账务
    try:
        s = st.load_all(os.path.join(ROOT))
        report["state_ok"] = True
        add(ig.staleness_check(s["wallet"]["valuation_date"], r["et"].date(), CAL))
        for res in ig.validate_accounting(s["wallet"], s["sim_positions"]):
            add(res)
        for res in ig.sizing_uniformity(s["sim_positions"]):
            add(res)
        slots = mc.slot_report(s["positions"])
        report["slots"] = slots
        report["regime_inputs_present"] = bool(s.get("benchmarks"))
    except Exception as e:                                    # noqa: BLE001
        report["state_ok"] = False
        report["escalations"].append("STATE_INTEGRITY_FAILURE")
        report["state_error"] = "%s: %s" % (type(e).__name__, e)

    # 4. 队列健康 / 死信
    if p:
        q = ob.queue_state(p)
        for res in ig.queue_health(q["pending"], q["failed"], now, q["oldest_pending_age_min"]):
            add(res)
        report["queue"] = {"pending": len(q["pending"]), "failed": len(q["failed"]),
                           "oldest_pending_age_min": q["oldest_pending_age_min"]}
        report["delivered_to_reconcile"] = ob.reconcile_delivered_to_alert_state(
            st.alert_state_keys(ROOT), p)

    # 4.5 W2 存活（WARN：不阻断——停摆恰恰是最需要跑起来的时刻）+ W5 git 管道（WARN）
    try:
        last = st.last_run_started(ROOT)
        res = ig.liveness_check(last, now, max_gap_min=800)  # 最大排期空档 SGT 08:30->20:00 ≈690min + 余量
        res.severity = "WARN"
        add(res)
    except Exception as e:                                    # noqa: BLE001
        report["liveness_error"] = "%s: %s" % (type(e).__name__, e)
    try:
        gdir = os.environ.get("US_STOCK_GIT") or (
            os.path.join(os.path.dirname(p), "us-stock-git") if p else None)
        if gdir and os.path.isdir(gdir):
            import hashlib as _h
            import time as _t
            b = os.path.join(gdir, "outgoing.bundle")
            exists = os.path.isfile(b)
            age = (_t.time() - os.path.getmtime(b)) / 60.0 if exists else None
            stamp_p = os.path.join(gdir, ".last-pushed-bundle")
            stamp_ok = False
            if exists and os.path.isfile(stamp_p):
                with open(b, "rb") as f:
                    digest = _h.sha256(f.read()).hexdigest()
                with open(stamp_p, encoding="utf-8") as f:
                    stamp_ok = f.read().strip() == digest
            errp = os.path.join(gdir, "pusher.err")
            errb = os.path.getsize(errp) if os.path.isfile(errp) else 0
            for res in ig.git_pipeline_check(exists, age, stamp_ok, errb):
                add(res)
    except Exception as e:                                    # noqa: BLE001
        report["git_watchdog_error"] = "%s: %s" % (type(e).__name__, e)

    # 5. 调度对齐（防止再次出现「阶段永不触发」）
    #    必须采样「接下来的交易日」；若只采样今天，周末运行会把每个阶段都判成不可达。
    days, d = [], r["et"].date()
    while len(days) < 5:
        if CAL.is_trading_day(d):
            days.append(d)
        d += __import__("datetime").timedelta(days=1)
    align = mc.verify_schedule_alignment(REQUIRED_CRON[0], REQUIRED_CRON[1], CAL, days, jitter_s=60)
    report["schedule_alignment_ok"] = align["ok"]
    if not align["ok"]:
        report["escalations"].append("SCHEDULE_MISALIGNED")
        report["schedule_detail"] = align

    report["ok"] = not report["escalations"]
    return report


def main():
    rep = run()
    if "--json" in sys.argv:
        print(json.dumps(rep, ensure_ascii=False, indent=2, default=str))
        return 0 if rep["ok"] else 1

    print("=" * 68)
    print("PREFLIGHT  %s" % rep["now_utc"])
    print("=" * 68)
    print("阶段判定 : %s   (%s)" % (rep["stage"], rep["route_reason"]))
    if rep.get("checkpoint"):
        print("检查点   : %s" % rep["checkpoint"])
    print("outbox   : %s" % ("OK " + rep.get("outbox", "") if rep.get("outbox_ok") else
                             "FAIL " + rep.get("outbox_error", "")))
    if "slots" in rep:
        s = rep["slots"]
        print("槽位     : 占用 %d/%d，可用 %d，可管理 %d，冻结 %d %s"
              % (s["occupied"], s["slot_limit"], s["available"], s["manageable"],
                 s["frozen"], s["frozen_symbols"]))
    if "queue" in rep:
        print("队列     : 待投 %d，死信 %d" % (rep["queue"]["pending"], rep["queue"]["failed"]))
    if rep.get("delivered_to_reconcile"):
        print("待回写   : %s" % ", ".join(rep["delivered_to_reconcile"]))
    print("调度对齐 : %s" % ("OK" if rep["schedule_alignment_ok"] else "MISALIGNED"))
    print("-" * 68)
    for c in rep["checks"]:
        if c.startswith("[PASS]"):
            continue
        print(" ", c)
    print("-" * 68)
    if rep["ok"]:
        print("结果：PASS — 可进入 %s 流程" % rep["stage"])
    else:
        print("结果：BLOCKED — 升级项：%s" % ", ".join(rep["escalations"]))
        print("按 SYSTEM.md §7：不得交易、不得发正常报告、不得在别处初始化。")
    print("=" * 68)
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
