#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selftest — 把总纲变成可执行断言。任何规范改动都必须在此补用例。
用法：python3 tools/selftest.py      退出码 0 = 全通过
"""
import os
import shutil
import sys
import tempfile
from datetime import datetime, date, timedelta
from decimal import Decimal

HERE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE_DIR, "..", "lib"))
sys.path.insert(0, HERE_DIR)  # for importing sibling tools (refresh_data)

import market_core as mc          # noqa: E402
import integrity as ig            # noqa: E402
import outbox as ob               # noqa: E402
import report_lint as rl          # noqa: E402

PASS = FAIL = 0
FAILURES = []


def check(name, cond, detail=""):
    global PASS, FAIL
    if cond:
        PASS += 1
    else:
        FAIL += 1
        FAILURES.append("%s %s" % (name, detail))
    print("  [%s] %s%s" % ("PASS" if cond else "FAIL", name, ("  <- " + detail) if (detail and not cond) else ""))


CAL = mc.TradingCalendar(
    holidays={"2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
              "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25"},
    early_closes={"2026-11-27": mc.EARLY_CLOSE, "2026-12-24": mc.EARLY_CLOSE},
)


def et(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=mc.ET).astimezone(mc.UTC)


def sgt(s):
    return datetime.strptime(s, "%Y-%m-%d %H:%M").replace(tzinfo=mc.SGT).astimezone(mc.UTC)


def test_routing():
    print("\n== 阶段路由 ==")
    cases = [
        (et("2026-07-27 08:30"), "PREMARKET", "盘前起点"),
        (et("2026-07-27 09:29"), "PREMARKET", "盘前末点"),
        (et("2026-07-27 09:30"), "INTRADAY", "开盘"),
        (et("2026-07-27 12:30"), "INTRADAY", "半点检查点"),
        (et("2026-07-27 12:15"), mc.NO_STAGE, "非检查点不得运行"),
        (et("2026-07-27 15:30"), "INTRADAY", "收盘前最后检查点"),
        (et("2026-07-27 16:00"), mc.NO_STAGE, "刚收盘未到结算窗口"),
        (et("2026-07-27 16:30"), "POST_CLOSE", "收盘+30min"),
        (et("2026-07-27 17:15"), "POST_CLOSE", "收盘+75min 上界"),
        (et("2026-07-27 17:16"), mc.NO_STAGE, "超出结算窗口"),
        (et("2026-01-05 16:30"), "POST_CLOSE", "冬令时结算"),
        (et("2026-11-27 13:30"), "POST_CLOSE", "早收盘 13:00 -> 13:30 结算"),
        (et("2026-11-27 15:30"), mc.NO_STAGE, "早收盘后不得当盘中"),
        (et("2026-11-27 12:30"), "INTRADAY", "早收盘日收盘前仍是盘中"),
        (et("2026-07-25 10:00"), mc.NO_STAGE, "周六"),
        (et("2026-07-03 12:00"), mc.NO_STAGE, "独立日观察日"),
        (sgt("2026-07-27 08:30"), "MORNING", "晨间起点(SGT)"),
        (sgt("2026-07-27 08:59"), "MORNING", "晨间末点(SGT)"),
        (sgt("2026-07-27 08:29"), mc.NO_STAGE, "晨间窗口前"),
        (sgt("2026-07-27 09:00"), mc.NO_STAGE, "晨间窗口后"),
        (sgt("2026-07-25 08:30"), "MORNING", "周末仍出只读晨报"),
    ]
    for t, expect, note in cases:
        got = mc.route(t, CAL)["stage"]
        check("route %s -> %s (%s)" % (t.astimezone(mc.ET).strftime("%m-%d %H:%M ET"), expect, note),
              got == expect, "got %s" % got)

    try:
        mc.route(datetime(2026, 7, 27, 12, 0), CAL)
        check("naive datetime 必须被拒绝", False, "未抛异常")
    except ValueError:
        check("naive datetime 必须被拒绝", True)

    # 回归：真实调度延迟 87-137 秒。严格 minute in (0,30) 会让全部盘中运行失效。
    print("  -- 检查点吸附（真实调度延迟回归）--")
    latency_cases = [
        ("2026-07-27 09:31", "INTRADAY", "0930", "晚 1 分钟（实测常态）"),
        ("2026-07-27 10:02", "INTRADAY", "1000", "晚 2 分钟"),
        ("2026-07-27 10:09", "INTRADAY", "1000", "宽限内上界"),
        ("2026-07-27 10:41", mc.NO_STAGE, None, "超出宽限 -> 不得当检查点"),
        ("2026-07-27 10:30", "INTRADAY", "1030", "准点"),
    ]
    for ts, expect_stage, expect_cp, note in latency_cases:
        r = mc.route(et(ts), CAL)
        ok = r["stage"] == expect_stage and (expect_cp is None or r["checkpoint"] == expect_cp)
        check("延迟 %s -> %s/%s (%s)" % (ts[-5:], expect_stage, expect_cp, note), ok,
              "got %s/%s" % (r["stage"], r["checkpoint"]))

    # 同一宽限窗内两次运行必须吸附到同一检查点 -> report_key 相同 -> 天然幂等
    a = mc.route(et("2026-07-27 10:01"), CAL)["checkpoint"]
    b = mc.route(et("2026-07-27 10:07"), CAL)["checkpoint"]
    check("同宽限窗内重复运行吸附到同一检查点（幂等）", a == b == "1000", "%s vs %s" % (a, b))

    try:
        CAL.is_trading_day(date(2031, 1, 2))
        check("未覆盖年份必须抛异常", False, "未抛异常")
    except mc.CalendarCoverageError:
        check("未覆盖年份必须抛异常", True)


def test_schedule_alignment():
    print("\n== 调度对齐（本次事故的自动检出点）==")
    days = [date(2026, 7, 27) + timedelta(days=i) for i in range(5)]

    bad = mc.verify_schedule_alignment({0}, set(range(24)), CAL, days, jitter_s=47)
    check("旧 cron `0 * * * *` 必须被判定为不可用", not bad["ok"])
    check("旧 cron 必须报出 MORNING 不可达", "MORNING" in bad["unreachable"],
          "unreachable=%s" % bad["unreachable"])

    good = mc.verify_schedule_alignment({0, 30}, {0, 1, 2, 3, 4, 5, 8, 20, 21, 22, 23},
                                        CAL, days, jitter_s=60)
    check("新 cron 必须四阶段全可达且稳健", good["ok"],
          "unreachable=%s fragile=%s" % (good["unreachable"], good["fragile"]))
    check("新 cron POST_CLOSE jitter 余量 >= 5 分钟",
          good["post_close_margin_min"] is not None and good["post_close_margin_min"] >= 5,
          "margin=%s" % good["post_close_margin_min"])


def test_regime():
    print("\n== 市场环境分类器（确定性）==")
    r = mc.classify_regime(vix=18.58, spy=738.93, spy_ma50=745.07, spy_ma200=698.54,
                           breadth_adv_dec=1.54)
    check("2026-07-24 实况应判 DEFENSIVE", r["regime"] == "DEFENSIVE", str(r))
    check("DEFENSIVE 上限 50%", r["ceiling_pct"] == 50)
    check("SPY 跌破 200 日线 -> STRESS",
          mc.classify_regime(15, 690, 745, 698.54)["regime"] == "STRESS")
    check("VIX>=30 -> STRESS", mc.classify_regime(31, 800, 745, 698)["regime"] == "STRESS")
    check("全面健康 -> RISK_ON",
          mc.classify_regime(13, 800, 780, 700, 1.5)["regime"] == "RISK_ON")
    check("宽度转负 -> CHOPPY",
          mc.classify_regime(13, 800, 780, 700, 0.8)["regime"] == "CHOPPY")


def test_slots():
    print("\n== 槽位会计（消除 open_slots 歧义）==")
    positions = (
        [{"symbol": s, "status": "OPEN", "kind": "real", "quantity": "UNKNOWN"}
         for s in ("PWR", "MP", "BE", "KTOS", "RMBS")] +
        [{"symbol": s, "status": "OPEN", "kind": "sim", "quantity": "1"}
         for s in ("GEV", "ETN", "ABT")]
    )
    # 2026-07-27 新契约：模拟风险预算只对模拟持仓计数；真实持仓单列、不占模拟槽。
    r = mc.slot_report(positions, slot_limit=8)
    check("occupied == 3（仅模拟盘占槽）", r["occupied"] == 3, str(r))
    check("available == 5（模拟盘空槽，真实持仓不占）", r["available"] == 5, str(r))
    check("real_tracked == 5（真实持仓单列）", r["real_tracked"] == 5, str(r))
    check("frozen == 5（真实持仓数量未知，单列不挤占预算）", r["frozen"] == 5, str(r))
    check("at_capacity 为假（模拟盘未满）", r["at_capacity"] is False, str(r))

    # 真实持仓数量已知也不占用模拟槽；模拟盘空槽数只由模拟持仓决定。
    known_real = (
        [{"symbol": s, "status": "OPEN", "kind": "real", "quantity": "10"}
         for s in ("PWR", "MP", "BE", "KTOS", "RMBS")] +
        [{"symbol": s, "status": "OPEN", "kind": "sim", "quantity": "1"}
         for s in ("GEV", "ETN", "ABT")]
    )
    r2 = mc.slot_report(known_real, slot_limit=8)
    check("真实持仓（数量已知）不占模拟槽：occupied 仍 3、available 仍 5",
          r2["occupied"] == 3 and r2["available"] == 5 and r2["frozen"] == 0, str(r2))


def test_accounting():
    print("\n== 账务校验（必须真的能失败）==")
    positions = [
        {"symbol": "GEV", "quantity": "4.7957", "last_close": "1014.75",
         "cost_basis": "4999.996820", "market_value": "4866.436575", "unrealized_pnl": "-133.560245"},
        {"symbol": "ETN", "quantity": "12.0331", "last_close": "404.07",
         "cost_basis": "4999.993712", "market_value": "4862.214717", "unrealized_pnl": "-137.778995"},
        {"symbol": "ABT", "quantity": "50.5919", "last_close": "103.06",
         "cost_basis": "4999.997477", "market_value": "5214.001214", "unrealized_pnl": "214.003737"},
    ]
    wallet = {"cash": "85000.011991", "total_market_value": "14942.652506",
              "total_assets": "99942.664497", "cumulative_pnl": "-57.335503",
              "realized_pnl": "0", "unrealized_pnl": "-57.335503"}
    s = ig.summarize(ig.validate_accounting(wallet, positions))
    check("当前真实账目应全部通过", s["ok"], str(s["failures"]))

    # 关键：注入错误必须被抓到（旧恒等式抓不到任何一个）
    tampered = dict(wallet, total_market_value="15942.652506")
    s2 = ig.summarize(ig.validate_accounting(tampered, positions))
    check("篡改总市值必须被 C1 抓到", not s2["ok"])

    tampered2 = dict(wallet, cash="86000.011991")
    s3 = ig.summarize(ig.validate_accounting(tampered2, positions))
    check("篡改现金必须被 C2 抓到（幽灵交易场景）", not s3["ok"])

    ghost = positions + [{"symbol": "XXX", "quantity": "10", "last_close": "100",
                          "cost_basis": "1000", "market_value": "1000", "unrealized_pnl": "0"}]
    s4 = ig.summarize(ig.validate_accounting(wallet, ghost))
    check("凭空多出一个仓位必须被抓到", not s4["ok"])

    # 已实现盈亏（部分止盈卖出）后账目仍须自洽：现金 = 初始 − Σ成本基础 + 已实现。
    # 场景：买 100@10（成本基础 1000），卖 40@15（收益 200），余 60@10、现价 12。
    # cash = 100000 − 1000 + 40×15 = 99600；余仓成本基础 600、市值 720、未实现 120。
    rz_positions = [{"symbol": "XYZ", "quantity": "60", "last_close": "12",
                     "cost_basis": "600", "market_value": "720", "unrealized_pnl": "120"}]
    rz_wallet = {"cash": "99600", "total_market_value": "720", "total_assets": "100320",
                 "cumulative_pnl": "320", "realized_pnl": "200", "unrealized_pnl": "120"}
    sr = ig.summarize(ig.validate_accounting(rz_wallet, rz_positions))
    check("含已实现盈亏的账目应全部通过（realized-aware C2/C6）", sr["ok"], str(sr["failures"]))

    # 漏记已实现盈亏（realized 归零但现金仍含收益）必须被 C2+C6 抓到
    rz_bad = dict(rz_wallet, realized_pnl="0")
    srb = ig.summarize(ig.validate_accounting(rz_bad, rz_positions))
    check("漏记已实现盈亏必须被抓到（realized 与现金/累计不符）", not srb["ok"])

    # realized=0 时新式与旧式等价：原始账目（realized=0）依然通过，保证向后兼容
    check("realized=0 时账目仍通过（向后兼容）", s["ok"])


def test_staleness():
    print("\n== 陈旧度看门狗 ==")
    r = ig.staleness_check("2026-07-16", date(2026, 7, 25), CAL)
    check("7/16 估值 vs 7/25 必须判为 STALE（本次事故）", not r.passed, repr(r))
    check("落后交易日数应为 6", r.actual == 6, "got %s" % r.actual)
    r2 = ig.staleness_check("2026-07-24", date(2026, 7, 25), CAL)
    check("7/24 估值 vs 7/25（周六）应通过", r2.passed, repr(r2))


def test_provenance():
    print("\n== 行情溯源 ==")
    good = ig.PriceRecord("GEV", "2026-07-24", "1014.75", [
        {"domain": "stockanalysis.com", "figure": "1014.75",
         "url": "https://stockanalysis.com/stocks/gev/?v=2", "method": "web_fetch"},
        {"domain": "roic.ai", "figure": "1014.75", "url": "https://roic.ai/quote/GEV", "method": "web_fetch"},
    ])
    check("三源零偏差记录应通过", ig.summarize(good.validate())["ok"])

    single = ig.PriceRecord("XX", "2026-07-24", "10", [
        {"domain": "stockanalysis.com", "figure": "10", "url": "https://x/?v=2", "method": "f"}])
    check("单一来源必须失败（P1）", not ig.summarize(single.validate())["ok"])

    banned = ig.PriceRecord("XX", "2026-07-24", "10", [
        {"domain": "stockanalysis.com", "figure": "10", "url": "https://x/?v=2", "method": "f"},
        {"domain": "finance.yahoo.com", "figure": "10", "url": "https://y", "method": "f"}])
    check("使用黑名单来源必须失败（P2）", not ig.summarize(banned.validate())["ok"])

    conflict = ig.PriceRecord("XX", "2026-07-24", "10", [
        {"domain": "stockanalysis.com", "figure": "10.00", "url": "https://x/?v=2", "method": "f"},
        {"domain": "roic.ai", "figure": "10.50", "url": "https://y", "method": "f"}])
    check("跨源偏差 5% 必须失败（P3）", not ig.summarize(conflict.validate())["ok"])


def test_outbox():
    print("\n== outbox 契约 ==")
    tmp = tempfile.mkdtemp(prefix="obtest-")
    try:
        ob.assert_path_usable(tmp, create_anchor=True)
        hook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=x"

        # 以下机制用例（去重/抑制）用 toy 文案，关掉 lint 专测机制。
        r = ob.enqueue("PREMARKET+2026-07-27", "# 报告\n持有全部", hook, path=tmp, lint=False)
        check("首次入队成功", r["enqueued"], str(r))

        r2 = ob.enqueue("PREMARKET+2026-07-27", "# 报告\n持有全部（不同措辞）", hook, path=tmp, lint=False)
        check("同键重复入队必须被拒", not r2["enqueued"] and "DUPLICATE" in r2["reason"], str(r2))

        rev = ob.next_revision("PREMARKET+2026-07-27", path=tmp)
        check("可生成修订键 #r1", rev.endswith("#r1"), rev)
        r3 = ob.enqueue(rev, "# 更正版报告\n内容已修正", hook, path=tmp, lint=False)
        check("修订键可入队（可重发更正版）", r3["enqueued"], str(r3))

        # 抑制：相同内容且无风险标记
        ob.enqueue("INTRADAY+2026-07-27+1000", "# 盘中\n全部持有，数据降级", hook, path=tmp, lint=False)
        r4 = ob.enqueue("INTRADAY+2026-07-27+1030", "# 盘中\n全部持有，数据降级", hook, path=tmp, lint=False)
        check("内容无变化应被抑制（治理告警疲劳）",
              not r4["enqueued"] and "SUPPRESSED" in r4["reason"], str(r4))
        r5 = ob.enqueue("INTRADAY+2026-07-27+1100", "# 盘中\n全部持有，数据降级",
                        hook, path=tmp, has_risk_flag=True, lint=False)
        check("带风险标记必须绕过抑制（安全信息不可被吞）", r5["enqueued"], str(r5))

        try:
            ob.enqueue("X", "y", "https://evil.example.com/hook", path=tmp, lint=False)
            check("非企业微信 host 必须被拒", False, "未抛异常")
        except ValueError:
            check("非企业微信 host 必须被拒", True)

        try:
            ob.assert_path_usable("/Users/linqing.wang/Desktop/Claude/us-stock-outbox")
            check("TCC 保护路径必须被拒（本次事故根因）", False, "未抛异常")
        except ob.TccProtectedPath:
            check("TCC 保护路径必须被拒（本次事故根因）", True)

        news = ob.reconcile_delivered_to_alert_state([], path=tmp)
        check("SIMTEST/SELFTEST 不得进 alert-state",
              all(not k.startswith(("SIMTEST-", "SELFTEST-", "PIPELINE-")) for k in news))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # -- 路径可用性探针语义（2026-07-27 修复：ENQUEUE_PATH_UNAVAILABLE 误报回归）--
    print("  -- assert_path_usable 探针语义 --")

    # 回归本次事故：某些沙箱 FUSE 挂载允许 open/write/rename 却拒绝 unlink(EPERM)。
    # enqueue() 从不 unlink，故 unlink 被拒时 outbox 必须仍判为可用，绝不误报。
    tmp_u = tempfile.mkdtemp(prefix="ob-unlink-")
    ob.assert_path_usable(tmp_u, create_anchor=True)
    orig_remove = os.remove
    try:
        def _deny_unlink(*a, **k):
            raise PermissionError(1, "Operation not permitted")
        os.remove = _deny_unlink
        try:
            ob.assert_path_usable(tmp_u)
            r = ob.enqueue("MORNING+2026-07-24", "# 晨报\n全部持有",
                           "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=x",
                           path=tmp_u, lint=False)
            check("unlink 被拒(EPERM)但 write/rename 正常 -> outbox 仍可用且能入队（本次修复回归）",
                  r["enqueued"], str(r))
        except (ob.EnqueuePathUnavailable, ob.TccProtectedPath) as e:
            check("unlink 被拒(EPERM)但 write/rename 正常 -> outbox 仍可用且能入队（本次修复回归）",
                  False, "误报为不可用: %s" % e)
        finally:
            os.remove = orig_remove
    finally:
        shutil.rmtree(tmp_u, ignore_errors=True)

    # 检出力保留 1：rename（原子入队）不可用必须致命。
    tmp_r = tempfile.mkdtemp(prefix="ob-rename-")
    ob.assert_path_usable(tmp_r, create_anchor=True)
    orig_rename = os.rename
    try:
        def _deny_rename(*a, **k):
            raise PermissionError(1, "Operation not permitted")
        os.rename = _deny_rename
        try:
            ob.assert_path_usable(tmp_r)
            check("rename 不可用必须致命(EnqueuePathUnavailable) — 保留检出力", False, "未抛异常")
        except ob.EnqueuePathUnavailable:
            check("rename 不可用必须致命(EnqueuePathUnavailable) — 保留检出力", True)
        finally:
            os.rename = orig_rename
    finally:
        shutil.rmtree(tmp_r, ignore_errors=True)

    # 检出力保留 2：路径根本无法建目录（父级是普通文件）必须致命。
    tmp_nd = tempfile.mkdtemp(prefix="ob-notdir-")
    try:
        blocker = os.path.join(tmp_nd, "afile")
        with open(blocker, "w") as f:
            f.write("x")
        try:
            ob.assert_path_usable(os.path.join(blocker, "outbox"))
            check("无法建目录的路径必须致命(EnqueuePathUnavailable)", False, "未抛异常")
        except ob.EnqueuePathUnavailable:
            check("无法建目录的路径必须致命(EnqueuePathUnavailable)", True)
    finally:
        shutil.rmtree(tmp_nd, ignore_errors=True)

    # 探针终名必须是点文件且非 .json：否则会被 queue_state()/转发器误当成待投消息。
    tmp_p = tempfile.mkdtemp(prefix="ob-probe-")
    ob.assert_path_usable(tmp_p, create_anchor=True)
    try:
        orig_rm = os.remove
        os.remove = lambda *a, **k: (_ for _ in ()).throw(PermissionError(1, "nope"))
        try:
            ob.assert_path_usable(tmp_p)   # unlink 被拒 -> 探针残留，模拟真实挂载
        finally:
            os.remove = orig_rm
        leftover_json = [n for n in os.listdir(tmp_p) if n.endswith(".json")]
        check("探针残留不得被 queue_state 当成待投消息（无 .json 残留）",
              leftover_json == [] and ob.queue_state(tmp_p)["pending"] == [],
              "leftover=%s" % leftover_json)
    finally:
        shutil.rmtree(tmp_p, ignore_errors=True)

    # 死信计数口径：failed/ 里只有 .json 文件算死信；点文件/归档子目录不得误报（2026-07-27）。
    tmp_f = tempfile.mkdtemp(prefix="ob-failcount-")
    try:
        fdir = os.path.join(tmp_f, "failed")
        os.makedirs(os.path.join(fdir, "archive"), exist_ok=True)
        with open(os.path.join(fdir, ".wp"), "w") as f:          # 探针残留点文件
            f.write("ok")
        with open(os.path.join(fdir, "archive", "old.json"), "w") as f:  # 已归档
            f.write("{}")
        q0 = ob.queue_state(tmp_f)
        check("failed/ 仅有点文件+归档子目录时死信数为 0（不误报 W3）",
              len(q0["failed"]) == 0, "failed=%s" % q0["failed"])
        with open(os.path.join(fdir, "20260101-000000_REAL.json"), "w") as f:  # 真死信
            f.write("{}")
        q1 = ob.queue_state(tmp_f)
        check("failed/ 出现真实 .json 死信必须被计入（保留检出力）",
              len(q1["failed"]) == 1, "failed=%s" % q1["failed"])
    finally:
        shutil.rmtree(tmp_f, ignore_errors=True)


def test_report_lint():
    print("\n== 推送可读性/无歧义硬门（§5 机器可验证子集）==")

    # 一份合规的盘中报告（标题+日期、动作合规、建议未执行、数据时间来源、篇幅内）
    good = (
        "# 美股盘中报告｜2026-07-27\n"
        "ABT · 持有 · 未触发止盈条件\n"
        "MP · 减仓建议未执行 · 相对大盘走弱，需收盘确认\n"
    )
    check("合规盘中报告应通过", rl.lint_report(good, "INTRADAY")["ok"],
          str(rl.lint_report(good, "INTRADAY")["violations"]))

    # L1：标题缺失
    bad_title = rl.lint_report("市场平稳\nABT 持有", "INTRADAY")
    check("无标题行必须判违规（L1）", not bad_title["ok"])

    # L1：标题缺日期
    bad_date = rl.lint_report("# 美股盘中报告\nABT 持有", "INTRADAY")
    check("标题缺日期必须判违规（L1）", not bad_date["ok"])

    # L3：模糊动词
    vague = rl.lint_report("# 盘中｜2026-07-27\nMP 观察", "INTRADAY")
    check("模糊动词「观察」必须判违规（L3）", not vague["ok"])

    # L4：盘中交易动作未标注“建议未执行”
    unlabeled = rl.lint_report("# 盘中｜2026-07-27\nMP 减仓 20%", "INTRADAY")
    check("盘中减仓未标注「建议未执行」必须判违规（L4）", not unlabeled["ok"])

    # L4：否定语境不误判（“无减仓/平仓信号”）
    negated = rl.lint_report(
        "# 盘中｜2026-07-27\n全部持有，无减仓/平仓信号", "INTRADAY")
    check("「无减仓/平仓信号」不得误判（L4 否定守卫）", negated["ok"],
          str(negated["violations"]))

    # L4（2026-07-27 修复）：条件/检查语境里的前瞻动作词不得误判。
    conditional = rl.lint_report(
        "# 美股盘前｜2026-07-27\nMP · 持有（建议未执行）· 财报前不动\n"
        "开盘后检查：若 BE 盘后财报破坏基本面，待正式收盘技术确认后再议减仓", "PREMARKET")
    check("条件/检查语境「若…待确认…再议减仓」不得误判（L4 条件守卫）",
          conditional["ok"], str(conditional["violations"]))

    # L4 检出力保留：真实的、当下的未标注交易动作行仍须判违规。
    real_unlabeled = rl.lint_report(
        "# 美股盘前｜2026-07-27\nMP 减仓20%", "PREMARKET")
    check("当下未标注「建议未执行」的真实交易动作仍须判违规（L4 保留检出力）",
          not real_unlabeled["ok"], str(real_unlabeled["violations"]))

    # L5 已撤销（2026-07-27 用户裁定）：无来源标注也合格
    nosrc = rl.lint_report("# 盘中｜2026-07-27\nABT · 持有 · 未触发止盈", "INTRADAY")
    check("无来源/as-of 标注也合格（L5 撤销）", nosrc["ok"], str(nosrc["violations"]))

    # L6：内部事务不得泄漏进推送
    leak1 = rl.lint_report("# 盘中｜2026-07-27\nABT 持有（来源 stockanalysis.com）", "INTRADAY")
    check("来源域名进正文必须判违规（L6）", not leak1["ok"])
    leak2 = rl.lint_report("# 盘中｜2026-07-27\nMP 持有，数据降级", "INTRADAY")
    check("「数据降级」进正文必须判违规（L6）", not leak2["ok"])
    leak3 = rl.lint_report("# 盘中｜2026-07-27\n持有；MARKET_DATA_DEGRADED", "INTRADAY")
    check("升级项代码进正文必须判违规（L6）", not leak3["ok"])

    # L2：篇幅超限（晨间 700 上限）
    toolong = rl.lint_report("# 晨报｜2026-07-27\n" + "字" * 720, "MORNING")
    check("晨间超 700 字必须判违规（L2）", not toolong["ok"])

    # stage 解析
    check("report_key 解析阶段：INTRADAY",
          rl.stage_from_report_key("INTRADAY+2026-07-27+1000") == "INTRADAY")
    check("非阶段键（SIMTEST）返回 None（跳过 lint）",
          rl.stage_from_report_key("SIMTEST-2026-07-27") is None)

    # enqueue 硬门：不合格报告必须抛 ReportLintError，绝不静默入队
    tmp = tempfile.mkdtemp(prefix="lint-eq-")
    ob.assert_path_usable(tmp, create_anchor=True)
    try:
        hook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=x"
        try:
            ob.enqueue("PREMARKET+2026-07-27", "# 报告\n持有全部", hook, path=tmp)
            check("不合格阶段报告必须被 enqueue 拒绝（抛 ReportLintError）", False, "未抛异常")
        except rl.ReportLintError:
            check("不合格阶段报告必须被 enqueue 拒绝（抛 ReportLintError）", True)
        # 合规报告应能正常入队
        rgood = ob.enqueue("PREMARKET+2026-07-27",
                           "# 美股盘前｜2026-07-27\n全部持有（建议未执行）",
                           hook, path=tmp)
        check("合规阶段报告应正常入队", rgood["enqueued"], str(rgood))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_quote_extract():
    print("\n== 行情页去噪抽取（2026-07-27 新增，治理抓取噪声）==")
    import quote_extract as qe
    sample = (
        "# State Street SPDR S&P 500 ETF (SPY)\n"
        "NYSEARCA: SPY · Real-Time Price · USD\n"
        "738.93\n"
        "+0.75 (0.10%)\n"
        "At close: Jul 24, 2026, 4:00 PM EDT\n"
        "738.66\n"
        "-0.27 (-0.04%)\n"
        " After-hours: Jul 24, 2026, 8:00 PM EDT\n"
        "| Previous Close | 738.18          |\n"
        "| Open           | 738.51          |\n"
        "| Day's Range    | 737.29 - 743.72 |\n"
        "...(大量无关新闻流)...\n"
    )
    q = qe.extract_quote(sample)
    check("抽取正式收盘价 738.93", q["price"] == "738.93", str(q))
    check("抽取涨跌幅 0.10%", q["change_pct"] == "0.10", str(q))
    check("抽取 as-of 含 Jul 24, 2026", q["as_of"] and "Jul 24, 2026" in q["as_of"], str(q))
    check("抽取盘后价 738.66", q["after_hours_price"] == "738.66", str(q))
    check("抽取前收盘 738.18", q["previous_close"] == "738.18", str(q))
    check("抽取开盘 738.51", q["open"] == "738.51", str(q))
    empty = qe.extract_quote("完全没有价格的噪声文本")
    check("无价格文本各字段为 None（宁缺勿造）",
          empty["price"] is None and empty["previous_close"] is None, str(empty))


def test_knowledge():
    print("\n== 知识库闭环（§12，2026-07-27 新增）==")
    import knowledge as kn
    tmp = tempfile.mkdtemp(prefix="kn-")
    try:
        k = kn.ensure_structure(tmp)
        check("ensure_structure 建齐目录且幂等",
              all(os.path.isdir(os.path.join(k, d)) for d in ("tickers", "regime", "reviews"))
              and kn.ensure_structure(tmp) == k)
        check("读不存在的标的页返回 None（不臆造）", kn.read_ticker(tmp, "XYZ") is None)

        p = kn.append_ticker_note(tmp, "XYZ", "2026-07-27", "建仓测试记录")
        check("append_ticker_note 自动建页并追加", "建仓测试记录" in open(p, encoding="utf-8").read())
        kn.append_ticker_note(tmp, "XYZ", "2026-07-27", "建仓测试记录")
        check("完全相同记录不重复追加（幂等）",
              open(p, encoding="utf-8").read().count("建仓测试记录") == 1)

        rp = kn.append_review(tmp, "2026-07-27", "## 决策\n持有")
        check("append_review 建当日复盘", kn.review_exists(tmp, "2026-07-27"))
        kn.append_review(tmp, "2026-07-27", "## 补充\n盘后验证")
        t = open(rp, encoding="utf-8").read()
        check("复盘追加不覆盖（增量原则）", "持有" in t and "盘后验证" in t and t.count("# 每日复盘") == 1)

        try:
            kn.append_ticker_note(tmp, "bad symbol", "2026-07-27", "x")
            check("非法代码必须被拒", False, "未抛异常")
        except ValueError:
            check("非法代码必须被拒", True)
        try:
            kn.append_review(tmp, "07/27", "x")
            check("非法日期必须被拒", False, "未抛异常")
        except ValueError:
            check("非法日期必须被拒", True)

        s = kn.summary(tmp)
        check("summary 计数正确", s["tickers"] == 1 and s["reviews"] == 1
              and s["latest_review"] == "2026-07-27", str(s))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_high_availability():
    print("\n== 高可用（2026-07-27 体检修复）==")

    # A. 锚定哨兵：堵「沙箱 home 假 outbox 静默吞消息」陷阱（实测确认过会发生）
    tmp = tempfile.mkdtemp(prefix="anchor-")
    try:
        try:
            ob.assert_path_usable(tmp)
            check("既存目录但无锚定文件必须被拒（陷阱回归）", False, "未抛异常")
        except ob.EnqueuePathUnavailable:
            check("既存目录但无锚定文件必须被拒（陷阱回归）", True)
        missing = os.path.join(tmp, "no-such-dir")
        try:
            ob.assert_path_usable(missing)
            check("不存在的目录必须被拒（不再自动创建生产 outbox）", False, "未抛异常")
        except ob.EnqueuePathUnavailable:
            check("不存在的目录必须被拒（不再自动创建生产 outbox）", True)
        check("目录未被静默创建", not os.path.isdir(missing))
        p = ob.assert_path_usable(tmp, create_anchor=True)
        check("create_anchor 显式初始化后通过", p == tmp
              and open(os.path.join(tmp, ob.ANCHOR_NAME)).read() == ob.ANCHOR_CONTENT)
        with open(os.path.join(tmp, ob.ANCHOR_NAME), "w") as f:
            f.write("wrong content")
        try:
            ob.assert_path_usable(tmp)
            check("锚定内容不符必须被拒", False, "未抛异常")
        except ob.EnqueuePathUnavailable:
            check("锚定内容不符必须被拒", True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # B. W5 git 管道看门狗（WARN 级，绝不阻断交易）
    r = ig.git_pipeline_check(bundle_exists=False, bundle_age_min=None,
                              stamp_matches=False, err_bytes=0)
    check("无 bundle -> W5 通过", all(x.passed for x in r), str([repr(x) for x in r]))
    r = ig.git_pipeline_check(True, 45.0, False, 0)
    stale = [x for x in r if not x.passed]
    check("bundle 待处理 45min 未盖章 -> GIT_PIPELINE_STALE",
          len(stale) == 1 and stale[0].severity == "WARN", str([repr(x) for x in r]))
    r = ig.git_pipeline_check(True, 45.0, True, 0)
    check("已盖章的旧 bundle -> 通过（已处理）", all(x.passed for x in r))
    r = ig.git_pipeline_check(False, None, False, 120)
    err = [x for x in r if not x.passed]
    check("pusher.err 非空 -> WARN 检出", len(err) == 1 and err[0].severity == "WARN")

    # C. W2 存活：时区无冒号归一化 + 阈值语义（800min 覆盖最大排期空档）
    import state as st
    tmp2 = tempfile.mkdtemp(prefix="live-")
    try:
        for n in st.FILES:
            with open(os.path.join(tmp2, n), "w") as f:
                f.write("placeholder\n")
        with open(os.path.join(tmp2, "system-state.md"), "w") as f:
            f.write("## Run summary\n\nactual_start: 2026-07-27T08:02:37+0800\n")
        s = st.last_run_started(tmp2)
        check("`+0800` 归一化为可解析 ISO", s == "2026-07-27T08:02:37+08:00", repr(s))
        parsed = datetime.fromisoformat(s)
        now_ok = parsed + timedelta(minutes=100)
        now_bad = parsed + timedelta(minutes=900)
        check("100min 间隔 -> W2 通过", ig.liveness_check(s, now_ok, 800).passed)
        check("900min 间隔 -> W2 检出停摆", not ig.liveness_check(s, now_bad, 800).passed)
        check("无记录 -> W2 检出（无法证明存活）", not ig.liveness_check(None, now_ok, 800).passed)
    finally:
        shutil.rmtree(tmp2, ignore_errors=True)


def test_data_layer():
    print("\n== 数据分层管理（§13，2026-07-27 新增）==")

    # 1) 信息源注册表：可用性属性——交易门槛指标必须 ≥2 核准源，否则 P1 永不可能通过
    for m in ig.TRADE_GATING_METRICS:
        n = len(ig.approved_for(m))
        check("交易门槛指标 %s 有 ≥2 核准源（P1 可满足性）" % m, n >= 2, "只有 %d 个" % n)
    # 2) 核准与黑名单不得重叠
    for m, srcs in ig.APPROVED_SOURCES.items():
        overlap = set(srcs) & set(ig.BAD_SOURCES)
        check("指标 %s 核准源与黑名单无交集" % m, not overlap, str(overlap))
    # 3) quirk 标志与既有常量一致（cache-buster / stamp-check）
    eq = ig.APPROVED_SOURCES["equity_close"]
    check("stockanalysis 标记 cache_buster（与 CACHE_BUSTER_REQUIRED 一致）",
          eq["stockanalysis.com"].get("cache_buster") is True
          and "stockanalysis.com" in ig.CACHE_BUSTER_REQUIRED)
    check("stocktitan 标记 stamp_check（与 STAMP_CHECK_REQUIRED 一致）",
          eq["stocktitan.net"].get("stamp_check") is True
          and "stocktitan.net" in ig.STAMP_CHECK_REQUIRED)
    # 4) 文档同步：sources.md 必须包含每个核准域名与每个黑名单域名
    doc_p = os.path.join(os.path.dirname(HERE_DIR), "data", "sources.md")
    if os.path.exists(doc_p):
        doc = open(doc_p, encoding="utf-8").read()
        missing = [d for srcs in ig.APPROVED_SOURCES.values() for d in srcs if d not in doc]
        missing += [d for d in ig.BAD_SOURCES if d not in doc]
        check("data/sources.md 与代码注册表同步（域名全覆盖）", not missing, str(missing))
    else:
        check("data/sources.md 存在", False, doc_p)

    # 5) 持仓归一化视图：纯函数正确性（单一账户口径，2026-07-31）
    import refresh_data as rd
    fixture = [
        {"symbol": "RMBS", "kind": "sim", "status": "OPEN", "quantity": "87.926808",
         "cost_basis": "10000.000000", "last_close": "89.62", "close_date": "2026-07-30",
         "market_value": "7880.000533", "unrealized_pnl": "-2119.999467"},
        {"symbol": "ABT", "kind": "sim", "status": "OPEN", "quantity": "96.311964",
         "cost_basis": "10000.000000", "last_close": "105.61", "close_date": "2026-07-30",
         "market_value": "10171.506518", "unrealized_pnl": "171.506518"},
    ]
    md, tot = rd.build_positions_table(fixture, {})
    check("视图含统一表头与全部行",
          md.count("\n|---") == 1 and "RMBS" in md and "ABT" in md, md[:120])
    check("组合市值合计（18051.51）", str(tot["mv"]) == "18051.51", str(tot))
    check("组合未实现合计（-1948.49）", str(tot["upnl"]) == "-1948.49", str(tot))
    check("avg_cost = cost_basis/qty（RMBS 113.73）", "113.73" in md, md[:250])
    # 6) 单一账户纯度守卫（2026-07-31，防 real/sim 区分在生成视图/账本回潮）
    for tok in ("real", "真实", "建议未执行", "kind"):
        check("视图纯度：不含 %r" % tok, tok not in md)
    ledger_p = os.path.join(HERE_DIR, "..", "portfolio-ledger.md")
    with open(ledger_p, encoding="utf-8") as f:
        ledger_txt = f.read()
    check("账本无「OPEN real positions」段", "## OPEN real positions" not in ledger_txt)
    check("账本为单一「OPEN positions」段", "## OPEN positions" in ledger_txt)
    pos_view_p = os.path.join(HERE_DIR, "..", "data", "positions.md")
    if os.path.exists(pos_view_p):
        with open(pos_view_p, encoding="utf-8") as f:
            pv = f.read()
        for tok in ("真实盘", "模拟盘小计", "建议未执行", "| kind |"):
            check("positions.md 纯度：不含 %r" % tok, tok not in pv)
    # 7) C7 仓位标准统一性（防「一部 $5k 一部 $10k」复发；个人判断不得静默覆盖用户口径）
    ok_pos = [{"symbol": "A", "cost_basis": "10000.000000", "thesis": "x"}]
    bad_pos = [{"symbol": "B", "cost_basis": "5000.00", "thesis": "y"}]
    ex_pos = [{"symbol": "C", "cost_basis": "2500.00", "thesis": "止盈后半仓 SIZE_EXCEPTION(take-profit)"}]
    check("C7 标准 $10k 通过", all(r.passed for r in ig.sizing_uniformity(ok_pos)))
    check("C7 偏离 $5k 必须失败", not all(r.passed for r in ig.sizing_uniformity(bad_pos)))
    check("C7 显式 SIZE_EXCEPTION 豁免通过", all(r.passed for r in ig.sizing_uniformity(ex_pos)))
    # 8) 账本统一段头解析（state.load_positions 认「## OPEN positions」）
    import tempfile as _tf
    import state as _st
    with _tf.TemporaryDirectory() as td:
        with open(os.path.join(td, "portfolio-ledger.md"), "w", encoding="utf-8") as f:
            f.write("# L\n\n## OPEN positions\n\n"
                    "| symbol | status | opened_on | cost | quantity | cost_basis | last_close "
                    "| close_date | market_value | unrealized_pnl | data_status | thesis |\n"
                    "|---|---|---|---|---|---|---|---|---|---|---|---|\n"
                    "| ZZZ | OPEN | 2026-01-01 | 10 | 1000 | 10000 | 11 | 2026-01-02 "
                    "| 11000 | 1000 | VERIFIED | t |\n")
        parsed = _st.load_positions(td)
        check("统一段头解析出 1 仓且 kind=sim",
              len(parsed) == 1 and parsed[0]["kind"] == "sim" and parsed[0]["symbol"] == "ZZZ",
              str(parsed))
        check("统一段头解析带 thesis 列", parsed[0].get("thesis") == "t", str(parsed))


def test_selection():
    print("\n[selection] 选股/建仓纪律门 ACT-005/006/007（L-008/L-009/L-010/L-012 codified）")
    import selection as sel
    from decimal import Decimal as D
    # ACT-005 事件封锁（L-010）
    check("ACT-005 距财报3日 -> 封锁新建", sel.event_timing_gate(3)[0] is False)
    check("ACT-005 边界=5日 -> 仍封锁", sel.event_timing_gate(5)[0] is False)
    check("ACT-005 6日 -> 放行", sel.event_timing_gate(6)[0] is True)
    check("ACT-005 无近端催化 -> 放行", sel.event_timing_gate(None)[0] is True)
    check("ACT-005 财报已过 -> 放行（事件后）", sel.event_timing_gate(-1)[0] is True)
    # ACT-006 主题上限（L-009/L-012）
    check("ACT-006 加仓后13.67%≤25 -> 放行",
          sel.theme_cap_gate("ai_power", D("5000"), D("100000"), D("8672"))[0] is True)
    check("ACT-006 加仓后28.67%>25 -> 拒绝",
          sel.theme_cap_gate("ai_power", D("20000"), D("100000"), D("8672"))[0] is False)
    check("ACT-006 恰好25% -> 放行（边界）",
          sel.theme_cap_gate("x", D("25000"), D("100000"), D("0"))[0] is True)
    check("ACT-006 未登记论题 -> 保守拒绝",
          sel.theme_cap_gate(None, D("1000"), D("100000"), D("0"))[0] is False)
    # ACT-004 基础仓位 = NAV 10%（=$10,000 @ $100k，比例制，用户 2026-07-31）
    check("ACT-004 基础初始仓 == 10% NAV", sel.BASE_INITIAL_PCT == D("10"))
    # ACT-007 波动折仓（L-008）：base 10% -> 高 beta 5%
    check("ACT-007 高 beta 名义仓折半（10%->5%）",
          sel.volatility_scaled_size(sel.BASE_INITIAL_PCT, True) == D("5"))
    check("ACT-007 常规仓位不变（10%）",
          sel.volatility_scaled_size(sel.BASE_INITIAL_PCT, False) == D("10"))
    # 组合门：BE 式（财报前 + 高 beta + 同主题重仓）必须被拒；ABT 式（事件后、低集中）放行
    rb = sel.screen_new_position("BE", sel.BASE_INITIAL_PCT, D("100000"), D("20000"), 2, True)
    check("screen BE 式（财报前高beta同主题）-> 拒绝", rb["allowed"] is False)
    check("screen 高 beta 仓位已折半 5%（$5k @ $100k）", rb["sized_pct"] == D("5"))
    ra = sel.screen_new_position("ABT", sel.BASE_INITIAL_PCT, D("100000"), D("0"), None, False)
    check("screen ABT 式（事件后低集中，10% $10k）-> 放行", ra["allowed"] is True)
    check("screen 常规仓位 == 10%（$10,000 @ $100k）", ra["sized_pct"] == D("10"))


def test_backtest():
    print("\n[backtest] 回测/绩效引擎（合成数据锁定，样本充分性守卫）")
    import backtest as bt
    from decimal import Decimal as D
    # 收益 & 回撤
    check("total_return [100,120]==20.00", bt.total_return([100, 120]) == D("20.00"))
    check("total_return 单点==0", bt.total_return([100]) == D("0"))
    check("max_drawdown [100,110,105,120]==4.55",
          bt.max_drawdown([100, 110, 105, 120]) == D("4.55"),
          str(bt.max_drawdown([100, 110, 105, 120])))
    check("max_drawdown [100,90,95]==10.00", bt.max_drawdown([100, 90, 95]) == D("10.00"))
    # 成交统计
    ts = bt.trade_stats([{"realized": "171.51"}, {"realized": "-50"}, {"realized": "100"}])
    check("trade n==3", ts["n"] == 3, str(ts))
    check("win_rate==66.67", ts["win_rate"] == D("66.67"), str(ts))
    check("profit_factor==5.43", ts["profit_factor"] == D("5.43"), str(ts))
    check("net_realized==221.51", ts["net_realized"] == D("221.51"), str(ts))
    check("expectancy==73.84", ts["expectancy"] == D("73.84"), str(ts))
    check("无亏损时 profit_factor 为 Infinity",
          bt.trade_stats([{"realized": "10"}])["profit_factor"] == D("Infinity"))
    check("空成交 win_rate==0", bt.trade_stats([])["win_rate"] == D("0"))
    # 对基准
    rb = bt.benchmark_relative([100, 106], [100, 105])
    check("超额==1.00pp", rb["excess_pp"] == D("1.00"), str(rb))
    # 样本充分性守卫（n=1 必须判不足）
    check("样本不足守卫：1 笔成交 -> sufficient False",
          bt.sample_sufficiency(1, 2)["sufficient"] is False)
    check("样本充分：25 笔 + 25 点 -> sufficient True",
          bt.sample_sufficiency(25, 25)["sufficient"] is True)
    # run 汇总不抛且键齐全
    r = bt.run([100, 97], [{"realized": "171.51"}], benchmark=[100, 101])
    check("run 汇总键齐全",
          set(["total_return_pct", "max_drawdown_pct", "trades", "sample", "vs_benchmark"]) <= set(r), str(r.keys()))


def main():
    print("=" * 70)
    print("us-market-system 自检 —— 可执行规范")
    print("=" * 70)
    for fn in (test_routing, test_schedule_alignment, test_regime, test_slots,
               test_accounting, test_staleness, test_provenance, test_outbox,
               test_report_lint, test_quote_extract, test_knowledge,
               test_high_availability, test_data_layer, test_selection,
               test_backtest):
        fn()
    print("\n" + "=" * 70)
    print("合计：%d 通过，%d 失败" % (PASS, FAIL))
    if FAILURES:
        print("\n失败项：")
        for f in FAILURES:
            print("  -", f)
    print("=" * 70)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
