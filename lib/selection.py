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
    # 2026-08-08 MORNING 注册：AI 算力芯片是与 ai_power（发电/输配电）、ai_software（云与应用）
    # 不同的产业链环节与驱动因子，按 L-009「论题而非 GICS」口径单列。
    "NVDA": "ai_semis", "AVGO": "ai_semis",
    # 2026-08-11 MORNING 注册：LLY 与 ABT 同属 healthcare 论题（器械 vs 制药同为医疗支付/监管
    # 驱动，按 L-009「论题而非 GICS」口径合并计集中度，避免两只医疗仓被当成互不相关的敞口）。
    "LLY": "healthcare",
    # 2026-08-12 MORNING 注册：LNG（Cheniere）驱动因子是美国 LNG 出口产能与全球天然气
    # 运输/价差，与本簿现有 AI 电力/半导体/医疗/国防/稀土五条论题均无共同驱动，单列。
    "LNG": "lng_export",
    # 2026-08-15 MORNING 注册（估值 2026-08-14）：TSM 与 NVDA/AVGO 同属 AI 算力芯片
    # 产业链环节（代工端），按 L-009「论题而非 GICS」口径并入 ai_semis 合并计集中度。
    "TSM": "ai_semis",
}

BASE_INITIAL_PCT = Decimal("10")   # ACT-004：单只新仓初始 = NAV 的 10%（= $10,000 @ $100k），
                                   # 比例制（随 NAV 缩放）、更均衡（用户 2026-07-31）。高 beta 经 ACT-007 折半。
REPLACEMENT_MARGIN = Decimal("15")  # ACT-004 替换门（用户 2026-08-15 裁定：5 -> 15）。
                                    # 实证：8/05–8/14 五次替换，可测四次全部劣后（-1.2/-2.0/-5.4/-11.5pp），
                                    # 且分差与结果无相关（+17 的 RMBS→MSFT 劣后 2.0pp，+12 的 GEV→LLY 劣后 11.5pp）。
                                    # 提高阈值只减少频次、不修正根因；根因由 ACT-008/009 两门处理。
                                    # ⚠ 数值地位 = HYPOTHESIS（2026-08-15 降格，SYSTEM.md §4.2 / playbook HYP-003）：
                                    #   「15」这个数选自 4 个观测的噪声，无统计根据——与 ACT-009 的结构性结论
                                    #   （价格派生维度不得参与排序，来自根因分析）根据强度不同。行为不变（照旧强制），
                                    #   裁定条件＝replacement claim 裁定满 20 件时的记分卡（learning.scorecard）。
THEME_CAP_PCT = Decimal("25")      # ACT-006：同论题合并敞口上限（占 NAV）
EVENT_BLACKOUT_SESSIONS = 5        # ACT-005：二元催化前禁新建的交易日数
HIGH_BETA_SIZE_FACTOR = Decimal("0.5")  # ACT-007：高 beta 名义仓位折半

# ---- ACT-008 最低持有期（用户 2026-08-15 裁定）----------------------------------
# 买入理由是多年期论点，卖出理由却是 5 日内价格 —— 两个时间轴不一致是结构性缺陷，
# 与样本量无关。实测：LLY 持有 5 个交易日、NVDA 3 个交易日即被相对分排序卖出，
# 五次退出**没有一次**由失效线触发（LLY 失效线 1113.95 未触及、卖价 1180.16）。
MIN_HOLDING_SESSIONS = 15          # 建仓后 N 个交易日内禁止「相对分排序」卖出。
                                   # 失效线/止损（ACT-002/003）不受本门约束——风险管理始终优先。
                                   # ⚠ 数值地位 = HYPOTHESIS（2026-08-15 降格，SYSTEM.md §4.2 / playbook HYP-003）：
                                   #   「必须有最低持有期」是结构性结论（时间轴不一致，根因分析所得，不降格）；
                                   #   「15」这个具体天数是在 4 个观测的噪声上选定的，无统计根据。行为不变，
                                   #   裁定条件＝replacement claim 裁定满 20 件时的记分卡（learning.scorecard）。

# ---- ACT-009 替换评分只用论点维度（用户 2026-08-15 裁定）------------------------
# 九维里技术面/指标是价格派生的，会让「刚下跌的仓」自动落到最弱位，
# 于是机械地「卖弱买强」，与长期持有相反。四次被卖出的标的全部在数日内反弹即其后果。
# 价格维度保留在**离场判定**侧（ACT-002/003 失效线），不参与替换排序。
THESIS_SCORE_DIMS = ("信息调研", "基本面", "事件驱动", "产业链", "财报", "情绪", "全球局势")
PRICE_SCORE_DIMS = ("技术面", "指标")

