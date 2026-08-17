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

    # 2026-08-17 Phase 2：cron に分40 追加（CLOSING 収盘执行窓）→ 五阶段全可达を要求。
    good = mc.verify_schedule_alignment({0, 30, 40}, {0, 1, 2, 3, 4, 5, 8, 20, 21, 22, 23},
                                        CAL, days, jitter_s=60)
    check("新 cron `0,30,40` 必须五阶段（含 CLOSING）全可达且稳健", good["ok"],
          "unreachable=%s fragile=%s" % (good["unreachable"], good["fragile"]))
    check("新 cron POST_CLOSE jitter 余量 >= 5 分钟",
          good["post_close_margin_min"] is not None and good["post_close_margin_min"] >= 5,
          "margin=%s" % good["post_close_margin_min"])


def test_closing_window():
    # 收盘执行窗（CLOSING）：引け 20 分前 <= et < 引け ＝ in-session の唯一取引執行フェーズ。
    # 目的：①route() が正常日/早收盘日で CLOSING 境界を正しく切ること（16:00 非依存・日历追従）、
    # ②既存 INTRADAY/POST_CLOSE を壊さないこと、③提案発火（ET15:40）が MOC 締切 ET15:50 前に
    # CLOSING を命中し余裕があること（提案cron、まだ非ライブ）、④REQUIRED_CRON とライブ非変更。
    print("\n== 收盘执行窗 CLOSING（引け20分前 in-session 执行窓、Phase 1 = routing/証明/文書のみ）==")

    # (a) 普通日 15:45 ET -> CLOSING（窓 15:40–16:00）
    check("CLOSING (a) 15:45 ET 普通日 -> CLOSING（收盘执行窗）",
          mc.route(et("2026-07-27 15:45"), CAL)["stage"] == mc.CLOSING_STAGE,
          "got %s" % mc.route(et("2026-07-27 15:45"), CAL)["stage"])
    # (b) 15:30 ET は :30 チェックポイント＝INTRADAY のまま（境界：窓下端 close-20 の手前）
    r_1530 = mc.route(et("2026-07-27 15:30"), CAL)
    check("CLOSING (b) 15:30 ET -> INTRADAY(1530)（收盘前最后检查点、CLOSING 窓に飲まれない）",
          r_1530["stage"] == "INTRADAY" and r_1530["checkpoint"] == "1530", str(r_1530))
    check("CLOSING 境界：15:39 ET -> INTRADAY（窓下端 15:40 の直前）",
          mc.route(et("2026-07-27 15:39"), CAL)["stage"] == "INTRADAY")
    check("CLOSING 境界：15:40 ET -> CLOSING（窓下端 close-20、包含）",
          mc.route(et("2026-07-27 15:40"), CAL)["stage"] == mc.CLOSING_STAGE)
    check("CLOSING 境界：15:59 ET -> CLOSING（窓上端、引け直前）",
          mc.route(et("2026-07-27 15:59"), CAL)["stage"] == mc.CLOSING_STAGE)
    check("CLOSING 境界：16:00 ET -> 非CLOSING（引け丁度は窓外、et<close 厳密）",
          mc.route(et("2026-07-27 16:00"), CAL)["stage"] != mc.CLOSING_STAGE)
    # (c) 16:05 ET（引け後）-> CLOSING でない（結算はまだ、POST_CLOSE は +20min から）
    check("CLOSING (c) 16:05 ET -> 非CLOSING（引け後は执行窓でない）",
          mc.route(et("2026-07-27 16:05"), CAL)["stage"] != mc.CLOSING_STAGE)

    # (d) 早收盘日 12:45 ET -> CLOSING（close=13:00 を日历から取得、窓 12:40–13:00、16:00 非依存）
    r_ec = mc.route(et("2026-11-27 12:45"), CAL)
    check("CLOSING (d) 早收盘日 12:45 ET -> CLOSING（close=13:00 自动追従、窓 12:40–13:00）",
          r_ec["stage"] == mc.CLOSING_STAGE and "12:40-13:00" in r_ec["reason"], str(r_ec))
    check("CLOSING 早收盘日 12:40 ET -> CLOSING（窓下端 close-20）",
          mc.route(et("2026-11-27 12:40"), CAL)["stage"] == mc.CLOSING_STAGE)
    check("CLOSING 早收盘日 12:39 ET -> INTRADAY（窓下端の直前）",
          mc.route(et("2026-11-27 12:39"), CAL)["stage"] == "INTRADAY")
    check("CLOSING 早收盘日 13:00 ET -> 非CLOSING（引け丁度は窓外）",
          mc.route(et("2026-11-27 13:00"), CAL)["stage"] != mc.CLOSING_STAGE)

    # (e) 通常日 12:45 ET -> 非CLOSING。CLOSING は**实 close_time 基準**であって壁時計固定ではない
    #     ことの固定：同じ 12:45 でも close=16:00 の通常日は窓外。
    #     （route の実返値は NO_STAGE＝12:30 チェックポイントの宽限外。それは CLOSING と直交する
    #       検查点吸附の性質で、ここで固定したいのは「CLOSING 窓に入らない」こと。）
    check("CLOSING (e) 通常日 12:45 ET -> 非CLOSING（窓は close_time 基準、壁時計固定でない）",
          mc.route(et("2026-07-27 12:45"), CAL)["stage"] != mc.CLOSING_STAGE)
    check("CLOSING 日历分岐：同一壁時計 12:45 が早收盘日=CLOSING / 通常日=非CLOSING",
          mc.route(et("2026-11-27 12:45"), CAL)["stage"] == mc.CLOSING_STAGE
          and mc.route(et("2026-07-27 12:45"), CAL)["stage"] != mc.CLOSING_STAGE)

    # ------ (f) 提案発火（ET15:40）が MOC 締切 ET15:50 前に CLOSING を命中する証明 ------
    # 提案cron、まだ非ライブ（REQUIRED_CRON 不変）。実測ジッタ 87–137s 後でも締切前に余裕を持つ。
    # 夏 EDT=UTC-4 / 冬 EST=UTC-5 で SGT 発火時刻が変わる点も併せて固定（ET15:40→夏SGT03:40/冬SGT04:40）。
    from datetime import time as _dtime
    MOC_DEADLINE = _dtime(15, 50)   # 引け 10 分前を MOC 発注締切と置く（普通日 close=16:00）
    proof_days = [(date(2026, 8, 17), "夏EDT", "03:40"), (date(2026, 1, 5), "冬EST", "04:40")]
    for day, season, want_sgt in proof_days:
        fire_et = datetime.combine(day, _dtime(15, 40), tzinfo=mc.ET)
        # 発火名目 SGT が季節で変わることを固定（ET15:40 → 夏 03:40 / 冬 04:40）
        sgt0 = fire_et.astimezone(mc.SGT)
        check("CLOSING (f) 提案発火 ET15:40 の SGT は %s（%s、DST 追従）" % (want_sgt, season),
              sgt0.strftime("%H:%M") == want_sgt, "got %s" % sgt0.strftime("%H:%M"))
        check("CLOSING (f) 発火 ET15:40 の SGT hour は live hours 0-5 圏内・分 40（新 cron に追加済み）（%s）" % season,
              sgt0.hour in {0, 1, 2, 3, 4, 5} and sgt0.minute == 40, str(sgt0))
        for j in (0, 87, 137):
            u = (fire_et + timedelta(seconds=j)).astimezone(mc.UTC)
            r = mc.route(u, CAL)
            etv = r["et"]
            deadline_dt = etv.replace(hour=MOC_DEADLINE.hour, minute=MOC_DEADLINE.minute,
                                      second=0, microsecond=0)
            margin_min = (deadline_dt - etv).total_seconds() / 60.0
            ok = (r["stage"] == mc.CLOSING_STAGE and etv < deadline_dt and margin_min >= 7.0)
            check("提案cron ET15:40+jitter 命中 CLOSING 且 MOC 15:50 前有余裕（%s jitter=%ds、余裕 %.1f 分）"
                  % (season, j, margin_min), ok,
                  "stage=%s et=%s margin=%.2f" % (r["stage"], etv.strftime("%H:%M:%S"), margin_min))

    # ------ (g) Phase 2 ライブ切替：cron に分40 追加 + CLOSING を STAGES 編入 ------
    # ライブ OS 定時タスクの cron も同値 `0,30,40 0-5,8,20-23` に更新済み（repo と lockstep、ドリフト無）。
    import preflight as pf
    check("CLOSING (g) preflight.REQUIRED_CRON に分40 追加済み（ライブ cron と一致）",
          pf.REQUIRED_CRON == ({0, 30, 40}, {0, 1, 2, 3, 4, 5, 8, 20, 21, 22, 23}),
          str(pf.REQUIRED_CRON))
    check("CLOSING (g) CLOSING は STAGES（ライブ到達性契約）に編入済み",
          mc.CLOSING_STAGE in mc.STAGES and mc.CLOSING_STAGE == "CLOSING")
    days_g = [date(2026, 7, 27) + timedelta(days=i) for i in range(5)]
    align = mc.verify_schedule_alignment(pf.REQUIRED_CRON[0], pf.REQUIRED_CRON[1],
                                         CAL, days_g, jitter_s=60)
    check("CLOSING (g) 新 cron で CLOSING は到達可能（unreachable に無）",
          "CLOSING" not in align["unreachable"], str(align.get("unreachable")))
    check("CLOSING (g) 新 cron 全阶段到达 ok=True（SCHEDULE_MISALIGNED なし・脆弱点なし）",
          align["ok"] and not align["unreachable"] and not align["fragile"],
          "unreachable=%s fragile=%s" % (align["unreachable"], align["fragile"]))


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

    # --- C3/C4/C5 单点检出力（2026-08-15 审计补齐：三守卫在生产会发火，
    #     却从无失败用例；L-007/L-023 规律要求「异常系确实落红」被固定）---
    # C3：仅篡改钱包总未实现 -> C3 必须发；逐仓 C4/C5 与 C1/C2 全绿，
    #     证明失败归因在「分解层」（C6 同时变红属正确行为：累计=已实现+未实现）。
    t_c3 = dict(wallet, unrealized_pnl="-40.000000")
    r_c3 = ig.validate_accounting(t_c3, positions)
    c3 = [r for r in r_c3 if r.name.startswith("C3")]
    check("C3 检出力：仅篡改总未实现 -> C3 passed=False",
          len(c3) == 1 and not c3[0].passed and not ig.summarize(r_c3)["ok"],
          str([repr(x) for x in c3]))
    check("C3 单点归因：C1/C2 与逐仓 C4/C5 保持全绿",
          all(r.passed for r in r_c3
              if r.name.startswith(("C1", "C2", "C4", "C5"))),
          str([repr(r) for r in r_c3 if not r.passed]))
    # C4：仅篡改单仓 market_value -> 该仓 C4 必须发；C1/C2/C3 与其余仓 C4 全绿
    #     （该仓 C5 同时变红属正确行为：C5 以存储 market_value 为输入）。
    t_c4 = [dict(p) for p in positions]
    t_c4[0]["market_value"] = "4999.999999"          # GEV
    r_c4 = ig.validate_accounting(wallet, t_c4)
    check("C4 检出力：仅篡改 GEV market_value -> C4 GEV passed=False",
          any(r.name.startswith("C4 GEV") and not r.passed for r in r_c4)
          and not ig.summarize(r_c4)["ok"],
          str([repr(r) for r in r_c4 if not r.passed]))
    check("C4 单点归因：C1/C2/C3 与其余仓 C4 全绿",
          all(r.passed for r in r_c4
              if r.name.startswith(("C1", "C2", "C3"))
              or (r.name.startswith("C4") and "GEV" not in r.name)),
          str([repr(r) for r in r_c4 if not r.passed]))
    # C5：仅篡改单仓 unrealized -> 该仓 C5 必须发；C1/C2 与全部 C4 全绿
    #     （C3 同时变红属正确行为：总未实现分解依赖逐仓未实现）。
    t_c5 = [dict(p) for p in positions]
    t_c5[1]["unrealized_pnl"] = "0.000000"           # ETN
    r_c5 = ig.validate_accounting(wallet, t_c5)
    check("C5 检出力：仅篡改 ETN unrealized -> C5 ETN passed=False",
          any(r.name.startswith("C5 ETN") and not r.passed for r in r_c5)
          and not ig.summarize(r_c5)["ok"],
          str([repr(r) for r in r_c5 if not r.passed]))
    check("C5 单点归因：C1/C2 与全部 C4 保持全绿",
          all(r.passed for r in r_c5
              if r.name.startswith(("C1", "C2", "C4"))),
          str([repr(r) for r in r_c5 if not r.passed]))


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

    # P4 检出力（2026-08-15 审计补齐：P4 在生产会发火，却从无一条失败用例——
    # 按 L-007/L-023 规律，「从未被构造过失败的守卫」不算存在）：
    # 无 ?v= 缓存参数的 stockanalysis URL 必须被 P4 检出（WARN 级、passed=False）。
    nocb = ig.PriceRecord("MSFT", "2026-08-14", "495.40", [
        {"domain": "stockanalysis.com", "figure": "495.40",
         "url": "https://stockanalysis.com/stocks/msft/", "method": "web_fetch"},
        {"domain": "roic.ai", "figure": "495.40",
         "url": "https://roic.ai/quote/MSFT", "method": "web_fetch"}])
    p4 = [r for r in nocb.validate() if r.name.startswith("P4")]
    check("P4 无 cache-buster URL 必须被检出（passed=False）",
          len(p4) == 1 and not p4[0].passed and p4[0].severity == "WARN",
          str([repr(r) for r in nocb.validate()]))
    check("P4 带 cache-buster URL 不误报（good 记录无 P4 项）",
          not [r for r in good.validate() if r.name.startswith("P4")])


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

    # 一份合规的盘中报告（标题+日期、动作合规、建议未执行、账务字段 L7、色分 L8、篇幅内）
    # 同时覆盖 2026-08-04 新版两行式（**加粗代码** + └ 原因行）与旧版单行式（着色后仍合规）。
    good = (
        "# 美股盘中报告｜2026-07-27\n"
        "**ABT** · 持有｜成本 103.83｜今日 <font color=\"warning\">+1.2%</font>｜累计 <font color=\"warning\">+1.7%</font>\n"
        "└ 未触发止盈条件\n"
        "MP · 减仓建议未执行 · 成本44.88｜今日<font color=\"info\">-2.0%</font>｜累计<font color=\"info\">-7.2%</font> · 相对大盘走弱，需收盘确认\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>｜累计 <font color=\"info\">-2.9%</font>）\n"
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
        "# 盘中｜2026-07-27\n全部持有，无减仓/平仓信号\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("「无减仓/平仓信号」不得误判（L4 否定守卫）", negated["ok"],
          str(negated["violations"]))

    # L4（2026-07-27 修复）：条件/检查语境里的前瞻动作词不得误判。
    conditional = rl.lint_report(
        "# 美股盘前｜2026-07-27\nMP · 持有（建议未执行）· 成本44.88｜昨日<font color=\"info\">-2.0%</font>｜累计<font color=\"info\">-7.2%</font> · 财报前不动\n"
        "开盘后检查：若 BE 盘后财报破坏基本面，待正式收盘技术确认后再议减仓\n"
        "账户：总资产 97,127（昨日 <font color=\"warning\">+0.4%</font>｜累计 <font color=\"info\">-2.9%</font>）", "PREMARKET")
    check("条件/检查语境「若…待确认…再议减仓」不得误判（L4 条件守卫）",
          conditional["ok"], str(conditional["violations"]))

    # L4 检出力保留：真实的、当下的未标注交易动作行仍须判违规。
    real_unlabeled = rl.lint_report(
        "# 美股盘前｜2026-07-27\nMP 减仓20%", "PREMARKET")
    check("当下未标注「建议未执行」的真实交易动作仍须判违规（L4 保留检出力）",
          not real_unlabeled["ok"], str(real_unlabeled["violations"]))

    # L5 已撤销（2026-07-27 用户裁定）：无来源标注也合格
    nosrc = rl.lint_report(
        "# 盘中｜2026-07-27\nABT · 持有 · 成本103.83｜今日<font color=\"warning\">+1.2%</font>｜累计<font color=\"warning\">+1.7%</font> · 未触发止盈\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("无来源/as-of 标注也合格（L5 撤销）", nosrc["ok"], str(nosrc["violations"]))

    # L7（2026-07-31 用户裁定）：账务透明硬门
    no_acct = rl.lint_report(
        "# 盘中｜2026-07-27\nABT · 持有 · 成本103.83｜今日+1.2%｜累计+1.7% · ok", "INTRADAY")
    check("缺「总资产」账户行必须判违规（L7）", not no_acct["ok"])
    no_cost = rl.lint_report(
        "# 盘中｜2026-07-27\nABT · 持有 · 未触发止盈\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("持仓行缺成本/今日/累计必须判违规（L7）", not no_cost["ok"])
    bold_no_cost = rl.lint_report(
        "# 盘中｜2026-08-04\n**ABT** · 持有 · 未触发止盈\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("加粗代码行仍被 L7 识别（缺账务字段判违规）", not bold_no_cost["ok"])
    forecast_line = rl.lint_report(
        "# 盘中｜2026-07-27\nABT · 持有 · 成本103.83｜今日<font color=\"warning\">+1.2%</font>｜累计<font color=\"warning\">+1.7%</font> · ok\n"
        "📊 KTOS 财报 8/4：共识 EPS 0.14，若确认订单加速则维持\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("📊 财报前瞻行不受 L7 账务要求（非动作行）", forecast_line["ok"],
          str(forecast_line["violations"]))

    # L8（2026-08-04 用户裁定）：盈亏百分比必须红涨绿跌着色，数据不得裸摆
    uncolored = rl.lint_report(
        "# 盘中｜2026-08-04\nABT · 持有 · 成本103.83｜今日+1.2%｜累计+1.7% · ok\n"
        "账户：总资产 97,127（今日 +0.4%）", "INTRADAY")
    check("持仓/账户行百分比未着色必须判违规（L8）", not uncolored["ok"])
    check("L8 违规信息明确指向着色",
          any("L8" in x for x in uncolored["violations"]), str(uncolored["violations"]))
    # 📊/🚨/└ 行不作着色要求（forecast_line 已覆盖 📊；此处覆盖 └ 原因行）
    reason_line = rl.lint_report(
        "# 盘中｜2026-08-04\n**ABT** · 持有｜成本 103.83｜今日 <font color=\"warning\">+1.2%</font>｜累计 <font color=\"warning\">+1.7%</font>\n"
        "└ 距 50 日线 3% 内，未触发条件\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("└ 原因行不受 L8 着色要求", reason_line["ok"], str(reason_line["violations"]))
    # L2 按可见字符计：font 标签与加粗记号不占篇幅预算
    check("L2 字数剔除 font 标签", rl._char_count('<font color=\"info\">-7.2%</font>') == 5)
    check("L2 字数剔除加粗记号", rl._char_count("**ABT**") == 3)

    # L6：内部事务不得泄漏进推送
    leak1 = rl.lint_report("# 盘中｜2026-07-27\nABT 持有（来源 stockanalysis.com）", "INTRADAY")
    check("来源域名进正文必须判违规（L6）", not leak1["ok"])
    leak2 = rl.lint_report("# 盘中｜2026-07-27\nMP 持有，数据降级", "INTRADAY")
    check("「数据降级」进正文必须判违规（L6）", not leak2["ok"])
    leak3 = rl.lint_report("# 盘中｜2026-07-27\n持有；MARKET_DATA_DEGRADED", "INTRADAY")
    check("升级项代码进正文必须判违规（L6）", not leak3["ok"])

    # L6 扩展（2026-08-04 用户裁定）：机制词/规则代号不得进推送——说人话
    jargon1 = rl.lint_report(
        "# 盘中｜2026-08-04\nABT · 持有 · 成本103.83｜今日<font color=\"warning\">+1.2%</font>｜累计<font color=\"warning\">+1.7%</font> · 未过 ACT-005 事件封锁\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("规则代号 ACT-xxx 进正文必须判违规（L6 平实语言）", not jargon1["ok"])
    jargon2 = rl.lint_report(
        "# 盘中｜2026-08-04\nABT · 持有 · 成本103.83｜今日<font color=\"warning\">+1.2%</font>｜累计<font color=\"warning\">+1.7%</font> · 候选未过门槛，不替换\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("机制词「门槛」进正文必须判违规（L6 平实语言）", not jargon2["ok"])
    hotword = rl.lint_report(
        "# 盘中｜2026-08-04\nABT · 持有 · 成本103.83｜今日<font color=\"warning\">+1.2%</font>｜累计<font color=\"warning\">+1.7%</font> · 热门题材拥挤，按持仓逻辑不动\n"
        "账户：总资产 97,127（今日 <font color=\"warning\">+0.4%</font>）", "INTRADAY")
    check("日常词「热门」不得误伤（L6 高精确选词）", hotword["ok"],
          str(hotword["violations"]))

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
                           "# 美股盘前｜2026-07-27\n全部持有（建议未执行）\n"
                           "账户：总资产 97,127（昨日 <font color=\"warning\">+0.4%</font>｜累计 <font color=\"info\">-2.9%</font>）",
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


def test_queue_watchdog():
    print("\n== W3/W4 队列看门狗检出力（2026-08-15 审计补齐）==")
    # queue_state 的计数口径此前有用例，queue_health 本体（W3/W4 的合否判定）没有——
    # 「会发火但从未被证明会失败」按 L-007/L-023 规律必须补上异常系用例。
    now = datetime(2026, 8, 15, 12, 0, tzinfo=mc.UTC)
    r = ig.queue_health([], ["20260815-000000_X.json"], now, None)
    w3 = [x for x in r if x.name.startswith("W3")]
    check("W3 死信非空必须 ERROR 检出",
          len(w3) == 1 and not w3[0].passed and w3[0].severity == "ERROR",
          str([repr(x) for x in r]))
    r2 = ig.queue_health(["p.json"], [], now, 45.0)
    w4 = [x for x in r2 if x.name.startswith("W4")]
    check("W4 积压超时必须 ERROR 检出",
          len(w4) == 1 and not w4[0].passed and w4[0].severity == "ERROR",
          str([repr(x) for x in r2]))
    check("W3/W4 空队列全绿（不误报）",
          all(x.passed for x in ig.queue_health([], [], now, None)))
    check("W4 恰好 30 分钟（边界=上限内）不发",
          all(x.passed for x in ig.queue_health(["p.json"], [], now, 30.0)
              if x.name.startswith("W4")))


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
    # 2026-08-11 实测：stockscan.io 对 5/8 标的返回 7 月下旬旧行情（按标的冻结），
    # 与 stocktitan 同类；若无 stamp 核对会把陈旧价当官方收盘入账（L-022）。
    check("stockscan 标记 stamp_check（与 STAMP_CHECK_REQUIRED 一致）",
          eq["stockscan.io"].get("stamp_check") is True
          and "stockscan.io" in ig.STAMP_CHECK_REQUIRED)
    # 该 quirk 必须真的有检出力：无 stamp 时 P5 必须报出来
    _pr = ig.PriceRecord("XYZ", "2026-08-11", "10.00",
                         [{"domain": "stockanalysis.com", "figure": "10.00", "url": "https://x/?v=1"},
                          {"domain": "stockscan.io", "figure": "10.00", "url": "https://y"}])
    _p5 = [r for r in _pr.validate() if r.name.startswith("P5") and "stockscan.io" in r.name]
    check("P5 对无 stamp 的 stockscan.io 有检出力", len(_p5) == 1 and not _p5[0].passed)
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
    # ACT-004 确定性替换门（2026-08-04 用户裁定确立；2026-08-15 用户裁定收紧为下述契约）
    # 冻结中：任何分差都不得放行（冻结是最外层，先于一切分差判断）
    check("替换门：冻结期内即便 +99 分也不替换",
          sel.replacement_gate(179, 80)[0] is False)
    check("替换门：冻结理由可读且指向解冻条件",
          "解冻条件" in sel.replacement_gate(179, 80)[1])
    check("REPLACEMENT_FROZEN 默认开启（用户 2026-08-15 裁定）",
          sel.REPLACEMENT_FROZEN is True)
    # 以下解冻后的契约用 frozen=False 显式测（解冻当日这些门必须已经生效）
    rg_ok, rg_why = sel.replacement_gate(100, 80, sessions_held=30, frozen=False)
    check("替换门：论点分+20 >15 且持有期已过 -> 允许替换", rg_ok, rg_why)
    check("替换门：恰好+15分（边界）-> 不自动执行，须人工复核",
          sel.replacement_gate(95, 80, sessions_held=30, frozen=False)[0] is False)
    check("替换门：边界理由须点明「边界即停」而非「分差不足」",
          "边界" in sel.replacement_gate(95, 80, sessions_held=30, frozen=False)[1])
    check("替换门：+14分 <15 -> 不替换",
          sel.replacement_gate(94, 80, sessions_held=30, frozen=False)[0] is False)
    check("REPLACEMENT_MARGIN 已由 5 提高到 15（用户 2026-08-15 裁定）",
          sel.REPLACEMENT_MARGIN == D("15"))
    # ACT-008 最低持有期：LLY（5 个交易日）与 NVDA（3 个交易日）的真实回归用例
    check("ACT-008 持有5日(LLY实况)+分差达标 -> 仍不得因相对分卖出",
          sel.replacement_gate(100, 80, sessions_held=5, frozen=False)[0] is False)
    check("ACT-008 持有3日(NVDA实况)+分差达标 -> 仍不得因相对分卖出",
          sel.replacement_gate(100, 80, sessions_held=3, frozen=False)[0] is False)
    check("ACT-008 恰好第15日 -> 可参与替换排序（边界）",
          sel.min_holding_gate(15)[0] is True)
    check("ACT-008 第14日 -> 不可（边界）", sel.min_holding_gate(14)[0] is False)
    check("ACT-008 失效线触发 -> 风险管理优先，最低持有期不阻断离场",
          sel.min_holding_gate(1, invalidation_hit=True)[0] is True)
    check("ACT-008 失效线触发时替换门亦放行（持有1日）",
          sel.replacement_gate(100, 80, sessions_held=1,
                               invalidation_hit=True, frozen=False)[0] is True)
    check("ACT-008 建仓日不可考 -> 按已过期处理且理由须标注",
          sel.min_holding_gate(None)[0] is True
          and "不可考" in sel.min_holding_gate(None)[1])
    # ACT-009 替换排序只用论点维度（技术面/指标不得参与）
    _dims = {"信息调研": 9, "基本面": 9, "事件驱动": 9, "产业链": 9, "财报": 9,
             "情绪": 9, "全球局势": 9, "技术面": 10, "指标": 10}
    check("ACT-009 论点分排除技术面/指标（63 而非 83）",
          sel.thesis_score(_dims) == D("63"))
    _weak_price = dict(_dims, 技术面=1, 指标=1)
    check("ACT-009 价格维度崩塌不改变论点分（刚下跌的仓不会自动变最弱）",
          sel.thesis_score(_weak_price) == sel.thesis_score(_dims))
    _incomplete = {k: v for k, v in _dims.items() if k != "财报"}
    try:
        sel.thesis_score(_incomplete)
        check("ACT-009 缺维必须报错（有检出力）", False, "缺维未被拒绝")
    except ValueError as e:
        check("ACT-009 缺维必须报错（有检出力）", "财报" in str(e), str(e))
    # ---- 历史回归：2026-08-05～08-14 的五次真实替换全部重放 ----------------------
    # 实测结果（8/14 收盘）：可测的四次全部劣后于「什么都不做」。
    # 本用例锁定「新规则下这些执行还会不会发生」，是本次改动的唯一有意义的验收标准。
    # (名称, 候选分, 最弱仓分, 被卖仓持有交易日数, 实测劣后pp, 新规下应否放行)
    _history = [
        ("RMBS→MSFT 8/05 (+17)", 85, 68, None, "-2.0pp", True),   # 仍会放行 —— 显式承认未覆盖
        ("BE→NVDA 8/07 (+13)",   82, 69, None, "-5.4pp", False),
        ("GEV→LLY 8/10 (+12)",   86, 74, None, "-11.5pp", False),
        ("NVDA→LNG 8/11 (+9)",   85, 76, 3,    "-1.2pp", False),
        ("LLY→TSM 8/14 (+5)",    81, 76, 5,    "判定前", False),
    ]
    for name, cand, weak, held, drag, should_pass in _history:
        got = sel.replacement_gate(cand, weak, sessions_held=held, frozen=False)[0]
        check("历史回归 %s 实测%s -> 新规%s" % (name, drag, "仍放行" if should_pass else "已拦截"),
              got is should_pass, "expected=%s got=%s" % (should_pass, got))
    _blocked = sum(1 for n, c, w, h, d, sp in _history
                   if sel.replacement_gate(c, w, sessions_held=h, frozen=False)[0] is False)
    check("历史回归：五次替换中至少拦下四次（否则改动无效）", _blocked >= 4,
          "blocked=%d/5" % _blocked)
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


def test_learning():
    print("\n[learning] 自我修正闭环（claim/影子帐簿/记分卡/教训执行状态，SYSTEM.md §4.2）")
    import json as _json
    import learning as lrn
    from decimal import Decimal as D

    def _mk(cid="T-ok", **kw):
        base = dict(claim_id=cid, kind=lrn.KIND_REPLACEMENT, made_on="2026-08-14",
                    subject="TSM", baseline="LLY", metric="relative_return_pct_vs_sold",
                    threshold="0", direction=">", horizon_sessions=60,
                    adjudicate_on="2026-11-09")
        base.update(kw)
        return lrn.make_claim(**base)

    check("合法主张可登记且初始 OPEN", _mk()["status"] == lrn.OPEN)

    # --- 反证不能守卫：四种残缺主张都必须真的被拒（L-007/L-023：正常系だけの断言は無効）---
    for name, patch in [("无阈值", dict(threshold=None)),
                        ("无裁定日", dict(adjudicate_on=None)),
                        ("期限 0 交易日", dict(horizon_sessions=0)),
                        ("未知 kind", dict(kind="vibes"))]:
        try:
            _mk("T-bad", **patch)
            check("不可证伪主张（%s）必须抛 NotFalsifiable" % name, False, "未抛异常")
        except lrn.NotFalsifiable:
            check("不可证伪主张（%s）必须抛 NotFalsifiable" % name, True)

    # --- 机械裁定：direction 全矩阵，含边界 ==（命中与否不由叙述决定）---
    def _mkd(dirn):
        return _mk("T-" + dirn, metric="m", threshold="10", direction=dirn)
    check("adjudicate >  观测10==阈值10 -> MISS（边界不算赢）",
          lrn.adjudicate(_mkd(">"), "10", "2026-11-09")["status"] == lrn.MISS)
    check("adjudicate >= 观测10==阈值10 -> HIT",
          lrn.adjudicate(_mkd(">="), "10", "2026-11-09")["status"] == lrn.HIT)
    check("adjudicate >  观测10.01 -> HIT",
          lrn.adjudicate(_mkd(">"), "10.01", "2026-11-09")["status"] == lrn.HIT)
    check("adjudicate <  观测9.99 -> HIT",
          lrn.adjudicate(_mkd("<"), "9.99", "2026-11-09")["status"] == lrn.HIT)
    check("adjudicate <  观测10==阈值10 -> MISS（边界不算赢）",
          lrn.adjudicate(_mkd("<"), "10", "2026-11-09")["status"] == lrn.MISS)
    check("adjudicate <= 观测10.01 -> MISS",
          lrn.adjudicate(_mkd("<="), "10.01", "2026-11-09")["status"] == lrn.MISS)

    # --- 终结不可重裁（防事后改判）---
    _adj = lrn.adjudicate(_mk("T-final"), "1.0", "2026-11-09")
    try:
        lrn.adjudicate(_adj, "-1.0", "2026-11-10")
        check("已终结主张重裁必须被拒", False, "未抛异常")
    except ValueError:
        check("已终结主张重裁必须被拒", True)

    # --- VOID：无理由拒绝；有理由计入记分卡（作废不得成为逃避裁定的暗门）---
    try:
        lrn.void_claim(_mk("T-v1"), "   ", "2026-08-15")
        check("VOID 无理由必须被拒", False, "未抛异常")
    except ValueError:
        check("VOID 无理由必须被拒", True)
    _void = lrn.void_claim(_mk("T-v2"), "标的被收购退市，metric 失义", "2026-08-15")
    try:
        lrn.void_claim(_void, "再作废一次", "2026-08-16")
        check("已终结主张再作废必须被拒", False, "未抛异常")
    except ValueError:
        check("已终结主张再作废必须被拒", True)
    _sc_v = lrn.scorecard([_adj, _void])
    check("VOID 计入记分卡（n_void==1，不被静默丢弃）", _sc_v["n_void"] == 1, str(_sc_v))

    # --- overdue_claims 检出力：真的能抓到逾期（这是 W6 的牙齿，必须证明会咬）---
    _late = _mk("T-late", adjudicate_on="2026-08-10")
    check("逾期 5 天的 OPEN 主张必须被检出",
          [c["claim_id"] for c in lrn.overdue_claims([_late], date(2026, 8, 15))] == ["T-late"])
    _due = _mk("T-due", adjudicate_on="2026-08-14")
    check("到期 1 天（宽限内）不算逾期、但列入 due（当次必须裁定）",
          not lrn.overdue_claims([_due], date(2026, 8, 15))
          and [c["claim_id"] for c in lrn.due_claims([_due], date(2026, 8, 15))] == ["T-due"])
    check("已裁定的主张不再算逾期",
          not lrn.overdue_claims([lrn.adjudicate(_late, "1", "2026-08-15")], date(2026, 12, 1)))

    # --- B1 检出力（2026-08-15 审计）：grace 口径必须是交易日，不是暦日 ---
    # 修复前：周五到期的 claim 在周日被判 OVERDUE（暦日 2 > grace 1），W6(ERROR)
    # 会在周末误阻断健全的 MORNING/POST_CLOSE（可用性回归）。注入交易日计数器后封堵。
    _fri = _mk("T-fri", adjudicate_on="2026-08-14")     # 2026-08-14 = 周五
    check("(B1a) 周五到期在周日（暦日+2、交易日+0）注入交易日历后**不算逾期**",
          not lrn.overdue_claims([_fri], date(2026, 8, 16),
                                 sessions_between=CAL.trading_days_between))
    check("(B1b) 交易日超过宽限必须逾期（周五到期 -> 下周二 = +2 交易日 > 1）",
          [c["claim_id"] for c in lrn.overdue_claims(
              [_fri], date(2026, 8, 18),
              sessions_between=CAL.trading_days_between)] == ["T-fri"])
    check("(B1c) 未注入时退化为暦日差（兜底口径，docstring 已声明调用方必须注入）",
          [c["claim_id"] for c in lrn.overdue_claims([_fri], date(2026, 8, 16))]
          == ["T-fri"])

    # --- 记分卡：样本不足 = 判定不能（非失败）；样本充分 = sufficient True ---
    _few = [lrn.adjudicate(_mk("T-f%d" % i), "1", "2026-11-09") for i in range(3)]
    _sc_few = lrn.scorecard(_few)
    check("3 样本 -> sufficient=False 且 verdict 含「判定不能」",
          _sc_few["sufficient"] is False and "判定不能" in _sc_few["verdict"], str(_sc_few))
    _many = [lrn.adjudicate(_mk("T-m%d" % i), "1" if i < 12 else "-1", "2026-11-09")
             for i in range(20)]
    _sc_many = lrn.scorecard(_many)
    check("20 裁定样本 -> sufficient=True", _sc_many["sufficient"] is True, str(_sc_many))
    check("记分卡命中率正确（12/20=60%）", _sc_many["hit_rate_pct"] == D("60"), str(_sc_many))

    # --- 教训执行状态：三类缺陷全部检出（未声明/CODIFIED 无测试名/PROSE_ONLY 无理由）---
    _reg = {"L-A": {"status": "CODIFIED", "test": "some test"},
            "L-B": {"status": "CODIFIED"},
            "L-C": {"status": "PROSE_ONLY"},
            "L-D": {"status": "PROSE_ONLY", "reason": "机械不可判"}}
    _enf = lrn.lesson_enforcement(_reg, ["L-A", "L-B", "L-C", "L-D", "L-E"])
    check("CODIFIED 无测试名 / PROSE_ONLY 无理由 / 完全未声明 -> 全部判缺陷",
          set(_enf["undeclared"]) == {"L-B", "L-C", "L-E"} and _enf["ok"] is False, str(_enf))
    check("合规声明正确计数（1 codified + 1 prose）",
          _enf["codified"] == 1 and _enf["prose_only"] == 1, str(_enf))
    check("全部合规声明 -> ok=True",
          lrn.lesson_enforcement(_reg, ["L-A", "L-D"])["ok"] is True)

    # --- 影子帐簿：GEV→LLY 实数据回归（8/14 收盘），符号约定「负 = 什么都不做更好」---
    _e = lrn.shadow_entry("GEV", "2026-08-10", "990.85", "LLY", "1231.94")
    _dl = lrn.shadow_delta(_e, "1063.25", "1180.16")
    check("GEV→LLY delta 为负（替换劣于不动）", _dl["delta_pp"] < 0, str(_dl))
    check("GEV→LLY delta == -11.5pp（与 8/15 审计一致）",
          _dl["delta_pp"].quantize(D("0.1")) == D("-11.5"), str(_dl["delta_pp"]))
    check("GEV 卖后收益 +7.3%（卖出后仍被定价 = 不失明）",
          _dl["sold_return_pct"].quantize(D("0.1")) == D("7.3"))
    _dl2 = lrn.shadow_delta(lrn.shadow_entry("X", "2026-08-10", "100", None), "90", None)
    check("无替换标的时 delta=None 但卖出收益仍可算",
          _dl2["delta_pp"] is None and _dl2["sold_return_pct"] == D("-10"))

    # --- IO 边界：重复 claim_id 拒绝；空目录不崩（preflight 例外安全的根据）---
    tmp = tempfile.mkdtemp()
    try:
        lrn.register_claim(tmp, _mk("T-io"))
        try:
            lrn.register_claim(tmp, _mk("T-io"))
            check("重复 claim_id 必须被拒", False, "未抛异常")
        except ValueError:
            check("重复 claim_id 必须被拒", True)
        check("JSONL 往返一致", lrn.load_claims(tmp)[0]["claim_id"] == "T-io")
        empty = os.path.join(tmp, "empty")
        os.makedirs(empty)
        _s = lrn.summary(empty, date(2026, 8, 15))
        check("无 claims/shadow 文件时 summary 不崩且为零",
              _s["n_claims"] == 0 and _s["shadow_tracked"] == 0 and not _s["overdue"])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # --- preflight W6 接线检出力：逾期主张必须升级为硬 escalation（守卫要证明会咬人）---
    import preflight as pf
    _orig_load = lrn.load_claims
    try:
        lrn.load_claims = lambda root: [_mk("T-wired", adjudicate_on="2026-08-01")]
        _rep = pf.run(datetime(2026, 8, 15, 12, 0, tzinfo=mc.UTC))
        check("preflight：逾期未裁定主张 -> 硬升级 UNADJUDICATED_CLAIMS 且 ok=False",
              "UNADJUDICATED_CLAIMS" in _rep["escalations"] and _rep["ok"] is False,
              str(_rep["escalations"]))
        lrn.load_claims = lambda root: []
        _rep2 = pf.run(datetime(2026, 8, 15, 12, 0, tzinfo=mc.UTC))
        check("preflight：无逾期 -> 不产生 UNADJUDICATED_CLAIMS",
              "UNADJUDICATED_CLAIMS" not in _rep2["escalations"], str(_rep2["escalations"]))
        # B1 接线检出力：W6 已注入交易日历——周五到期的主张在周日不得误升级
        lrn.load_claims = lambda root: [_mk("T-weekend", adjudicate_on="2026-08-14")]
        _rep_wk = pf.run(datetime(2026, 8, 16, 12, 0, tzinfo=mc.UTC))   # 2026-08-16 = 周日
        check("preflight W6 注入交易日历：周五到期在周日不误升级（B1 可用性回归封堵）",
              "UNADJUDICATED_CLAIMS" not in _rep_wk["escalations"],
              str(_rep_wk["escalations"]))
        check("preflight：report 带 learning 汇总键",
              set(["n_claims", "due_today", "overdue", "replacement", "all"])
              <= set(_rep2.get("learning", {})), str(_rep2.get("learning")))
    finally:
        lrn.load_claims = _orig_load

    # --- preflight W8 检出力（2026-08-15 审计补齐：「统计充分且命中率<50%」的
    #     落黄分支在生产可达，却从未被证明真的会落黄）---
    _w8_claims = [lrn.adjudicate(_mk("T-w8-%d" % i), "1" if i < 8 else "-1", "2026-08-14")
                  for i in range(20)]      # 8 HIT / 12 MISS -> 40% < 50%
    _sc_w8 = lrn.scorecard(_w8_claims, lrn.KIND_REPLACEMENT)
    check("W8 根据：20 裁定 8 中 -> sufficient=True 且命中率 40% < 50%",
          _sc_w8["sufficient"] is True and _sc_w8["hit_rate_pct"] == D("40"),
          str(_sc_w8))
    try:
        lrn.load_claims = lambda root: _w8_claims
        _rep_w8 = pf.run(datetime(2026, 8, 15, 12, 0, tzinfo=mc.UTC))
        _w8_lines = [c for c in _rep_w8["checks"] if "W8" in c]
        check("preflight W8：充分样本且命中率<50% -> [WARN] 落黄（检出力）",
              len(_w8_lines) == 1 and _w8_lines[0].startswith("[WARN]"),
              str(_w8_lines))
        check("W8 是 WARN 级：落黄可见但不进 escalations（判定不能≠失败的对偶）",
              not any("W8" in e for e in _rep_w8["escalations"]),
              str(_rep_w8["escalations"]))
    finally:
        lrn.load_claims = _orig_load

    # --- 实文件：8/05–8/14 五次替换的遡及登记（data/claims.jsonl / shadow-book.jsonl）---
    _root = os.path.abspath(os.path.join(HERE_DIR, ".."))
    _claims = lrn.load_claims(_root)
    _ids = [c["claim_id"] for c in _claims]
    # 不变式（2026-08-15 修订）：claims 分两类——替换类(RPL, 与影子帐簿一一对应) 与
    # 口座/规则类(kind=rule, 无影子帐簿, 检验能动运用本身对 SPY 是否有价值)。
    # 断言按「类别」而非「总数」写，未来新增 claim 不应机械性地打破此测。
    _rpl = [c for c in _claims if c["kind"] == lrn.KIND_REPLACEMENT]
    _rpl_ids = [c["claim_id"] for c in _rpl]
    check("claim_id 全部唯一", len(set(_ids)) == len(_ids), str(_ids))
    check("替换类 claim 恰有 5 条（8/05–8/14 五次替换遡及登记）",
          len(_rpl) == 5, str(_rpl_ids))
    check("替换类 claim_id 命名遵循 RPL-<交易日>-<卖>-<买>",
          set(_rpl_ids) == {"RPL-2026-08-05-RMBS-MSFT", "RPL-2026-08-07-BE-NVDA",
                            "RPL-2026-08-10-GEV-LLY", "RPL-2026-08-11-NVDA-LNG",
                            "RPL-2026-08-14-LLY-TSM"}, str(_rpl_ids))
    check("替换类全部 OPEN（60 交易日后才裁定，不得预判）",
          all(c["status"] == lrn.OPEN for c in _rpl))
    check("替换类全部 kind=replacement / 60 交易日 / 相对收益>0",
          all(c["horizon_sessions"] == 60
              and c["direction"] == ">" and D(c["threshold"]) == 0 for c in _rpl))

    def _sessions_after(d0, n):
        d, cnt = d0, 0
        while cnt < n:
            d += timedelta(days=1)
            if CAL.is_trading_day(d):
                cnt += 1
        return d
    for c in _claims:      # 裁定日=交易日历推导，对所有 claim（含口座类）都成立
        _d0 = datetime.strptime(c["made_on"], "%Y-%m-%d").date()
        _due = _sessions_after(_d0, c["horizon_sessions"])
        check("%s 裁定日 %s = made_on+%d 交易日（日历推导，非手写）"
              % (c["claim_id"], c["adjudicate_on"], c["horizon_sessions"]),
              c["adjudicate_on"] == _due.isoformat(), "expected %s" % _due)
    check("遡及登记今日（2026-08-15）无一逾期（W6 不误伤）",
          not lrn.overdue_claims(_claims, date(2026, 8, 15)))

    # 口座级最上位 claim：检验能动运用本身是否跑赢 SPY（究极目标＝利益，非系统指标）。
    _port = [c for c in _claims if c["claim_id"] == "PORT-2026-08-14-vs-SPY"]
    check("口座级 claim 存在（能动运用 vs SPY 的最上位可证伪预测）", len(_port) == 1, str(_ids))
    if _port:
        _p = _port[0]
        check("口座级 claim: kind=rule / metric=对SPY超额 / >0 / OPEN / 有裁定日",
              _p["kind"] == lrn.KIND_RULE
              and _p["metric"] == "portfolio_excess_return_pct_vs_SPY"
              and _p["direction"] == ">" and D(_p["threshold"]) == 0
              and _p["status"] == lrn.OPEN and bool(_p["adjudicate_on"]),
              str(_p))

    _shadow = lrn.load_shadow(_root)
    # 影子帐簿只对应替换类 claim（口座/规则类不建仓，无影子）。
    check("影子帐簿与替换类 claim 一一对应（卖出标的继续被定价）",
          len(_shadow) == len(_rpl) and
          {(e["symbol"], e["replaced_by"]) for e in _shadow}
          == {(c["baseline"], c["subject"]) for c in _rpl})
    check("影子帐簿每条都带替换入场价（否则 delta 不可算）",
          all(e["replacement_entry_price"] for e in _shadow))

    # --- 教训登记实文件：25 条全部声明、CODIFIED 必须指向 selftest 里真实存在的断言 ---
    _reg_path = os.path.join(_root, "knowledge", "lesson-status.json")
    with open(_reg_path, encoding="utf-8") as f:
        _reg_real = _json.load(f)
    import re as _re
    with open(os.path.join(_root, "knowledge", "lessons.md"), encoding="utf-8") as f:
        _lids = sorted(set(_re.findall(r"\*\*(L-\d{3}) ·", f.read())))
    check("lessons.md 提取到 25 条教训（L-001..L-025）",
          len(_lids) == 25 and _lids[0] == "L-001" and _lids[-1] == "L-025", str(_lids))
    _enf_real = lrn.lesson_enforcement(_reg_real, _lids)
    check("实登记：25 条无一未声明（W7 当前必须绿）",
          _enf_real["ok"] is True and _enf_real["total"] == 25, str(_enf_real["undeclared"]))
    with open(os.path.abspath(__file__), encoding="utf-8") as f:
        _self_src = f.read()
    for lid, rec in sorted(_reg_real.items()):
        if lid.startswith("L-") and rec.get("status") == "CODIFIED":
            check("%s 声称的测试断言真实存在于 selftest（防虚报 CODIFIED）" % lid,
                  rec["test"].split("（")[0].strip() in _self_src, rec["test"])


def test_orphan_replacement():
    print("\n[learning] 替换↔claim 即时强制 ORPHAN_REPLACEMENT（L-020 根穴恒久封堵，2026-08-15）")
    import learning as lrn
    import preflight as pf
    # 最小账本成交解析：只认 trade_id 行；表头/分隔线/持仓表/散文全部忽略
    toy = (
        "## Trade history\n"
        "| trade_id | trade_date | symbol | action |\n"
        "|---|---|---|---|\n"
        "| 2026-08-05-AAA-平仓-01 | 2026-08-05 | AAA | 平仓 |\n"
        "| 2026-08-05-BBB-建仓-01 | 2026-08-05 | BBB | 建仓 |\n"
        "| 2026-08-06-CCC-止盈减仓50-01 | 2026-08-06 | CCC | 止盈-减仓50% |\n"
        "| 2026-08-07-DDD-平仓-01 | 2026-08-07 | DDD | 平仓 |\n")
    trades = lrn.parse_ledger_trades(toy)
    check("最小解析：4 条成交全部提取（表头/分隔线被忽略）", len(trades) == 4, str(trades))
    pairs = lrn.replacement_pairs(trades)
    check("替换对识别：同日 平仓+建仓 恰为 1 对（AAA→BBB）",
          [p["claim_id"] for p in pairs] == ["RPL-2026-08-05-AAA-BBB"], str(pairs))
    check("减仓与孤立平仓不构成替换（不误伤）",
          all(p["date"] not in ("2026-08-06", "2026-08-07") for p in pairs))
    # (a) 合成孤儿：替换对无对应 claim -> 必须被检出
    check("ORPHAN_REPLACEMENT 合成孤儿对必须被检出",
          lrn.orphan_replacements(trades, []) == ["RPL-2026-08-05-AAA-BBB"],
          str(lrn.orphan_replacements(trades, [])))
    check("claim 齐备 -> 无孤儿",
          lrn.orphan_replacements(trades, ["RPL-2026-08-05-AAA-BBB"]) == [])
    # --- B3 检出力（2026-08-15 审计）：配对必须锚定替换标记，素的平仓不得误配 ---
    # 修复前：同日的无关「平仓」（规则性主动退出）＋别标的「建仓」被无条件配成替换对，
    # 向不存在的 claim 要求登记 -> ERROR 误阻断（可用性回归）。marker 化后封堵。
    toy_b3 = (
        "## CLOSED positions\n"
        "| AAA | CLOSED | 2026-08-01 | 2026-08-05 | **确定性替换退出（trade "
        "2026-08-05-AAA-平仓-01，MORNING 执行）**：卖最弱、买候选 |\n"
        "## Trade history\n"
        "| trade_id | trade_date | symbol | action |\n"
        "|---|---|---|---|\n"
        "| 2026-08-05-AAA-平仓-01 | 2026-08-05 | AAA | 平仓 |\n"
        "| 2026-08-05-BBB-建仓-01 | 2026-08-05 | BBB | 建仓 |\n"
        "| 2026-08-20-XXX-平仓-01 | 2026-08-20 | XXX | 平仓 |\n"
        "| 2026-08-20-YYY-建仓-01 | 2026-08-20 | YYY | 建仓 |\n")
    _markers = lrn.parse_replacement_markers(toy_b3)
    check("(B3) 替换标记解析：恰捕捉带标记的 AAA 平仓一条",
          _markers == ["2026-08-05-AAA-平仓-01"], str(_markers))
    _trades_b3 = lrn.parse_ledger_trades(toy_b3)
    _pairs_b3 = lrn.replacement_pairs(_trades_b3, replacement_close_ids=_markers)
    check("(B3) 无标记的素の平仓+同日无关建仓**不成对**（XXX/YYY 不被误配）",
          [p["claim_id"] for p in _pairs_b3] == ["RPL-2026-08-05-AAA-BBB"],
          str(_pairs_b3))
    check("(B3) marker 口径下无孤儿（不向不存在的 claim 要求登记 = 不误阻断）",
          lrn.orphan_replacements(_trades_b3, ["RPL-2026-08-05-AAA-BBB"],
                                  replacement_close_ids=_markers) == [],
          str(lrn.orphan_replacements(_trades_b3, ["RPL-2026-08-05-AAA-BBB"],
                                      replacement_close_ids=_markers)))
    check("(B3) 带标记的替换对缺 claim 仍必须响（检出力不因 marker 化而丢）",
          lrn.orphan_replacements(_trades_b3, [], replacement_close_ids=_markers)
          == ["RPL-2026-08-05-AAA-BBB"])
    # preflight 接线检出力：现实账本 5 对替换在 claims 被清空时必须全部响
    _orig = lrn.load_claims
    try:
        lrn.load_claims = lambda root: []
        rep = pf.run(datetime(2026, 8, 15, 12, 0, tzinfo=mc.UTC))
        check("preflight：替换对缺 claim -> 硬升级 ORPHAN_REPLACEMENT 且 ok=False",
              "ORPHAN_REPLACEMENT" in rep["escalations"] and rep["ok"] is False,
              str(rep["escalations"]))
    finally:
        lrn.load_claims = _orig
    # (b) 现实数据：实账本 + 实 claims.jsonl 必须无孤儿（5 对替换已遡及登记）。
    #     若此处变红 = 真实的登记漏，须人工补登 claim，绝不得删检查。
    _root = os.path.abspath(os.path.join(HERE_DIR, ".."))
    with open(os.path.join(_root, "portfolio-ledger.md"), encoding="utf-8") as f:
        _real_text = f.read()
    real_trades = lrn.parse_ledger_trades(_real_text)
    real_markers = lrn.parse_replacement_markers(_real_text)
    check("现实账本替换标记恰 5 条（CLOSED note「确定性替换退出（trade …」全部被捕捉）",
          real_markers == [
              "2026-08-05-RMBS-平仓-01", "2026-08-07-BE-平仓-01",
              "2026-08-10-GEV-平仓-01", "2026-08-11-NVDA-平仓-01",
              "2026-08-14-LLY-平仓-01"],
          str(real_markers))
    real_pairs = lrn.replacement_pairs(real_trades, replacement_close_ids=real_markers)
    check("现实账本恰识别出 5 对替换（8/05,8/07,8/10,8/11,8/14，marker 口径）",
          [p["claim_id"] for p in real_pairs] == [
              "RPL-2026-08-05-RMBS-MSFT", "RPL-2026-08-07-BE-NVDA",
              "RPL-2026-08-10-GEV-LLY", "RPL-2026-08-11-NVDA-LNG",
              "RPL-2026-08-14-LLY-TSM"],
          str([p["claim_id"] for p in real_pairs]))
    real_ids = [c["claim_id"] for c in lrn.load_claims(_root)]
    check("ORPHAN_REPLACEMENT 现实账本+现实 claims 无孤儿（当前必须绿）",
          lrn.orphan_replacements(real_trades, real_ids,
                                  replacement_close_ids=real_markers) == [],
          str(lrn.orphan_replacements(real_trades, real_ids,
                                      replacement_close_ids=real_markers)))


def test_price_convention():
    print("\n[price] 価格口径（狭スコープ）：T-20min価は CLOSING約定フィル価格＋保有成本のみ、それ以外は公式收盘（2026-08-17 用户裁定＝過剰統一 G-PRICE の巻き戻し）")
    _root = os.path.abspath(os.path.join(HERE_DIR, ".."))

    def _read(*parts):
        with open(os.path.join(_root, *parts), encoding="utf-8") as f:
            return f.read()

    def _section(text, start_marker, end_marker):
        i = text.find(start_marker)
        j = text.find(end_marker, i + 1) if i >= 0 else -1
        return text[i:j] if i >= 0 and j >= 0 else (text[i:] if i >= 0 else "")

    _les = _read("knowledge", "lessons.md")
    _sys = _read("SYSTEM.md")
    _src_md = _read("data", "sources.md")
    _pb = _read("strategy-playbook.md")
    _alert = _read("alert-state.md")
    _integ = _read("lib", "integrity.py")
    _l004 = _section(_les, "**L-004 ·", "**L-005 ·")
    _l021 = _section(_les, "**L-021 ·", "**L-022 ·")

    # --- (a) 残す狭い1点：CLOSING約定フィル価格＝T-20min価（保有成本もこれに由来）が SYSTEM/SKILL に明记 ---
    check("(a) SYSTEM.md：CLOSING約定フィル価格＝T-20min価（保有成本もこれに由来）が明记",
          ("約定フィル" in _sys and "T-20min" in _sys and "保有成本" in _sys))
    _skill_p = os.path.join(_root, "..", "Scheduled", "us-market-system", "SKILL.md")
    check("(a0) SKILL.md 存在（外部手順書、口径同期の対象）", os.path.exists(_skill_p), _skill_p)
    if os.path.exists(_skill_p):
        _skill = _read("..", "Scheduled", "us-market-system", "SKILL.md")
        check("(a1) SKILL CLOSING：約定フィル価格のみ T-20min価と明记",
              ("約定フィル" in _skill and "T-20min" in _skill),
              "約定フィル=%s T-20min=%s" % ("約定フィル" in _skill, "T-20min" in _skill))
        # POST_CLOSE は公式收盘で valuation/結算（読み取り専用への縮小は撤回）
        check("(c1) SKILL POST_CLOSE：公式收盘で valuation/結算（読み取り専用でない）",
              ("結算" in _skill and "公式收盘" in _skill and "読み取り専用" not in _skill),
              "結算=%s 公式收盘=%s 読み取り専用残存=%s"
              % ("結算" in _skill, "公式收盘" in _skill, "読み取り専用" in _skill))

    # --- (b) 離場判定 ACT-002/003 は公式收盘（収盘确认）に戻っている（T-20min不在） ---
    check("(b) SYSTEM.md：離場は収盘确认（公式收盘）で「T-20min価 < X」不残存",
          ("收盘确认" in _sys and "T-20min価 < X" not in _sys),
          "收盘确认=%s / T-20min価 < X 残存=%s"
          % ("收盘确认" in _sys, "T-20min価 < X" in _sys))
    check("(b1) strategy-playbook：ACT-002/003 離場は official close（T-20min 完全不在）",
          ("official close" in _pb and "T-20min" not in _pb),
          "official close=%s / playbook T-20min 残存=%s"
          % ("official close" in _pb, "T-20min" in _pb))
    check("(b2) alert-state：離場判据は公式收盘口径（T-20min 框注不在）",
          "T-20min" not in _alert, "alert T-20min 残存=%s" % ("T-20min" in _alert))

    # --- (c) POST_CLOSE は公式收盘で valuation/結算（SYSTEM §4.3；読み取り専用への縮小は撤回）---
    _pc_line = _section(_sys, "- **POST_CLOSE ＝公式收盘", "- **阶段边界总账")
    check("(c) SYSTEM.md §4.3：POST_CLOSE は公式收盘で valuation/結算（読み取り専用でない）",
          ("公式收盘" in _pc_line and "結算" in _pc_line), _pc_line[:60])
    # valuation 入力＝公式收盘（C1 注記が T-20min に戻っていない）
    check("(c2) lib/integrity.py：valuation 入力＝公式收盘价（T-20min は valuation に用いない）",
          ("公式收盘价" in _integ and "valuation には用いない" in _integ))

    # --- (d) L-004/L-021 の例外が「約定フィル限定」に狭められている ---
    check("(d) lessons L-004：例外が約定フィル限定・分析/評価/離場は公式收盘",
          ("約定フィル" in _l004 and "公式收盘" in _l004 and "T-20min" in _l004))
    check("(d1) lessons L-021：例外が約定フィル限定・評価/検証は公式收盘（定稿値必須）",
          ("約定フィル" in _l021 and "公式收盘" in _l021))
    # 安全意図（≥2源）が保持されている（改訂であって撤回でない証明）
    check("(d2) L-004 が≥2源の安全要件を保持",
          ("≥2" in _l004 or "2 核准源" in _l004 or "2核准源" in _l004), _l004[:80])

    # --- (e) sources.md：closing_window_price は登録維持だが CLOSING約定フィル専用に限定 ---
    check("(e) sources.md：closing_window_price 登録維持＋CLOSING約定フィル専用に限定",
          ("closing_window_price" in _src_md and "約定フィル" in _src_md
           and "用いない" in _src_md))
    _cwp = ig.approved_for("closing_window_price")
    check("(e2) closing_window_price に ≥2 核准源（約定フィル価格 P1 可満足性）",
          len(_cwp) >= 2, "只有 %d 个" % len(_cwp))
    check("(e3) closing_window_price 源は黑名单と無交集（P2 不破坏）",
          not (set(_cwp) & set(ig.BAD_SOURCES)), str(set(_cwp) & set(ig.BAD_SOURCES)))


def test_gap_ledger():
    print("\n== gap 台账覆盖检查（防「书面对策」再度腐化，W7 同思想）==")
    import re as _re
    p = os.path.join(HERE_DIR, "..", "knowledge", "gap-ledger.md")
    check("knowledge/gap-ledger.md 存在", os.path.exists(p), p)
    if not os.path.exists(p):
        return
    with open(p, encoding="utf-8") as f:
        txt = f.read()
    STATES = ("ENFORCED", "CODIFIABLE_PENDING", "INHERENTLY_MANUAL")
    rows = []
    for line in txt.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0] in ("编号", "") or set(cells[0]) <= set("-: "):
            continue
        rows.append((line, cells))
    check("台账至少 25 行（三次审计的 gap 全量收录）", len(rows) >= 25,
          "rows=%d" % len(rows))
    bad_state = [c[0] for line, c in rows if sum(1 for s in STATES if s in line) != 1]
    check("每行恰有三态之一（ENFORCED/CODIFIABLE_PENDING/INHERENTLY_MANUAL）",
          not bad_state, str(bad_state))
    with open(os.path.abspath(__file__), encoding="utf-8") as f:
        _src = f.read()
    enforced = [(line, cells) for line, cells in rows if "ENFORCED" in line]
    check("ENFORCED 行 >= 8（本次实装的守卫全部挙证）", len(enforced) >= 8,
          "enforced=%d" % len(enforced))
    for line, cells in enforced:
        names = _re.findall(r"`([^`]+)`", line)
        check("ENFORCED 行 %s 挙证测试名非空（虚报防止）" % cells[0], bool(names), line)
        for nm in names:
            check("ENFORCED 主张的测试 %r 真实存在于 selftest（W7 同思想）" % nm,
                  nm in _src, nm)


def main():
    print("=" * 70)
    print("us-market-system 自检 —— 可执行规范")
    print("=" * 70)
    for fn in (test_routing, test_schedule_alignment, test_closing_window,
               test_regime, test_slots,
               test_accounting, test_staleness, test_provenance, test_outbox,
               test_report_lint, test_quote_extract, test_knowledge,
               test_high_availability, test_queue_watchdog, test_data_layer,
               test_selection, test_backtest, test_learning,
               test_orphan_replacement, test_price_convention, test_gap_ledger):
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
