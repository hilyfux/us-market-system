#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_lint — 把 SYSTEM.md §5「可读性与无歧义」标准里**机器可验证的子集**变成硬门。

设计原则：**高精确、低误报**。宁可漏判几处纯编辑性歧义（交由生成报告的一步自检兜底），
也不要误杀一份合规报告——`enqueue()` 会在 lint 失败时抛 `ReportLintError`，
一个假阳性就会挡住一次本该发出的推送。因此这里只断言那些不依赖语义理解、
可确定判定的规则：

  L1 标题行         首个非空行必须是 markdown 标题（`#` 开头）且含日期。
  L2 篇幅           盘前/盘中/盘后 ≤650 字、晨间 ≤700 字（非空白字符计）。
  L3 动作词表       正文出现的“类动作”动词必须取自 §4 词表；模糊动词（观察/关注/择机…）一律判违规。
  L4 建议未执行标注  盘前/盘中阶段的非“持有”交易动作行必须显式标注“建议未执行”
                     （带否定词的“无减仓/平仓信号”一类不误判）。
  L5 （已撤销，2026-07-27）原“须注明数据时间来源”。用户裁定推送是交易便签，
                     溯源与数据质量属内部事务；验证照做，但不进正文。
  L6 内部事务泄漏    来源域名/降级术语/升级项出现在推送正文即违规（问题内部修，不推给用户）。

纯语义类要求（自相矛盾、可两解、省略前提）无法在不做真正语言理解的前提下稳定判定，
**刻意不在此断言**，仍由报告生成步骤负责——§5 已注明这一分工。
"""
import re
from typing import Dict, List, Optional

MORNING_LIMIT = 700
DEFAULT_LIMIT = 650

# §4 唯一合法动作集合。X% 形式用正则匹配。
_VALID_ACTION_RE = re.compile(
    r"(?:持有|建仓|加仓|减仓|平仓"
    r"|止盈-减仓\d+%|止盈-平仓"
    r"|止损-减仓\d+%|止损-平仓)"
)
# 交易类（非“持有”）动作——盘前/盘中须标注“建议未执行”。
_TRADE_ACTION_RE = re.compile(r"(?:建仓|加仓|减仓|平仓|止盈|止损)")
# 明确禁止的模糊动词：像动作却不在词表内，是歧义之源。
_VAGUE_VERBS = ("观察", "关注", "留意", "观望", "择机", "逢低", "逢高",
                "视情况", "看情况", "伺机", "酌情", "再看", "待定")
# 否定/无信号语境，避免把“无减仓平仓信号”误判为一次减仓动作。
# 刻意不含「0 」「零」——它们会误配时刻（如 10:00 ）与百分比，造成误判。
_NEGATION = ("无", "未", "没有", "不", "非", "no ", "not ", "without", "none")
# 条件/假设/检查语境：“若…则减仓”“开盘后检查…待收盘确认”不是一次当下的动作指派，
# 而是前瞻的决策规则；与否定语境同样豁免 L4。否则前瞻检查条件里出现的动作词
# （如“再议减仓”）会被误判成未标注的交易动作，挡住一份合规报告（2026-07-27 修复）。
# 只收录强假设/检查指示词，不含裸“则/需/视”，避免过度豁免真实动作行。
_CONDITIONAL = ("若", "如果", "一旦", "假设", "检查", "复核",
                "确认后", "待确认", "触发条件", "if ", "once ", "should ")
_DATE_RE = re.compile(r"\d{4}-\d{2}-\d{2}|\d{1,2}\s*月\s*\d{1,2}\s*日")
# 内部事务标记（2026-07-27，L6）：这些词属于系统内部（溯源/降级/升级项），
# 出现在推送正文即违规——用户只要「代码·动作·原因」，问题内部解决。
_INTERNAL_LEAK_MARKERS = ("stockanalysis.com", "roic.ai", "数据时间", "数据来源",
                          "MARKET_DATA_DEGRADED", "STATE_INTEGRITY_FAILURE",
                          "ENQUEUE_PATH_UNAVAILABLE", "STALE_VALUATION",
                          "数据降级", "未核实", "无法核实", "延迟>")


class ReportLintError(ValueError):
    """报告不满足 §5 机器可验证标准；含具体违规列表。修正后用 KEY#rN 重发。"""

    def __init__(self, violations: List[str]):
        self.violations = violations
        super().__init__("报告未通过 §5 可读性/无歧义硬门：\n- " + "\n- ".join(violations))


