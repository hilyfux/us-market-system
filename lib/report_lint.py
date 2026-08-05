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
                     2026-08-04 扩展：机制词与规则代号（硬门/门槛/ACT-xxx/L-xxx/lint 等）
                     同属内部事务——推送说人话，拒绝理由写事实本身。
  L7 账务透明        （2026-07-31 用户裁定）正文必须含账户行（「总资产」+当日盈亏）；
                     每条持仓行（^TICKER ·|｜ 开头且含 §4 动作词）必须含「成本」、
                     当日字段（今日/当日/昨日）与「累计」百分比。推送没有账目=用户看不见钱。
  L8 盈亏色分        （2026-08-04 用户裁定：账目数据不得裸摆、须整形+着色）持仓行与
                     账户行中的盈亏百分比必须用企业微信 `<font color>` 标注——
                     正=warning（橙红）、负=info（绿）、零=comment（灰），东亚惯例红涨绿跌。
                     行内含百分比但无颜色标签即拒绝入队。配套：L2 篇幅改按**可见字符**计
                     （剔除 font 标签与 ** 加粗记号——格式标记不挤占内容预算）。

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
# L7 持仓行识别：行首为 1-5 位大写代码（可 ** 加粗）+ 分隔符（· 或 ｜ 或空格+·）。高精确：
# emoji 行（🚨/📊）、「成交：」「账户：」「└ 原因」等不匹配，不会被误加账务要求。
_POSITION_LINE_RE = re.compile(r"^(?:\*\*)?[A-Z]{1,5}(?:\*\*)?\s*[·｜]")
# L8 着色检查：百分比形态（供持仓/账户行检测「有百分比却无颜色」）。
_PCT_RE = re.compile(r"[+\-−]?\d+(?:\.\d+)?%")
# L2 可见字符口径：企业微信 font 色彩标签与 markdown 加粗记号不计入篇幅。
_MARKUP_RE = re.compile(r"</?font[^>]*>|\*\*")
# 内部事务标记（2026-07-27，L6）：这些词属于系统内部（溯源/降级/升级项），
# 出现在推送正文即违规——用户只要「代码·动作·原因」，问题内部解决。
# 2026-08-04 用户裁定扩展：机制词与规则代号也属内部事务——推送说人话，
# 「不合条件」写成事实本身（如「财报临近，暂不买」），不写「未过 XX 门」。
# 选词保持高精确（不收裸「门」——「热门」等日常词会误伤）。
_INTERNAL_LEAK_MARKERS = ("stockanalysis.com", "roic.ai", "数据时间", "数据来源",
                          "MARKET_DATA_DEGRADED", "STATE_INTEGRITY_FAILURE",
                          "ENQUEUE_PATH_UNAVAILABLE", "STALE_VALUATION",
                          "数据降级", "未核实", "无法核实", "延迟>",
                          "ACT-0", "CORE-0", "L-00", "硬门", "门槛",
                          "替换门", "事件门", "集中度门", "评分门", "lint")


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
    """字数 = 非空白**可见**字符数（2026-08-04：剔除 font 色彩标签与 ** 加粗记号。
    色分是用户要求的必需格式，格式标记不得挤占内容篇幅预算）。"""
    return len(re.sub(r"\s+", "", _MARKUP_RE.sub("", markdown)))


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

    # L7 账务透明（2026-07-31 用户裁定：推送必须让用户看见钱）
    if "总资产" not in markdown:
        v.append("L7 缺账户行：正文必须含「总资产」（含当日盈亏）——推送没有账目=用户看不见钱")
    for ln in lines:
        if not _POSITION_LINE_RE.match(ln.strip()):
            continue
        if not _VALID_ACTION_RE.search(ln):
            continue  # 非动作行（如财报前瞻行）不作账务要求
        miss = []
        if "成本" not in ln:
            miss.append("成本")
        if not any(k in ln for k in ("今日", "当日", "昨日")):
            miss.append("今日/当日")
        if "累计" not in ln or "%" not in ln:
            miss.append("累计%")
        if miss:
            v.append("L7 持仓行缺账务字段 %s：%r" % ("/".join(miss), ln.strip()[:50]))

    # L8 盈亏色分（2026-08-04 用户裁定：红涨绿跌着色，数据不得裸摆）
    for ln in lines:
        s = ln.strip()
        is_pos = bool(_POSITION_LINE_RE.match(s) and _VALID_ACTION_RE.search(s))
        is_acct = "总资产" in s
        if not (is_pos or is_acct):
            continue  # 📊/🚨/└ 原因行等不作着色要求
        if _PCT_RE.search(s) and "<font color=" not in s:
            v.append("L8 盈亏未着色：持仓/账户行的百分比须用 <font color> 红涨绿跌标注：%r" % s[:50])

    return {"ok": not v, "violations": v}
