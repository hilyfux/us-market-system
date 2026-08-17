#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preflight — 每次运行开头必须执行的守卫。退出码非 0 表示不得进入正常阶段流程。

它把「系统无法报告自己没在跑」这一根本缺陷补上：
    路由 + 陈旧度 + 存活 + 队列健康 + outbox 可用性 + 调度对齐 + 账务 + 学习闭环（判断质量）
任何一项 ERROR 级失败都会被命名并升级，而不是静默继续。

2026-08-15 起新增 W6/W7/W8（SYSTEM.md §4.2）：此前 36 项检查把账目校到分位，
却没有任何一项能因「判断在亏」而变红——账目被 36 路监视，判断力零监视。
W6（到期未裁定主张 = 硬 escalation UNADJUDICATED_CLAIMS）是闭环的牙齿：
它把「忘了复检」从沉默失败变成响亮失败。

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
import learning as lr         # noqa: E402
import outbox as ob           # noqa: E402
import state as st            # noqa: E402

CAL = mc.TradingCalendar(
    holidays={"2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
              "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25"},
    early_closes={"2026-11-27": mc.EARLY_CLOSE, "2026-12-24": mc.EARLY_CLOSE},
)
REQUIRED_CRON = ({0, 30, 40}, {0, 1, 2, 3, 4, 5, 8, 20, 21, 22, 23})


def lesson_ids_from_md(path):
    """从 lessons.md 提取教训 ID（条目头形如「**L-001 · 标题**」）。文件缺失返回空列表——
    W7 是覆盖检查，不得因知识库缺文件而使 preflight 崩溃。"""
    try:
        import re
        with open(path, encoding="utf-8") as f:
            return sorted(set(re.findall(r"\*\*(L-\d{3}) ·", f.read())))
    except OSError:
        return []


def lesson_registry(path):
    """读 lesson-status.json。缺失/损坏返回空 dict -> 全部教训判未声明（W7 WARN），不崩溃。"""
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return {}


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

    # 4.6 学习闭环 W6/W7/W8（SYSTEM.md §4.2，2026-08-15）——判断质量首次有了能变红的检查。
    #     例外安全：claims/shadow/lesson 文件缺失只表示「尚无主张/未登记」，不得使 preflight 崩溃
    #     （load_claims 对缺文件返回 []；lesson_* 辅助函数各自兜底）。
    try:
        et_date = r["et"].date()
        claims = lr.load_claims(ROOT)

        # W6 到期未裁定主张 —— 唯一的硬升级（闭环的牙齿）。
        # L-020 失效的原因正在于「追踪卖出后表现」只是备忘、没有到期强制；
        # 这里把它变成 ERROR：逾期未裁定 = 不得交易、不得发正常报告。
        # grace 口径 = 交易日：注入交易日历计数器（2026-08-15 审计 B1——
        # 暦日退化会把周五到期的主张在周日误判逾期并误阻断健全运行）。
        overdue = lr.overdue_claims(claims, et_date,
                                    sessions_between=CAL.trading_days_between)
        add(ig.CheckResult(
            "UNADJUDICATED_CLAIMS", not overdue, 0, len(overdue),
            "W6 到期未裁定主张：%s —— 每条到期主张必须机械裁定 HIT/MISS（作废须 VOID+理由），"
            "「忘了复检」是响亮失败" % (", ".join(c["claim_id"] for c in overdue) or "无"),
            severity="ERROR"))

        # ORPHAN_REPLACEMENT（2026-08-15）—— 替换成交与 claim 登记的即时耦合。
        # 现有 5 条 claim 全靠事后人工遡及补登；若下次替换漏登记，此前没有任何
        # 检查会变红（L-020 的根穴）。现在：账本成交表里同一 executed 日的
        # 平仓+建仓 = 替换对，每对必须有 claim RPL-<日>-<卖>-<买>，缺失即硬 ERROR。
        # 减仓/单腿成交显式不算替换（learning.replacement_pairs），不误伤。
        # 配对锚定在替换标记上（2026-08-15 审计 B3）：只有 CLOSED note 声明
        # 「确定性替换退出（trade …」的平仓才参与配对——素的平仓＋同日无关建仓
        # 不再被误配成替换对而向不存在的 claim 要求登记（误阻断弹已卸）。
        with open(os.path.join(ROOT, "portfolio-ledger.md"), encoding="utf-8") as f:
            _ledger_text = f.read()
        _trades = lr.parse_ledger_trades(_ledger_text)
        _markers = lr.parse_replacement_markers(_ledger_text)
        _orphans = lr.orphan_replacements(_trades, [c["claim_id"] for c in claims],
                                          replacement_close_ids=_markers)
        add(ig.CheckResult(
            "ORPHAN_REPLACEMENT", not _orphans, 0, len(_orphans),
            "替换成交必须当场登记可证伪主张（RPL-<日>-<卖>-<买>）：%s"
            % (", ".join(_orphans) or "无孤儿替换"),
            severity="ERROR"))

        # W7 教训执行状态覆盖 —— WARN。散文教训是已知缺口，须可见但不阻断运行
        # （阻断会诱使人为凑高覆盖率，违背「正直的覆盖」的目的）。
        ids = lesson_ids_from_md(os.path.join(ROOT, "knowledge", "lessons.md"))
        enf = lr.lesson_enforcement(
            lesson_registry(os.path.join(ROOT, "knowledge", "lesson-status.json")), ids)
        add(ig.CheckResult(
            "W7 教训执行状态覆盖", enf["ok"], 0, len(enf["undeclared"]),
            "共 %d 条：CODIFIED %d / PROSE_ONLY %d / 未声明或声明不完整 %s"
            "（每条须 CODIFIED+测试名 或 PROSE_ONLY+理由）"
            % (enf["total"], enf["codified"], enf["prose_only"], enf["undeclared"] or "无"),
            severity="WARN"))
        report["lesson_enforcement"] = {k: (str(v) if k == "coverage_pct" else v)
                                        for k, v in enf.items()}

        # W8 判断质量记分卡（replacement）—— WARN。样本不足 = 判定不能，**不是失败**
        # （把判定不能当失败，等于重犯 2026-08-15 在 4 个观测上下结论的错）。
        # 只有统计充分且命中率 <50%（多数替换劣于什么都不做）才变黄。
        sc = lr.scorecard(claims, lr.KIND_REPLACEMENT)
        w8_ok = (not sc["sufficient"]) or (sc["hit_rate_pct"] is not None
                                           and sc["hit_rate_pct"] >= 50)
        add(ig.CheckResult(
            "W8 判断质量记分卡(replacement)", w8_ok, None, None,
            "裁定 %d（HIT %d/MISS %d/VOID %d/OPEN %d）｜%s"
            % (sc["n_adjudicated"], sc["n_hit"], sc["n_miss"],
               sc["n_void"], sc["n_open"], sc["verdict"]),
            severity="WARN"))

        report["learning"] = lr.summary(ROOT, et_date,
                                        sessions_between=CAL.trading_days_between)
    except Exception as e:                                    # noqa: BLE001
        report["learning_error"] = "%s: %s" % (type(e).__name__, e)

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
    if "learning" in rep:
        ln = rep["learning"]
        print("学习闭环 : 主张 %d 条，今日到期 %d，逾期 %d；replacement：%s"
              % (ln["n_claims"], len(ln["due_today"]), len(ln["overdue"]),
                 ln["replacement"]["verdict"]))
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
