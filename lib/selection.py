#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
selection — 选股/建仓纪律门（ACT-005/006/007），确定性、可测试。

背景：2026-07 的深亏集中在「财报前投机建仓 + 单一主题等额重仓」。复盘沉淀出
L-008/L-009/L-010/L-012，但此前只停留在 knowledge 与 HYPOTHESIS，未进入强制规则。
本模块把三条已验证的教训做成纯函数门，由 MORNING 新机会扫描调用，selftest 锁定。

机制以代码为准（SYSTEM.md §0）：改阈值即改策略，改这里并同步 selftest。
"""
from decimal import Decimal
from typing import Dict, Optional, Tuple

# 论题标签（thesis-level，用于集中度会计；GICS 行业检不出跨行业的同一叙事，见 L-009）。
# 新标的建仓时必须在此登记论题标签，否则集中度门无法计算 -> 视为未知，保守拒绝。
THEME_TAGS: Dict[str, str] = {
    "GEV": "ai_power", "ETN": "ai_power", "PWR": "ai_power", "BE": "ai_power",
    "KTOS": "defense", "MP": "rare_earth", "RMBS": "ai_memory", "ABT": "healthcare",
    "MSFT": "ai_software",  # 2026-08-06 MORNING 注册（替换候选入档，8/5 双源收盘 487.46）
}

BASE_INITIAL_PCT = Decimal("10")   # ACT-004：单只新仓初始 = NAV 的 10%（= $10,000 @ $100k），
                                   # 比例制（随 NAV 缩放）、更均衡（用户 2026-07-31）。高 beta 经 ACT-007 折半。
REPLACEMENT_MARGIN = Decimal("5")  # ACT-004 替换门：候选总分须高于最弱持仓 ≥5 分（确定性显著更高）。
THEME_CAP_PCT = Decimal("25")      # ACT-006：同论题合并敞口上限（占 NAV）
EVENT_BLACKOUT_SESSIONS = 5        # ACT-005：二元催化前禁新建的交易日数
HIGH_BETA_SIZE_FACTOR = Decimal("0.5")  # ACT-007：高 beta 名义仓位折半


def event_timing_gate(sessions_until_earnings: Optional[int],
                      blackout: int = EVENT_BLACKOUT_SESSIONS) -> Tuple[bool, str]:
    """
    ACT-005（L-010 事件后确认优于事件前押注）：二元催化（财报）前 `blackout` 个交易日内
    禁止**新建**仓；等财报落地并被收盘确认后再入场。

    sessions_until_earnings：距下一财报的交易日数；None = 无近端已知催化。
    返回 (allowed, reason)。仅约束新建/加仓，不影响既有持仓的「持有」。
    """
    if sessions_until_earnings is None:
        return True, "无近端已知催化"
    if sessions_until_earnings < 0:
        return True, "财报已过（事件后，允许在确认收盘后入场）"
    if sessions_until_earnings <= blackout:
        return False, "距财报仅 %d 个交易日（≤%d），事件前不建仓（L-010）" % (
            sessions_until_earnings, blackout)
    return True, "距财报 %d 个交易日，超出封锁窗口" % sessions_until_earnings


def theme_exposure_pct(add_amount: Decimal, nav: Decimal,
                       current_theme_mv: Decimal) -> Decimal:
    """建仓后该论题合并敞口占 NAV 的百分比（纯计算）。"""
    if nav <= 0:
        raise ValueError("NAV 必须为正")
    return ((current_theme_mv + add_amount) / nav * 100)


def theme_cap_gate(theme: Optional[str], add_amount: Decimal, nav: Decimal,
                   current_theme_mv: Decimal,
                   cap_pct: Decimal = THEME_CAP_PCT) -> Tuple[bool, str]:
    """
    ACT-006（L-009/L-012 集中度按论题算并在建仓时强制）：新建/加仓后，
    同论题合并敞口不得超过 NAV 的 cap_pct%。theme=None（未登记论题）保守拒绝。
    """
    if theme is None:
        return False, "标的未登记论题标签，集中度不可计算 -> 保守拒绝（先登记 THEME_TAGS）"
    pct = theme_exposure_pct(add_amount, nav, current_theme_mv).quantize(Decimal("0.01"))
    if pct > cap_pct:
        return False, "论题 %s 建仓后敞口 %.2f%% > 上限 %.0f%%（L-012）" % (theme, pct, cap_pct)
    return True, "论题 %s 建仓后敞口 %.2f%% ≤ %.0f%%" % (theme, pct, cap_pct)


def volatility_scaled_size(base_pct: Decimal, is_high_beta: bool,
                           factor: Decimal = HIGH_BETA_SIZE_FACTOR) -> Decimal:
    """ACT-007（L-008 仓位看波动）：高 beta 标的名义仓位按 factor 折算（默认减半）。"""
    return (base_pct * factor) if is_high_beta else base_pct


def replacement_gate(candidate_score, weakest_score,
                     margin: Decimal = REPLACEMENT_MARGIN) -> Tuple[bool, str]:
    """
    ACT-004 满槽替换门（2026-08-04 用户裁定：确定性替换方法论）。
    候选总分（九维综合评分：信息调研/基本面/事件驱动/产业链/财报/技术/指标/情绪/全球局势）
    ≥ 最弱持仓总分 + margin 即允许「卖最弱、买候选」；
    **不再要求旧仓满足「公司破坏」退出条件**——该条件只约束非替换的主动退出（ACT-002/003）。
    非强制换仓：无更优候选（差距 < margin）则全体持有。
    新仓建立仍须另过 screen_new_position()（ACT-005/006/007）。
    """
    diff = Decimal(str(candidate_score)) - Decimal(str(weakest_score))
    if diff >= margin:
        return True, "候选总分高于最弱持仓 %s 分 ≥ 门槛 %s 分 -> 允许替换（卖最弱、买候选）" % (diff, margin)
    return False, "候选总分仅高 %s 分 < 门槛 %s 分（确定性未显著更高）-> 不替换、全体持有" % (diff, margin)


def screen_new_position(symbol: str, base_pct: Decimal, nav: Decimal,
                        current_theme_mv: Decimal, sessions_until_earnings: Optional[int],
                        is_high_beta: bool) -> Dict[str, object]:
    """
    组合三门，返回是否可建仓、建议仓位（折算后）、各门结论。
    add_amount 用折算后仓位对应的金额参与集中度门（先算 size 再算集中度）。
    """
    theme = THEME_TAGS.get(symbol)
    sized_pct = volatility_scaled_size(base_pct, is_high_beta)
    add_amount = (nav * sized_pct / 100)
    ev_ok, ev_why = event_timing_gate(sessions_until_earnings)
    th_ok, th_why = theme_cap_gate(theme, add_amount, nav, current_theme_mv)
    allowed = ev_ok and th_ok
    return {
        "allowed": allowed,
        "theme": theme,
        "sized_pct": sized_pct,
        "add_amount": add_amount,
        "gates": {"ACT-005_event": (ev_ok, ev_why),
                  "ACT-006_theme": (th_ok, th_why)},
    }
