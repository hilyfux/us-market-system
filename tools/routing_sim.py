#!/usr/bin/env python3
"""
routing_sim.py — us-market-system 阶段路由仿真 / 调度覆盖率审计

用途：不触碰任何真实状态，纯逻辑仿真。
  1) 按 SYSTEM.md 规则实现阶段判定，用合成时间戳穷举（含夏/冬令时、周末、假日、13:00 早收盘）
  2) 把「注册的 cron 实际触发时刻」映射到阶段窗口，量化哪些阶段打不中
运行：python3 routing_sim.py
"""
from datetime import datetime, timedelta, time as dtime
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")
SGT = ZoneInfo("Asia/Singapore")
UTC = ZoneInfo("UTC")

# ---- 交易日历（测试夹具；真实运行必须向交易所核实，见 SYSTEM.md ACT-001）----
HOLIDAYS_2026 = {  # 全日休市
    "2026-01-01", "2026-01-19", "2026-02-16", "2026-04-03", "2026-05-25",
    "2026-06-19", "2026-07-03", "2026-09-07", "2026-11-26", "2026-12-25",
}
EARLY_CLOSE_2026 = {"2026-11-27": dtime(13, 0), "2026-12-24": dtime(13, 0)}


def session(et_dt):
    """返回 (是否交易日, 开盘时间, 收盘时间)。收盘兼容 13:00 早收盘，不硬编码 16:00。"""
    d = et_dt.strftime("%Y-%m-%d")
    if et_dt.weekday() >= 5 or d in HOLIDAYS_2026:
        return False, None, None
    return True, dtime(9, 30), EARLY_CLOSE_2026.get(d, dtime(16, 0))


def route(et_dt):
    """阶段路由，优先级与 SKILL.md 一致：MORNING > POST_CLOSE > INTRADAY > PREMARKET。"""
    utc_dt = et_dt.astimezone(UTC)
    # MORNING：UTC 00:30–00:59 触发窗口（SGT 约 08:30）
    if utc_dt.hour == 0 and 30 <= utc_dt.minute <= 59:
        return "MORNING"

    is_td, open_t, close_t = session(et_dt)
    if not is_td:
        return "NO_ACTIVE_STAGE"

    close_dt = et_dt.replace(hour=close_t.hour, minute=close_t.minute, second=0, microsecond=0)
    open_dt = et_dt.replace(hour=open_t.hour, minute=open_t.minute, second=0, microsecond=0)

    # POST_CLOSE：实际收盘后约 20–60 分钟
    delta_min = (et_dt - close_dt).total_seconds() / 60
    if 20 <= delta_min <= 60:
        return "POST_CLOSE"

    # INTRADAY：连续交易中，且只在 :00 / :30 检查点
    if open_dt <= et_dt < close_dt and et_dt.minute in (0, 30):
        return "INTRADAY"

    # PREMARKET：ET 08:30–09:29 且未开盘
    if dtime(8, 30) <= et_dt.time() < dtime(9, 30):
        return "PREMARKET"

    return "NO_ACTIVE_STAGE"


def fire_times(cron_minutes, cron_hours, day_sgt):
    """给定 cron 的 (分钟集合, 小时集合)，返回该 SGT 日的所有触发时刻（转成 ET）。"""
    out = []
    for h in sorted(cron_hours):
        for m in sorted(cron_minutes):
            sgt_dt = datetime.combine(day_sgt, dtime(h, m), tzinfo=SGT)
            out.append(sgt_dt.astimezone(ET))
    return out


def coverage(cron_minutes, cron_hours, label, days):
    """统计该 cron 在给定日期集合上，各阶段被命中的次数。"""
    hits = {}
    for d in days:
        for et_dt in fire_times(cron_minutes, cron_hours, d):
            hits.setdefault(route(et_dt), 0)
            hits[route(et_dt)] += 1
    print(f"\n--- {label} ---")
    for stage in ("MORNING", "PREMARKET", "INTRADAY", "POST_CLOSE", "NO_ACTIVE_STAGE"):
        n = hits.get(stage, 0)
        mark = "  ** NEVER FIRES **" if n == 0 and stage != "NO_ACTIVE_STAGE" else ""
        print(f"  {stage:<16} {n:>4}{mark}")
    return hits