def stage_from_report_key(report_key: str) -> Optional[str]:
    """PREMARKET+.. / INTRADAY+.. / MORNING+.. / POSTCLOSE+.. -> 阶段；其余返回 None（不 lint）。"""
    base = report_key.split("+", 1)[0].split("#", 1)[0].strip().upper()
    return base if base in ("PREMARKET", "INTRADAY", "MORNING", "POSTCLOSE") else None


def _char_count(markdown: str) -> int:
    """字数 = 非空白字符数（对 markdown 标记从严，宁紧勿松）。"""
    return len(re.sub(r"\s+", "", markdown))


def lint_report(markdown: str, stage: str) -> Dict[str, object]:
    """返回 {ok, violations}。stage ∈ {PREMARKET, INTRADAY, MORNING, POSTCLOSE}。"""
    stage = stage.upper()
    v: List[str] = []
    lines = [ln for ln in markdown.splitlines()]
    nonblank = [ln for ln in lines if ln.strip()]

    # L1 标题行
    if not nonblank:
        v.append("L1 空报告：无任何内容")
    else:
        title = nonblank[0].strip()
        if not title.startswith("#"):
            v.append("L1 首行必须是 markdown 标题（以 # 开头），当前为：%r" % title[:40])
        elif not _DATE_RE.search(title):
            v.append("L1 标题行必须含日期（阶段+日期），当前为：%r" % title[:40])

    # L2 篇幅
    limit = MORNING_LIMIT if stage == "MORNING" else DEFAULT_LIMIT
    n = _char_count(markdown)
    if n > limit:
        v.append("L2 篇幅超限：%d 字 > %s 阶段上限 %d 字" % (n, stage, limit))

    # L3 模糊动词
    for verb in _VAGUE_VERBS:
        if verb in markdown:
            v.append("L3 出现模糊动词「%s」——动作必须取自 §4 词表，不得含糊" % verb)

    # L4 非“持有”交易动作须标注“建议未执行”（盘前/盘中）
    if stage in ("PREMARKET", "INTRADAY"):
        for ln in lines:
            if not _TRADE_ACTION_RE.search(ln):
                continue
            low = ln.lower()
            if any(neg in ln or neg in low for neg in _NEGATION):
                continue  # “无减仓/平仓信号”等否定语境，非一次动作
            if any(cond in ln or cond in low for cond in _CONDITIONAL):
                continue  # “开盘后检查：若…再议减仓”等条件/前瞻语境，非一次当下动作
            if "建议未执行" not in ln:
                v.append("L4 %s 阶段的交易动作行必须标注「建议未执行」：%r"
                         % (stage, ln.strip()[:50]))

    # L5（2026-07-27 撤销）：原要求正文含数据时间/来源标注。用户裁定：推送是给人看的
    # 交易便签（代码·动作·原因），溯源、as-of、数据质量问题属于**系统内部事务**，
    # 记入 run-summary / knowledge / escalations 并修复，不得推给用户。
    # 溯源验证本身照做（ACT-001/P1-P5 不变），只是不再出现在推送正文里。

    # L6 内部事务泄漏：来源域名/降级术语/系统升级项不得出现在推送正文。
    for leak in _INTERNAL_LEAK_MARKERS:
        if leak.lower() in markdown.lower():
            v.append("L6 推送正文含内部事务「%s」——问题应内部记录并修复，不是推给用户" % leak)

    return {"ok": not v, "violations": v}
