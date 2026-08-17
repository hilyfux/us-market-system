#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
integrity — 有检出力的账务校验、陈旧度看门狗、行情溯源

替换旧的「账务守恒」检查。旧检查是恒等式：
    现金 + 市值 = 总资产      (总资产本就由此定义)
    累计盈亏 = 总资产 - 100000 (累计盈亏本就由此定义)
它们恒返回 0.000000，包括在数据完全错误时，检出能力为 0。

本模块提供的校验都能真正失败：
    C1 市值重算   sum(qty x price) 对比存储市值
    C2 现金溯源   initial - sum(cost_basis) 对比存储现金
    C3 盈亏分解   sum(每仓未实现) 对比总未实现
    C4 逐仓一致   每仓 market_value == qty x last_close
    C5 成本一致   每仓 unrealized == market_value - cost_basis
"""
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Dict, List, Optional, Sequence

TOLERANCE = Decimal("0.05")   # USD


def D(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


class CheckResult(object):
    __slots__ = ("name", "passed", "expected", "actual", "diff", "detail", "severity")

    def __init__(self, name, passed, expected=None, actual=None, detail="", severity="ERROR"):
        self.name = name
        self.passed = bool(passed)
        self.expected = expected
        self.actual = actual
        # 非数值的 expected/actual（如 P4/P5 的 "stamp" / "缺失"）不参与差值计算。
        # 2026-08-11 发现：旧实现无条件 D()，使 P4/P5 一被触发就抛 InvalidOperation ——
        # 两个溯源守卫因此从未真正可用（L-007 类缺陷：检查存在但检不出东西）。
        if expected is not None and actual is not None:
            try:
                self.diff = D(actual) - D(expected)
            except (InvalidOperation, ValueError, TypeError):
                self.diff = None
        else:
            self.diff = None
        self.detail = detail
        self.severity = severity

    def __repr__(self):
        s = "PASS" if self.passed else ("WARN" if self.severity == "WARN" else "FAIL")
        base = "[%s] %s" % (s, self.name)
        if self.diff is not None:
            base += "  expected=%s actual=%s diff=%s" % (self.expected, self.actual, self.diff)
        if self.detail:
            base += "  — %s" % self.detail
        return base


def validate_accounting(wallet: Dict[str, object], positions: Sequence[Dict[str, object]],
                        initial_capital="100000") -> List[CheckResult]:
    """
    wallet:    {cash, total_market_value, total_assets, cumulative_pnl,
                realized_pnl, unrealized_pnl}
    positions: 仅模拟持仓（真实持仓 quantity 未知，按 CORE 不计入钱包）
               每项 {symbol, quantity, last_close, cost_basis, market_value, unrealized_pnl}
    """
    res = []
    cash = D(wallet["cash"])
    stored_mv = D(wallet["total_market_value"])
    stored_total = D(wallet["total_assets"])
    stored_cum = D(wallet["cumulative_pnl"])
    stored_unreal = D(wallet.get("unrealized_pnl", 0))
    realized = D(wallet.get("realized_pnl", 0))
    init = D(initial_capital)

    # C1 市值重算：从股数与收盘价独立重算，不信任存储值。
    # valuation 入力口径注记：この last_close（mark-to-market 入力）は **公式收盘价**——
    # mark-to-market・NAV は公式收盘で評価し POST_CLOSE が更新する（従来どおり）。
    # C1 は sum(qty×price)==stored_mv の恒等成立を検証するだけで **price ラベル不問**（C1 は不変）。
    # T-20min価は CLOSING の**约定フィル価格・保有成本の由来にのみ**用い、valuation には用いない
    # （2026-08-17 の口径統一で valuation まで T-20min化したが過剰と裁定され差し戻し；SYSTEM.md §4.3）。
    recomputed = sum((D(p["quantity"]) * D(p["last_close"])).quantize(Decimal("0.000001"))
                     for p in positions) if positions else Decimal(0)
    res.append(CheckResult(
        "C1 市值重算 sum(qty x price) vs 存储市值",
        abs(recomputed - stored_mv) <= TOLERANCE, stored_mv, recomputed,
        "有检出力：存储市值被篡改或漏更新即失败"))

    # C2 现金溯源：现金 = 初始资金 − 全部持仓成本基础 + 累计已实现盈亏。
    # 卖出兑现的盈/亏落入现金，故须加 realized；realized=0 时与旧式完全等价（向后兼容，
    # 全部历史账目与既有 selftest 不受影响）。仍能抓幽灵交易/漏记成本/手改现金，
    # 且新增：卖出后现金若与「成本回收 + 已实现盈亏」不符即失败。
    derived_cash = (init - sum(D(p["cost_basis"]) for p in positions) + realized) if positions else (init + realized)
    res.append(CheckResult(
        "C2 现金溯源 initial - sum(cost_basis) + realized vs 存储现金",
        abs(derived_cash - cash) <= TOLERANCE, cash, derived_cash,
        "有检出力：幽灵交易、漏记成本、现金被手改、卖出兑现记错均会失败"))

    # C3 盈亏分解
    sum_unreal = sum(D(p["unrealized_pnl"]) for p in positions) if positions else Decimal(0)
    res.append(CheckResult(
        "C3 盈亏分解 sum(每仓未实现) vs 总未实现",
        abs(sum_unreal - stored_unreal) <= TOLERANCE, stored_unreal, sum_unreal))

    # C4/C5 逐仓一致
    for p in positions:
        sym = p["symbol"]
        mv_calc = (D(p["quantity"]) * D(p["last_close"])).quantize(Decimal("0.000001"))
        res.append(CheckResult(
            "C4 %s market_value == qty x last_close" % sym,
            abs(mv_calc - D(p["market_value"])) <= TOLERANCE, D(p["market_value"]), mv_calc))
        pnl_calc = (D(p["market_value"]) - D(p["cost_basis"])).quantize(Decimal("0.000001"))
        res.append(CheckResult(
            "C5 %s unrealized == market_value - cost_basis" % sym,
            abs(pnl_calc - D(p["unrealized_pnl"])) <= TOLERANCE, D(p["unrealized_pnl"]), pnl_calc))

    # 恒等式：保留但明确标注无检出力，供人工核对可读性
    res.append(CheckResult(
        "I1 恒等式 cash+mv==total（无检出力，仅可读性）",
        abs((cash + stored_mv) - stored_total) <= TOLERANCE, stored_total, cash + stored_mv,
        "identity, not a test", severity="WARN"))
    res.append(CheckResult(
        "I2 恒等式 total-initial==cum_pnl（无检出力）",
        abs((stored_total - init) - stored_cum) <= TOLERANCE, stored_cum, stored_total - init,
        "identity, not a test", severity="WARN"))
    res.append(CheckResult(
        "C6 累计盈亏 == 已实现 + 未实现",
        abs((realized + stored_unreal) - stored_cum) <= TOLERANCE, stored_cum, realized + stored_unreal,
        "有检出力：已实现/未实现拆分错误会失败"))
    return res


POSITION_STANDARD_USD = Decimal("10000")   # 用户 2026-07-31：每标的初始一律 $10,000
SIZE_EXCEPTION_TAG = "SIZE_EXCEPTION"      # 账本 thesis 列带此标记 = 显式豁免（如部分止盈后）


def sizing_uniformity(positions: Sequence[Dict[str, object]],
                      standard: Decimal = POSITION_STANDARD_USD) -> List[CheckResult]:
    """
    C7 仓位标准统一性（2026-07-31 新增，防「一部 $5k 一部 $10k」类漂移复发）：
    每个 OPEN 持仓的 cost_basis 必须等于统一标准（±TOLERANCE），
    除非该仓在账本 thesis 里带显式 SIZE_EXCEPTION 标记（例如部分止盈后的合法半仓）。
    背景：$10k 均衡计划落地时 ABT 被自行保留半仓——个人判断不得静默覆盖用户口径，
    偏离必须显式、必须响亮。
    """
    res = []
    for p in positions:
        sym = p["symbol"]
        if SIZE_EXCEPTION_TAG in str(p.get("thesis", "")):
            res.append(CheckResult("C7 %s 仓位标准（显式豁免 %s）" % (sym, SIZE_EXCEPTION_TAG),
                                   True, detail="带豁免标记，跳过", severity="WARN"))
            continue
        cb = D(p["cost_basis"])
        res.append(CheckResult(
            "C7 %s 仓位标准 == $%s" % (sym, standard),
            abs(cb - standard) <= TOLERANCE, standard, cb,
            "每标的统一 $10k（用户 2026-07-31）；偏离须带 %s 标记" % SIZE_EXCEPTION_TAG))
    return res


# --------------------------------------------------------------- 看门狗
STALENESS_MAX_TRADING_DAYS = 1


def staleness_check(valuation_date: str, today: date, cal, max_days=STALENESS_MAX_TRADING_DAYS) -> CheckResult:
    """
    2026-07 停摆的直接检出点：估值日落后最近交易日超过 max_days 即升级为故障。
    证据当时就摆在 last_successful_official_settlement 里，但无人断言。
    """
    vd = date.fromisoformat(valuation_date)
    last_td = today if cal.is_trading_day(today) else cal.prev_trading_day(today)
    behind = cal.trading_days_between(vd, last_td)
    ok = behind <= max_days
    return CheckResult(
        "W1 估值陈旧度",
        ok, max_days, behind,
        "估值日 %s 落后最近交易日 %s 共 %d 个交易日（上限 %d）%s" % (
            vd.isoformat(), last_td.isoformat(), behind, max_days,
            "" if ok else " -> STALE_VALUATION，须升级告警而非静默"))


def liveness_check(last_run_iso: Optional[str], now: datetime, max_gap_min: int = 180) -> CheckResult:
    """存活检查：系统无法报告『自己没在跑』，故需显式断言上次运行时间。"""
    if not last_run_iso:
        return CheckResult("W2 存活", False, max_gap_min, None,
                           "无上次运行记录 -> 无法证明系统存活")
    gap = (now - datetime.fromisoformat(last_run_iso)).total_seconds() / 60.0
    return CheckResult("W2 存活", gap <= max_gap_min, max_gap_min, round(gap, 1),
                       "距上次运行 %.1f 分钟" % gap)


def git_pipeline_check(bundle_exists: bool, bundle_age_min: Optional[float],
                       stamp_matches: bool, err_bytes: int,
                       max_pending_min: int = 30) -> List[CheckResult]:
    """
    W5 git 推送管道看门狗（2026-07-27，WARN 级——git 故障绝不阻断交易/报告）。
    检出：bundle 已出但转发器长时间未处理（GIT_PIPELINE_STALE）；pusher.err 有内容。
    v1 pusher 的"错误基线比较->误盖章跳过"类 bug 即属此类：坏在沉默，不坏在报错。
    """
    res = []
    if not bundle_exists:
        res.append(CheckResult("W5 git 管道", True, None, None, "无待推 bundle", severity="WARN"))
    elif stamp_matches:
        res.append(CheckResult("W5 git 管道", True, None, None, "bundle 已被转发器处理", severity="WARN"))
    else:
        ok = bundle_age_min is not None and bundle_age_min <= max_pending_min
        res.append(CheckResult("W5 git 管道", ok, max_pending_min,
                               None if bundle_age_min is None else round(bundle_age_min, 1),
                               "bundle 待处理 %s 分钟%s" % (
                                   "?" if bundle_age_min is None else "%.1f" % bundle_age_min,
                                   "" if ok else " -> GIT_PIPELINE_STALE（转发器可能未运行）"),
                               severity="WARN"))
    res.append(CheckResult("W5 pusher.err 为空", err_bytes == 0, 0, err_bytes,
                           "" if err_bytes == 0 else "pusher 有 stderr 输出，需查看",
                           severity="WARN"))
    return res


def queue_health(pending: Sequence[str], failed: Sequence[str], now: datetime,
                 oldest_pending_age_min: Optional[float], max_age_min: int = 30) -> List[CheckResult]:
    """死信与积压监控：failed/ 此前无人查看，.attempts 用尽后静默放弃。"""
    res = [CheckResult("W3 死信目录 failed/ 为空", len(failed) == 0, 0, len(failed),
                       "存在投递失败消息需人工处理：%s" % ", ".join(failed[:5]) if failed else "")]
    if oldest_pending_age_min is not None:
        res.append(CheckResult("W4 队列积压时长", oldest_pending_age_min <= max_age_min,
                               max_age_min, round(oldest_pending_age_min, 1),
                               "最旧待投递消息已等待 %.1f 分钟" % oldest_pending_age_min))
    else:
        res.append(CheckResult("W4 队列积压时长", True, max_age_min, 0, "队列为空"))
    return res


# --------------------------------------------------------------- 行情溯源
# 信息源注册表（2026-07-27 §13）：**按指标分级**，全部条目来自实测（2026-07-25 三源核验记录）。
# 规则：交易门槛指标（equity_close/vix/us10y）每项须 ≥2 个核准源，否则 P1 永远无法通过——
# 这是可用性属性，selftest 断言之。quirk 标志与 CACHE_BUSTER/STAMP 常量保持一致。
APPROVED_SOURCES = {
    "equity_close": {           # 个股/ETF 正式收盘与历史
        "stockanalysis.com": {"cache_buster": True,
                              "note": "无 ?v= 缓存参数会返回数周旧缓存（ETN 实测给过 7/21 收盘）"},
        "roic.ai": {"note": "ABT 实测含盘后价，取正式收盘字段"},
        "stocktitan.net": {"stamp_check": True,
                           "note": "按标的冻结；必须核对 Last updated（GEV 页曾滞留一个月）"},
        "stockscan.io": {"stamp_check": True,
                         "note": "2026-08-11 实测：同一时刻对 MSFT/ETN/ABT/NVDA/LLY 返回 7 月下旬旧行情（站内指数条也停在旧值），KTOS 却是当日定稿——按标的冻结，与 stocktitan 同类。必须核对该页自身的日期戳/前收盘是否等于我方记录的上一交易日收盘，不一致即弃用该源"},
    },
    "vix": {                    # 波动率指数
        "cboe.com": {"cache_buster": True, "note": "发行方；cdn.cboe.com 无缓存参数曾给六月快照"},
        "investing.com": {"note": "仅指数页可用；其个股报价页数周陈旧，不得用于 equity_close"},
        "google.com/finance": {},
        "tradingeconomics.com": {},
    },
    "us10y": {                  # 十年期美债收益率
        "investing.com": {},
        "cboe.com": {"note": "^TNX"},
        "tradingeconomics.com": {},
        "etftrends.com": {},
    },
    "breadth": {                # 市场宽度（环境分类用，非交易门槛，允许单源+标注）
        "stockanalysis.com": {"cache_buster": True, "note": "markets 页；单源可用但须在内部记录标注"},
    },
    # closing_window_price（T-20min価＝引け20分前の盤中価，CLOSING約定フィル専用）：用途を厳密限定
    # （2026-08-17 用户裁定）。この盤中価は **CLOSING で約定した取引のフィル価格と、それに由来する
    # 保有成本（コスト基準）にのみ**用いる。取得口径＝**≥2 核准源・偏差≤1%・盤中タイムスタンプ**。
    # 盤中価ゆえ「At close／Adj.Close 定稿／全日出来高」は**要求しない**（≥2源の安全要件 L-004 は保持）。
    # **評価（mark-to-market・NAV）・離場判定・分析・戦略レビュー・データ門の取価には用いない**——
    # これらは全て equity_close（正式收盘、POST_CLOSE で更新/検証）。当初 addendum は本価格を全会计書込・
    # 評価・データ門・離場まで拡大したが過剰と裁定され差し戻し。TRADE_GATING_METRICS には**入れない**
    # （runtime の収盘取得フローと混同しないため；≥2核准源可满足性は test_price_convention が机器保证）。
    "closing_window_price": {
        "stockanalysis.com": {"cache_buster": True,
                              "note": "报价头の盤中価（Market open 時）を CLOSING約定フィル価格（T-20min価）に用いる；缓存参数必须"},
        "roic.ai": {"note": "盘中报价字段を用いる（At close ではなく現在値）"},
        "stocktitan.net": {"note": "盘中现价；≥2源の一つ"},
        "stockscan.io": {"note": "盘中现价；≥2源の一つ"},
    },
}
TRADE_GATING_METRICS = ("equity_close", "vix", "us10y")


def approved_for(metric: str):
    """返回该指标的核准源字典；未注册指标返回空 dict（调用方须显式处理）。"""
    return APPROVED_SOURCES.get(metric, {})


BAD_SOURCES = {
    "nasdaq.com": "JS 空壳", "cnbc.com": "JS 空壳", "finviz.com": "JS 空壳",
    "zacks.com": "JS 空壳", "barchart.com": "JS 空壳",
    "wsj.com": "抓取被拒", "marketwatch.com": "抓取被拒",
    "markets.businessinsider.com": "抓取被拒",
    "macrotrends.net": "数周陈旧", "wallstreetzen.com": "数周陈旧",
    "stockinvest.us": "数周陈旧", "gurufocus.com": "数周陈旧",
    "finance.yahoo.com": "报价页严重陈旧（非延迟）",
    "home.treasury.gov": "所有端点均截断",
}
CACHE_BUSTER_REQUIRED = ("stockanalysis.com", "cdn.cboe.com")
STAMP_CHECK_REQUIRED = ("stocktitan.net", "stockscan.io")
MAX_CROSS_SOURCE_PCT = Decimal("1.0")


class PriceRecord(object):
    """
    按价格记录溯源。旧账本只存一个 last_close + VERIFIED，无来源无时间戳，
    事后无法审计某个数字是谁给的 —— 而本次实测有多个来源在给错数
    （缓存陈旧、盘中行冒充收盘），故溯源必须落到单价级别。
    """
    __slots__ = ("symbol", "session_date", "close", "sources", "note")

    def __init__(self, symbol: str, session_date: str, close, sources: List[Dict[str, str]], note=""):
        self.symbol = symbol
        self.session_date = session_date
        self.close = D(close)
        self.sources = sources          # [{domain, figure, url, method}]
        self.note = note

    def validate(self) -> List[CheckResult]:
        res = []
        domains = {s["domain"] for s in self.sources}
        res.append(CheckResult("P1 %s 独立来源 >=2" % self.symbol,
                               len(domains) >= 2, 2, len(domains),
                               "来源：%s" % ", ".join(sorted(domains))))
        banned = domains & set(BAD_SOURCES)
        res.append(CheckResult("P2 %s 未使用已知不可靠来源" % self.symbol,
                               not banned, 0, len(banned),
                               "命中黑名单：%s" % ", ".join(sorted(banned)) if banned else ""))
        figs = [D(s["figure"]) for s in self.sources]
        spread = (max(figs) - min(figs)) / min(figs) * 100 if figs and min(figs) > 0 else Decimal(0)
        res.append(CheckResult("P3 %s 跨源偏差 <=%s%%" % (self.symbol, MAX_CROSS_SOURCE_PCT),
                               spread <= MAX_CROSS_SOURCE_PCT, MAX_CROSS_SOURCE_PCT,
                               spread.quantize(Decimal("0.0001"))))
        for s in self.sources:
            if any(d in s["domain"] for d in CACHE_BUSTER_REQUIRED) and "?" not in s.get("url", ""):
                res.append(CheckResult("P4 %s %s 需带 cache-buster" % (self.symbol, s["domain"]),
                                       False, "?v=N", "无",
                                       "该域名曾返回数周前缓存", severity="WARN"))
            if any(d in s["domain"] for d in STAMP_CHECK_REQUIRED) and not s.get("stamp"):
                res.append(CheckResult("P5 %s %s 需核对 Last updated 戳" % (self.symbol, s["domain"]),
                                       False, "stamp", "缺失",
                                       "该站按标的冻结，曾出现整月陈旧", severity="WARN"))
        return res

    def to_dict(self):
        return {"symbol": self.symbol, "session_date": self.session_date,
                "close": str(self.close), "sources": self.sources, "note": self.note}


def summarize(results: Sequence[CheckResult]) -> Dict[str, object]:
    errs = [r for r in results if not r.passed and r.severity == "ERROR"]
    warns = [r for r in results if not r.passed and r.severity == "WARN"]
    return {"total": len(results), "failed": len(errs), "warned": len(warns),
            "ok": not errs, "failures": [repr(r) for r in errs],
            "warnings": [repr(r) for r in warns]}