def main():
    print("=" * 68)
    print("PART 1 — 阶段路由正确性（合成时间戳）")
    print("=" * 68)
    cases = [
        # (ET 时间戳, 期望阶段, 说明)
        ("2026-07-27 08:30", "PREMARKET", "夏令时 盘前窗口起点"),
        ("2026-07-27 09:29", "PREMARKET", "盘前窗口末点"),
        ("2026-07-27 09:30", "INTRADAY", "开盘首个检查点"),
        ("2026-07-27 12:00", "INTRADAY", "盘中整点"),
        ("2026-07-27 12:30", "INTRADAY", "盘中半点"),
        ("2026-07-27 12:15", "NO_ACTIVE_STAGE", "非 :00/:30 → 不应运行"),
        ("2026-07-27 15:30", "INTRADAY", "收盘前最后检查点"),
        ("2026-07-27 16:00", "NO_ACTIVE_STAGE", "正好收盘，尚未到结算窗口"),
        ("2026-07-27 16:30", "POST_CLOSE", "收盘 +30min"),
        ("2026-07-27 17:00", "POST_CLOSE", "收盘 +60min 边界"),
        ("2026-07-27 17:01", "NO_ACTIVE_STAGE", "超出结算窗口"),
        ("2026-01-05 16:30", "POST_CLOSE", "冬令时 结算（EST）"),
        ("2026-01-05 09:30", "INTRADAY", "冬令时 开盘"),
        ("2026-11-27 13:30", "POST_CLOSE", "早收盘日 13:00 → 13:30 结算"),
        ("2026-11-27 15:30", "NO_ACTIVE_STAGE", "早收盘日已收盘，不得当盘中"),
        ("2026-11-27 12:30", "INTRADAY", "早收盘日 收盘前仍是盘中"),
        ("2026-07-25 10:00", "NO_ACTIVE_STAGE", "周六"),
        ("2026-07-26 16:30", "NO_ACTIVE_STAGE", "周日"),
        ("2026-07-03 12:00", "NO_ACTIVE_STAGE", "独立日观察日 全日休市"),
        ("2026-12-25 12:00", "NO_ACTIVE_STAGE", "圣诞 休市"),
    ]
    passed = failed = 0
    for ts, expect, note in cases:
        et_dt = datetime.strptime(ts, "%Y-%m-%d %H:%M").replace(tzinfo=ET)
        got = route(et_dt)
        ok = got == expect
        passed, failed = (passed + 1, failed) if ok else (passed, failed + 1)
        print(f"  [{'PASS' if ok else 'FAIL'}] {ts} ET  ->{got:>17}   ({note})")
        if not ok:
            print(f"         expected {expect}")
    print(f"\n  routing: {passed} passed, {failed} failed")

    # MORNING 单独验证（由 UTC 窗口决定）
    print("\n  MORNING 窗口（UTC 00:30-00:59 == SGT 08:30-08:59）:")
    for hhmm in ("08:00", "08:29", "08:30", "08:45", "08:59", "09:00"):
        sgt_dt = datetime.strptime("2026-07-27 " + hhmm, "%Y-%m-%d %H:%M").replace(tzinfo=SGT)
        print(f"    SGT {hhmm} (UTC {sgt_dt.astimezone(UTC):%H:%M}) -> {route(sgt_dt.astimezone(ET))}")

    print("\n" + "=" * 68)
    print("PART 2 — 调度覆盖率：注册的 cron vs 总纲要求的 cron")
    print("=" * 68)
    # 一整个工作周（SGT 日）
    days = [datetime(2026, 7, 27).date() + timedelta(days=i) for i in range(5)]
    print(f"样本：SGT {days[0]} .. {days[-1]}（5 个交易日）")

    actual = coverage({0}, set(range(24)), "实际注册: 0 * * * *（每小时 :00）", days)
    spec = coverage({0, 30}, {0, 1, 2, 3, 4, 5, 8, 20, 21, 22, 23},
                    "总纲要求: 0,30 0-5,8,20-23 * * *", days)

    print("\n--- 差异结论 ---")
    for stage in ("MORNING", "PREMARKET", "INTRADAY", "POST_CLOSE"):
        a, s = actual.get(stage, 0), spec.get(stage, 0)
        verdict = "一致" if a == s else ("**实际打不中**" if a == 0 else f"覆盖不足 {a}/{s}")
        print(f"  {stage:<12} 实际 {a:>3}  应有 {s:>3}   {verdict}")
    print(f"\n  实际每周触发 {5*24} 次，其中无效心跳 {actual.get('NO_ACTIVE_STAGE',0)} 次"
          f"（{actual.get('NO_ACTIVE_STAGE',0)/(5*24)*100:.0f}% 空跑）")


if __name__ == "__main__":
    main()
