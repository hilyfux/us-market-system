#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
market_core — 交易日历、阶段路由、调度对齐校验、市场环境分类、槽位会计

设计原则
  1. 单一实现源：阶段判定只有这一份代码。SYSTEM.md 只写策略，不再复述机制。
  2. 窗口各自声明时区：MORNING 属于 SGT（用户早晨），PREMARKET/INTRADAY/POST_CLOSE
     属于 ET（交易所相对）。不强行统一，而是由一个函数集中换算。
  3. 调度可证明：verify_schedule_alignment() 会证明给定 cron 能命中每个阶段并留有
     jitter 余量。**归因订正（2026-08-15 用户裁定）**：2026-07 那 6 个交易日的停摆，
     **实因是 PC（硬件）更换，与 cron 无关**，勿再混为一谈。本层校验针对的是**另一个
     独立且真实存在**的调度整列缺陷——`0 * * * *` 使 MORNING 永不触发、POST_CLOSE 仅落在
     +60min 边界被 jitter 挤出窗口——这缺陷该修（已修），但它不是那 6 天停摆的原因。
  4. 分类器确定化：市场环境不再靠判断，由 classify_regime() 按阈值推导，可复现。

兼容性：目标 Python 3.9（launchd 下实际解释器为 CommandLineTools python3 3.9.6），
不使用 3.10+ 语法。
"""
from datetime import datetime, date, timedelta, time as dtime
from zoneinfo import ZoneInfo
from typing import Dict, List, Optional, Tuple, Set

ET = ZoneInfo("America/New_York")
SGT = ZoneInfo("Asia/Singapore")
UTC = ZoneInfo("UTC")

REGULAR_OPEN = dtime(9, 30)
REGULAR_CLOSE = dtime(16, 0)
EARLY_CLOSE = dtime(13, 0)

# 结算窗口：实际收盘后 N 分钟。放宽到 20–75（原 20–60），
# 理由：60 分钟上界使唯一候选点恰好落在边界上，任何 jitter 都会越界。
POST_CLOSE_MIN_MIN = 20
POST_CLOSE_MAX_MIN = 75

# 收盘执行窗（CLOSING）：引け 20 分前 <= et < 引け。in-session の唯一取引執行フェーズ。
# 引け時刻は日历（TradingCalendar.close_time）から取得し、16:00 をハードコードしない
# （早收盘日 13:00 → 窓 12:40–13:00、ACT-001）。九维再評価・替換判定・MOC 確定はここで行い、
# 約定は同日の**検証済み公式引け値**で記帳する（記帳口径は従来通り、決定/約定の時点だけ現実化）。
CLOSING_LEAD_MIN = 20

PREMARKET_START = dtime(8, 30)   # ET
MORNING_START = dtime(8, 30)     # SGT
MORNING_END = dtime(8, 59)       # SGT

VALID_CHECKPOINT_MINUTES = (0, 30)

# 检查点宽限窗口（分钟）。
# 实测每次调度实际启动比计划晚 87–137 秒（见 system-state 的 scheduled_checkpoint
# 与 actual_start 对比），因此 ET 分钟数永远是 :31/:01 而非 :00/:30。
# 若严格要求 minute in (0,30)，全部盘中运行都会被判为无阶段 —— 旧散文规范之所以
# "能跑"，只是因为 LLM 宽松地把 09:31:48 归到了 0930 检查点。
# 这里把该宽松行为固化为显式规则：运行时刻落在检查点后 GRACE 分钟内，归属该检查点，
# report_key 使用吸附后的检查点，从而天然幂等（同一宽限窗内重复运行不会重复推送）。
CHECKPOINT_GRACE_MIN = 10

# STAGES = ライブ REQUIRED_CRON が「各阶段到達可能」を保証すべき集合。
# verify_schedule_alignment() はこの集合に対して到達性/脆弱性を判定する。
# CLOSING（收盘执行窗）は route() が返す独立ステージだが、**この集合にはまだ含めない**：
# 現行ライブ cron は :00/:30 のみで引け20分前の CLOSING 窓に発火しない＝到達不能が正常（Phase 1）。
# Phase 2 で OS 定時タスク＋REQUIRED_CRON を同時に変えて CLOSING を編入し、その時に本集合へ加える。
STAGES = ("MORNING", "PREMARKET", "INTRADAY", "POST_CLOSE", "CLOSING")
CLOSING_STAGE = "CLOSING"
NO_STAGE = "NO_ACTIVE_STAGE"


# ---------------------------------------------------------------- 交易日历
class TradingCalendar:
    """
    交易日历。假日/早收盘为**事实数据**，必须显式提供或从 holidays.json 载入。
    刻意不内置猜测：日历错误会静默污染结算，宁可 raise。
    """

    def __init__(self, holidays: Set[str], early_closes: Dict[str, dtime]):
        self.holidays = set(holidays)
        self.early_closes = dict(early_closes)
        self._years = {int(d[:4]) for d in self.holidays}

    def covers(self, d: date) -> bool:
        return d.year in self._years

    def assert_covers(self, d: date) -> None:
        if not self.covers(d):
            raise CalendarCoverageError(
                "交易日历未覆盖 %d 年；必须补充该年度假日与早收盘数据后再运行，"
                "不得按 16:00 硬编码推断（SYSTEM.md ACT-001）。" % d.year
            )

    def is_trading_day(self, d: date) -> bool:
        self.assert_covers(d)
        return d.weekday() < 5 and d.isoformat() not in self.holidays

    def close_time(self, d: date) -> Optional[dtime]:
        if not self.is_trading_day(d):
            return None
        return self.early_closes.get(d.isoformat(), REGULAR_CLOSE)

    def is_early_close(self, d: date) -> bool:
        return d.isoformat() in self.early_closes

    def session(self, d: date) -> Optional[Tuple[dtime, dtime]]:
        if not self.is_trading_day(d):
            return None
        return REGULAR_OPEN, self.close_time(d)

    def prev_trading_day(self, d: date) -> date:
        c = d - timedelta(days=1)
        for _ in range(15):
            if self.is_trading_day(c):
                return c
            c -= timedelta(days=1)
        raise CalendarCoverageError("向前 15 天未找到交易日，日历数据可疑")

    def trading_days_between(self, start: date, end: date) -> int:
        """(start, end] 区间内的交易日数量。用于陈旧度断言。"""
        if end <= start:
            return 0
        n, c = 0, start + timedelta(days=1)
        while c <= end:
            if self.is_trading_day(c):
                n += 1
            c += timedelta(days=1)
        return n


class CalendarCoverageError(RuntimeError):
    pass


# ---------------------------------------------------------------- 阶段路由
def snap_to_checkpoint(et_dt: datetime) -> Optional[datetime]:
    """把实际运行时刻吸附到其所属的 :00/:30 检查点；超出宽限则返回 None。"""
    for cp_min in sorted(VALID_CHECKPOINT_MINUTES, reverse=True):
        cp = et_dt.replace(minute=cp_min, second=0, microsecond=0)
        if cp > et_dt:
            continue
        if (et_dt - cp).total_seconds() / 60.0 < CHECKPOINT_GRACE_MIN:
            return cp
    # 跨小时回看：例如 ET 10:03 属于 10:00；ET 10:05 也属于 10:00
    prev_hour = (et_dt - timedelta(hours=1)).replace(minute=30, second=0, microsecond=0)
    if 0 <= (et_dt - prev_hour).total_seconds() / 60.0 < CHECKPOINT_GRACE_MIN:
        return prev_hour
    return None


def route(now_utc: datetime, cal: TradingCalendar) -> Dict[str, object]:
    """
    返回 {stage, reason, et, sgt, session_close, minutes_after_close}
    优先级：MORNING > POST_CLOSE > INTRADAY > PREMARKET。
    入参必须是 aware datetime；naive 直接 raise（时区错误曾是本系统事故源）。
    """
    if now_utc.tzinfo is None:
        raise ValueError("route() 需要带时区的 datetime，拒绝 naive 输入")

    et = now_utc.astimezone(ET)
    sgt = now_utc.astimezone(SGT)
    out = {"stage": NO_STAGE, "reason": "", "et": et, "sgt": sgt,
           "session_close": None, "minutes_after_close": None, "checkpoint": None}

    # MORNING —— 以 SGT 声明（用户早晨），与交易所状态无关；休市日只生成只读晨报
    if MORNING_START <= sgt.time() <= MORNING_END:
        out["stage"] = "MORNING"
        out["reason"] = "SGT %s 落入晨间窗口 %s-%s" % (
            sgt.strftime("%H:%M"), MORNING_START.strftime("%H:%M"), MORNING_END.strftime("%H:%M"))
        return out

    d = et.date()
    if not cal.is_trading_day(d):
        out["reason"] = "ET %s 非交易日（周末或假日）" % d.isoformat()
        return out

    open_t, close_t = cal.session(d)
    open_dt = et.replace(hour=open_t.hour, minute=open_t.minute, second=0, microsecond=0)
    close_dt = et.replace(hour=close_t.hour, minute=close_t.minute, second=0, microsecond=0)
    after = (et - close_dt).total_seconds() / 60.0
    out["session_close"] = close_dt
    out["minutes_after_close"] = round(after, 2)

    if POST_CLOSE_MIN_MIN <= after <= POST_CLOSE_MAX_MIN:
        out["stage"] = "POST_CLOSE"
        out["reason"] = "实际收盘 %s 后 %.1f 分钟，落入结算窗口 %d-%d%s" % (
            close_t.strftime("%H:%M"), after, POST_CLOSE_MIN_MIN, POST_CLOSE_MAX_MIN,
            "（早收盘日）" if cal.is_early_close(d) else "")
        return out

    # CLOSING —— 收盘执行窗（引け 20 分前 <= et < 引け）。INTRADAY より**先に**切り出す：
    # CLOSING 窓は連続取引時間帯の部分集合なので、後回しにすると INTRADAY のチェックポイント
    # 吸附に飲まれる。設計：15:30 の :30 チェックポイントは INTRADAY のまま、15:40–15:59 が CLOSING。
    # 引け時刻は close_dt（日历由来）から算出＝早收盘日 13:00 は自動追従（窓 12:40–13:00）、16:00 非依存。
    closing_start_dt = close_dt - timedelta(minutes=CLOSING_LEAD_MIN)
    if closing_start_dt <= et < close_dt:
        out["stage"] = CLOSING_STAGE
        out["reason"] = "ET %s 落入收盘执行窗 %s-%s（引け %d 分前・in-session MOC 執行窓）%s" % (
            et.strftime("%H:%M:%S"), closing_start_dt.strftime("%H:%M"),
            close_t.strftime("%H:%M"), CLOSING_LEAD_MIN,
            "（早收盘日）" if cal.is_early_close(d) else "")
        return out

    if open_dt <= et < close_dt:
        cp = snap_to_checkpoint(et)
        if cp is not None:
            out["stage"] = "INTRADAY"
            out["checkpoint"] = cp.strftime("%H%M")
            out["reason"] = "连续交易中，ET %s 吸附到检查点 %s（宽限 %d 分钟内）" % (
                et.strftime("%H:%M:%S"), cp.strftime("%H:%M"), CHECKPOINT_GRACE_MIN)
        else:
            out["reason"] = "连续交易中但 ET %s 距最近 :00/:30 检查点已超 %d 分钟宽限" % (
                et.strftime("%H:%M"), CHECKPOINT_GRACE_MIN)
        return out

    if PREMARKET_START <= et.time() < open_t:
        out["stage"] = "PREMARKET"
        out["reason"] = "ET %s 在盘前窗口 %s-%s 内且未开盘" % (
            et.strftime("%H:%M"), PREMARKET_START.strftime("%H:%M"), open_t.strftime("%H:%M"))
        return out

    out["reason"] = "ET %s 不属于任何阶段窗口" % et.strftime("%H:%M")
    return out


# ------------------------------------------------- 调度对齐校验（防止再次停摆）
def cron_fire_times_utc(minutes: Set[int], hours: Set[int], day_sgt: date,
                        jitter_s: int, tz: ZoneInfo = SGT) -> List[datetime]:
    """把 cron(分钟集, 小时集) 在 tz 下某日的触发时刻展开为 UTC，并叠加 jitter。"""
    out = []
    for h in sorted(hours):
        for m in sorted(minutes):
            local = datetime.combine(day_sgt, dtime(h, m), tzinfo=tz) + timedelta(seconds=jitter_s)
            out.append(local.astimezone(UTC))
    return out


def verify_schedule_alignment(minutes: Set[int], hours: Set[int], cal: TradingCalendar,
                              sample_days: List[date], jitter_s: int = 60) -> Dict[str, object]:
    """
    证明给定 cron 能命中每个阶段，并给出最坏情况的 jitter 余量。

    对每个采样日，在 jitter=0 与 jitter=jitter_s 两种极端下分别路由；
    只有两种极端都命中，该阶段才算「稳健可达」——这正是 2026-07 事故的检出点：
    POST_CLOSE 在 jitter=0 时命中、jitter=47s 时越界，属于不稳健。
    """
    hits = {s: 0 for s in STAGES}
    robust = {s: 0 for s in STAGES}
    empty = 0
    margins = {s: [] for s in STAGES}
    fragile_detail = []
    # STAGES 外のステージ（現状 CLOSING）に発火が落ちても KeyError で落ちない兜底。
    # 到達性契約（unreachable/fragile）には数えないが、命中数は観測可能にする（可観測性）。
    # Phase 2 で CLOSING を STAGES に編入すれば、そのまま到達性判定の対象になる。
    other_hits = {}

    # 只在 jitter 实际可能取到的区间端点上求值：[0, jitter_s]。
    # 早期版本错误地探测了 nominal+60s（超出 jitter 上界），把「运行晚 1 分钟就
    # 跨出该分钟」误报为脆弱；真正的修法是检查点吸附，见 snap_to_checkpoint。
    for day in sample_days:
        for nominal in cron_fire_times_utc(minutes, hours, day, 0):
            s_lo = route(nominal, cal)
            s_hi = route(nominal + timedelta(seconds=jitter_s), cal)
            st = s_lo["stage"]
            if st == NO_STAGE:
                empty += 1
                continue
            if st not in hits:
                other_hits[st] = other_hits.get(st, 0) + 1
                continue
            hits[st] += 1
            if s_hi["stage"] == st:
                robust[st] += 1
            else:
                fragile_detail.append("%s: jitter 0s->%s 但 %ds->%s" % (
                    nominal.astimezone(ET).strftime("%m-%d %H:%M ET"), st, jitter_s, s_hi["stage"]))
            if st == "POST_CLOSE":
                for r in (s_lo, s_hi):
                    if r["minutes_after_close"] is not None:
                        margins[st].append(round(min(r["minutes_after_close"] - POST_CLOSE_MIN_MIN,
                                                     POST_CLOSE_MAX_MIN - r["minutes_after_close"]), 2))

    unreachable = [s for s in STAGES if hits[s] == 0]
    fragile = [s for s in STAGES if hits[s] > 0 and robust[s] < hits[s]]
    return {
        "hits": hits, "robust": robust, "empty_runs": empty, "other_hits": other_hits,
        "unreachable": unreachable, "fragile": fragile, "fragile_detail": fragile_detail[:5],
        "post_close_margin_min": min(margins["POST_CLOSE"]) if margins["POST_CLOSE"] else None,
        "ok": not unreachable and not fragile,
    }


# ------------------------------------------------------------ 市场环境分类
REGIME_CEILING = {"RISK_ON": 90, "CHOPPY": 75, "DEFENSIVE": 50, "STRESS": 0}


def classify_regime(vix: float, spy: float, spy_ma50: float, spy_ma200: float,
                    breadth_adv_dec: Optional[float] = None) -> Dict[str, object]:
    """
    确定性市场环境分类。ACT-004 的仓位上限由此推导，不再依赖主观判断。

    规则自上而下，首个命中者生效：
      STRESS    VIX>=30 或 SPY<200日线            -> 上限 0%
      DEFENSIVE VIX>=22 或 SPY<50日线             -> 上限 50%
      CHOPPY    VIX>=16 或 宽度<1.0               -> 上限 75%
      RISK_ON   其余                               -> 上限 90%
    阈值是策略参数，改这里即改全系统；任何改动都必须在 selftest 中补一条用例。
    """
    reasons = []
    if vix >= 30:
        reasons.append("VIX %.2f >= 30" % vix)
    if spy < spy_ma200:
        reasons.append("SPY %.2f 低于 200 日线 %.2f" % (spy, spy_ma200))
    if reasons:
        return {"regime": "STRESS", "ceiling_pct": 0, "reasons": reasons}

    if vix >= 22:
        reasons.append("VIX %.2f >= 22" % vix)
    if spy < spy_ma50:
        reasons.append("SPY %.2f 低于 50 日线 %.2f" % (spy, spy_ma50))
    if reasons:
        return {"regime": "DEFENSIVE", "ceiling_pct": 50, "reasons": reasons}

    if vix >= 16:
        reasons.append("VIX %.2f >= 16" % vix)
    if breadth_adv_dec is not None and breadth_adv_dec < 1.0:
        reasons.append("宽度 %.2f < 1.0" % breadth_adv_dec)
    if reasons:
        return {"regime": "CHOPPY", "ceiling_pct": 75, "reasons": reasons}

    return {"regime": "RISK_ON", "ceiling_pct": 90,
            "reasons": ["VIX %.2f < 16 且 SPY 在 50/200 日线之上" % vix]}


# ---------------------------------------------------------------- 槽位会计
def slot_report(positions: List[Dict[str, object]], slot_limit: int = 8) -> Dict[str, object]:
    """
    模拟风险预算（slot_limit）**只对模拟持仓计数**——模拟盘拥有独立的 8 槽（2026-07-27 变更）。

    背景：旧口径把真实持仓与模拟持仓混在同一个 8 槽预算里，导致 5 只真实持仓占满槽位、
    模拟盘 8.5 万美元现金在 50% 上限下却无槽可用（结构性死锁）。真实持仓是用户真金白银、
    仅供顾问跟踪（一律「建议未执行」），**不应占用模拟盘的风险预算**，故此处按 kind 分离：
      occupied/available/at_capacity 只反映**模拟盘**；真实持仓单列在 real_* 字段。
    frozen = 真实持仓且 quantity 未知（数量补齐后应为 0）——单列，不再挤占模拟预算。
    """
    open_pos = [p for p in positions if p.get("status") == "OPEN"]
    sim = [p for p in open_pos if p.get("kind") == "sim"]
    real = [p for p in open_pos if p.get("kind") == "real"]
    frozen = [p for p in real if str(p.get("quantity", "UNKNOWN")).upper() == "UNKNOWN"]
    real_manageable = [p for p in real if p not in frozen]
    occupied = len(sim)
    return {
        "slot_limit": slot_limit,
        "occupied": occupied,                       # 模拟盘占用的槽位
        "available": max(0, slot_limit - occupied),  # 模拟盘可直接建仓的空槽
        "manageable": len(sim) + len(real_manageable),  # 可定量管理的仓（模拟 + 数量已知的真实）
        "frozen": len(frozen),
        "frozen_symbols": [p.get("symbol") for p in frozen],
        "frozen_pct_of_limit": round(len(frozen) / slot_limit * 100, 1) if slot_limit else 0.0,
        "sim_open": len(sim),
        "real_tracked": len(real),                  # 真实持仓数（顾问跟踪，不占模拟槽）
        "at_capacity": occupied >= slot_limit,       # 仅指模拟盘是否满槽
        "note": ("模拟盘满槽：新机会只能通过替换进入（须过 selection.replacement_gate：冻结/最低持有期/"
                 "论点分差门槛，阈值以 lib/selection.py 为准，此处不复述数值防止二重管理）"
                 if occupied >= slot_limit else
                 "模拟盘有 %d 个空槽，可在 regime 仓位上限内直接建仓；真实持仓不占模拟预算"
                 % max(0, slot_limit - occupied)),
    }