# ---- 替换冻结（用户 2026-08-15 裁定）-------------------------------------------
# 8/26 NVDA 决算 + GEV/LLY 卖出后追踪が出るまで新規入れ替えを停止。
REPLACEMENT_FROZEN = True
REPLACEMENT_FREEZE_REASON = ("用户 2026-08-15 裁定：替换方法论待验证期。"
                             "解冻条件＝8/26 NVDA 财报回填 + GEV/LLY/NVDA 卖出后相对表现入档（L-020）")


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


def thesis_score(dim_scores: Dict[str, object]) -> Decimal:
    """
    ACT-009：从九维打分里取**论点维度**之和，作为替换排序的唯一依据。

    dim_scores 必须是九维全集（缺维 = 打分未完成，拒绝）；技术面/指标照常打分并记录，
    但不进入本函数返回值——它们只在离场判定（ACT-002/003 失效线）侧使用。
    """
    missing = [d for d in THESIS_SCORE_DIMS + PRICE_SCORE_DIMS if d not in dim_scores]
    if missing:
        raise ValueError("九维打分不完整，缺：%s（缺维不得进入替换排序）" % "/".join(missing))
    return sum((Decimal(str(dim_scores[d])) for d in THESIS_SCORE_DIMS), Decimal("0"))


def min_holding_gate(sessions_held: Optional[int],
                     invalidation_hit: bool = False,
                     min_sessions: int = MIN_HOLDING_SESSIONS) -> Tuple[bool, str]:
    """
    ACT-008 最低持有期（用户 2026-08-15 裁定）：建仓后 min_sessions 个交易日内，
    **不得因相对分排序被卖出**；只有失效线/止损触发（invalidation_hit=True）才可离场。

    返回 (可因替换卖出?, 理由)。sessions_held=None（代理成本仓/基线迁移仓，建仓日不可考）
    视为已过最低期——不能用未知去阻断风险管理，也不能用未知去豁免纪律，
    故按「已过期」处理并在理由里显式标注，由人工在复盘时校正。
    """
    if invalidation_hit:
        return True, "失效线已触发 -> 风险管理优先于最低持有期，可离场"
    if sessions_held is None:
        return True, "建仓日不可考（基线迁移仓）-> 按已过最低持有期处理（须在复盘显式标注）"
    if sessions_held < min_sessions:
        return False, ("持有仅 %d 个交易日 < 最低 %d 个 -> 不因相对分卖出"
                       "（买入理由是多年期论点，不可用数日价格推翻）" % (sessions_held, min_sessions))
    return True, "持有 %d 个交易日 ≥ 最低 %d 个 -> 可参与替换排序" % (sessions_held, min_sessions)


def replacement_gate(candidate_score, weakest_score,
                     margin: Decimal = REPLACEMENT_MARGIN,
                     sessions_held: Optional[int] = None,
                     invalidation_hit: bool = False,
                     frozen: bool = None) -> Tuple[bool, str]:
    """
    ACT-004 满槽替换门（2026-08-04 用户裁定确立，2026-08-15 用户裁定收紧）。

    传入的分数**必须是 thesis_score() 的论点分**（ACT-009），不是九维总分。
    判定顺序：冻结 -> 最低持有期（ACT-008）-> 分差 ≥ margin。
    任一不满足则全体持有。新仓建立仍须另过 screen_new_position()（ACT-005/006/007）。

    **边界即停（用户 2026-08-15 裁定的深思原则）**：分差恰好等于 margin 时不自动放行，
    返回 False 并要求显式复核——「刚好达标」是最该多想一层的地方，不是最该照章执行的地方。
    LLY→TSM 正是在 +5 恰好达标处机械执行，结果是当日最贵的一次替换。
    """
    if frozen is None:
        frozen = REPLACEMENT_FROZEN
    if frozen:
        return False, "替换已冻结：%s" % REPLACEMENT_FREEZE_REASON

    hold_ok, hold_why = min_holding_gate(sessions_held, invalidation_hit)
    if not hold_ok:
        return False, "最低持有期未满 -> 不替换（%s）" % hold_why

    diff = Decimal(str(candidate_score)) - Decimal(str(weakest_score))
    if diff == margin:
        return False, ("论点分恰好高 %s 分 ＝ 门槛 %s 分（边界）-> 不自动执行，"
                       "须显式复核后由人裁定（边界即停）" % (diff, margin))
    if diff > margin:
        return True, "论点分高于最弱持仓 %s 分 > 门槛 %s 分 -> 允许替换（卖最弱、买候选）" % (diff, margin)
    return False, "论点分仅高 %s 分 < 门槛 %s 分（确定性未显著更高）-> 不替换、全体持有" % (diff, margin)


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
