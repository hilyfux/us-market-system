#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
learning —— 自我修正闭环（用户 2026-08-15 裁定：系统必须能自己发现失败并改进）。

## 为什么需要这个模块

系统原有的"反思"装置很齐全（25 条教训、每日复盘、playbook 昇格基准、preflight 36 项、
selftest 218 项），却在 2026-08-05～08-14 连续五次替换中**全程报告 ok=true**，
而事后手工核查发现可测的四次全部劣后。装置齐全却失灵，根因是四个结构缺陷：

1. **卖出即失明**：仓位一平仓就从状态文件消失，日循环再也不去取它的价格。
   于是"卖掉的比买进的涨得好"这个信息量最大的信号，**在结构上不可见**。
   L-020 曾登记"追踪 GEV/LLY/NVDA 卖出后表现"——但那是**写给自己的备忘**，
   备忘不会执行（与 L-023「从未被构造过的守卫等于不存在」同型）。
2. **只验账、不验判断**：preflight 把 C1–C7 校到分位，却没有任何一项检查能因
   "策略在亏"而变红。账目被 36 路监视，判断力无人监视。
3. **打分从不被打分**：九维评分被用了 13 次，一次也没有被对照结果评估过。
   建仓时不登记**可证伪的预测**，所以这个分数**永远不可能错**——不可能错的分数不可能改进。
4. **教训停在散文**：已代码化的 L-022 此后零违反；停在散文的 L-010 被违反三次。
   散文教训被当成"已生效的对策"，实际是未执行的意图。

## 本模块提供的机制（对治上述四条）

- `Claim`：决策时登记**可证伪**的预测（指标 + 阈值 + 期限 + 裁定日）。
  `register_claim()` **拒绝**不可证伪的主张——没有裁定日或没有阈值即抛错。
- `due_claims()` / `adjudicate()`：到期机械裁定，命中与否不由叙述决定。
- `overdue_claims()`：**到期未裁定 = 硬升级**。这是整个闭环的牙齿：
  它把"忘了复检"从沉默失败变成响亮失败（对治缺陷 1 与 3）。
- `ShadowBook`：已平仓标的继续被日常定价，"卖出 vs 买入"自动可比（对治缺陷 1）。
- `scorecard()`：判断质量记分卡，**样本不足时显式返回"判定不能"而非红**
  （复用 backtest.MIN_TRADES_FOR_SIGNIFICANCE，防止把噪声当 edge —— 这正是
  2026-08-15 我自己在 4 个观测上改核心规则时犯的错，机器化以防复发）。
- `lesson_enforcement()`：每条教训必须声明 CODIFIED（附测试名）或 PROSE_ONLY（附理由）；
  未声明即缺陷。散文教训作为**已知缺口**可见，而不是被当成已生效的控制（对治缺陷 4）。

## 设计约束

- 纯函数 + 显式 IO 边界（低耦合）：本模块只认 dict/JSONL，不直接读账本、不发网络。
- **VOID 必须带理由且计入记分卡**：否则被裁判的一方可以把不利主张悄悄作废。
- 时间用交易日计（与失效线口径一致），日历由调用方注入（不在此重实现）。
"""
import json
import os
import re
from datetime import date, datetime
from decimal import Decimal
from typing import Callable, Dict, List, Optional, Sequence

CLAIMS_FILE = "data/claims.jsonl"
SHADOW_FILE = "data/shadow-book.jsonl"

# 主张状态。VOID 是显式的、带理由的、且被计数的——不是静默丢弃。
OPEN, HIT, MISS, VOID = "OPEN", "ADJUDICATED_HIT", "ADJUDICATED_MISS", "VOID"
TERMINAL = (HIT, MISS, VOID)

# 决策类别。replacement 是本次事故的类别，单列以便单独记分。
KIND_REPLACEMENT = "replacement"
KIND_ENTRY = "entry"
KIND_EXIT = "exit"
KIND_FORECAST = "forecast"
KIND_RULE = "rule"          # 规则本身的有效性主张（如 ACT-008 是否改善结果）
KINDS = (KIND_REPLACEMENT, KIND_ENTRY, KIND_EXIT, KIND_FORECAST, KIND_RULE)

# 教训的执行状态。
CODIFIED, PROSE_ONLY = "CODIFIED", "PROSE_ONLY"


class NotFalsifiable(ValueError):
    """主张不可证伪 —— 拒绝登记。不可证伪的主张是叙述，不是预测。"""


def _d(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _iso(d) -> str:
    if isinstance(d, (date, datetime)):
        return d.strftime("%Y-%m-%d")
    return str(d)


# --------------------------------------------------------------------------
# 1. 主张（Claim）—— 决策时登记可证伪的预测
# --------------------------------------------------------------------------

def make_claim(claim_id: str, kind: str, made_on, subject: str,
               metric: str, threshold, direction: str,
               horizon_sessions: int, adjudicate_on,
               rationale: str = "", baseline: Optional[str] = None) -> Dict[str, object]:
    """
    构造一条可证伪的主张。任一要素缺失即抛 NotFalsifiable —— 这是本模块的核心约束：
    **系统不允许做出无法被判错的决策**。

    metric/direction/threshold 三者共同定义「什么结果算我错了」：
      例：替换 LLY->TSM，metric="relative_return_pct_vs_sold"、direction=">"、threshold=0
      读作「TSM 在 horizon 内的收益率必须高于被卖出的 LLY，否则本次替换判 MISS」。
    """
    if kind not in KINDS:
        raise NotFalsifiable("未知决策类别 %r（可选：%s）" % (kind, "/".join(KINDS)))
    if not metric or direction not in (">", ">=", "<", "<="):
        raise NotFalsifiable("必须给出 metric 与比较方向（>,>=,<,<=）——否则无法判错")
    if threshold is None:
        raise NotFalsifiable("必须给出阈值——没有阈值的预测永远不会错")
    if not adjudicate_on:
        raise NotFalsifiable("必须给出裁定日——没有到期日的预测不会被复检（L-020 型缺陷）")
    if horizon_sessions is None or int(horizon_sessions) <= 0:
        raise NotFalsifiable("必须给出正的交易日期限")
    return {
        "claim_id": claim_id,
        "kind": kind,
        "made_on": _iso(made_on),
        "subject": subject,
        "baseline": baseline,
        "metric": metric,
        "direction": direction,
        "threshold": str(_d(threshold)),
        "horizon_sessions": int(horizon_sessions),
        "adjudicate_on": _iso(adjudicate_on),
        "status": OPEN,
        "rationale": rationale,
        "observed": None,
        "adjudicated_on": None,
        "void_reason": None,
    }


def adjudicate(claim: Dict[str, object], observed, on_date) -> Dict[str, object]:
    """
    机械裁定：把观测值与阈值按 direction 比较。命中与否**不取决于叙述**。
    已终结的主张不可重裁（防止事后改判）。
    """
    if claim["status"] in TERMINAL:
        raise ValueError("主张 %s 已终结（%s），不得重裁" % (claim["claim_id"], claim["status"]))
    obs, thr, dirn = _d(observed), _d(claim["threshold"]), claim["direction"]
    hit = {">": obs > thr, ">=": obs >= thr, "<": obs < thr, "<=": obs <= thr}[dirn]
    out = dict(claim)
    out["observed"] = str(obs)
    out["status"] = HIT if hit else MISS
    out["adjudicated_on"] = _iso(on_date)
    return out


def void_claim(claim: Dict[str, object], reason: str, on_date) -> Dict[str, object]:
    """
    作废一条主张。**理由必填**且会进入记分卡的 void 计数——
    否则被评判的一方可以把不利主张悄悄作废，记分卡就失去意义。
    """
    if not reason or not reason.strip():
        raise ValueError("VOID 必须带理由（无理由作废＝静默逃避裁定）")
    if claim["status"] in TERMINAL:
        raise ValueError("主张 %s 已终结，不得再作废" % claim["claim_id"])
    out = dict(claim)
    out["status"] = VOID
    out["void_reason"] = reason.strip()
    out["adjudicated_on"] = _iso(on_date)
    return out


def due_claims(claims: Sequence[Dict[str, object]], today) -> List[Dict[str, object]]:
    """
    今天（含）之前到期且仍 OPEN 的主张——本次运行必须裁定的清单。

    口径点检（2026-08-15 审计 B1）：adjudicate_on 本身在登记时由交易日历推导落定，
    本函数只判「日期已到」，不存在暦日/交易日混同、不会早发火；周末运行列出周五
    到期的主张属预期（用上一官方收盘裁定即可），故无需交易日注入口。
    """
    t = _iso(today)
    return [c for c in claims if c["status"] == OPEN and c["adjudicate_on"] <= t]


def overdue_claims(claims: Sequence[Dict[str, object]], today,
                   grace_sessions: int = 1,
                   sessions_between: Optional[Callable[[date, date], int]] = None
                   ) -> List[Dict[str, object]]:
    """
    **闭环的牙齿**：到期后超过 grace 仍未裁定的主张。
    preflight 把它升级为硬 escalation —— 「忘了复检」从此是响亮失败，不是沉默失败。
    这正是 L-020（追踪 GEV/NVDA 卖出后表现）失效的原因：它只是备忘，没有到期强制。

    grace_sessions 的口径是**交易日**（与失效线一致，见模块头「时间用交易日计」）。
    `sessions_between(due_date, today) -> int` 是交易日计数器注入口
    （如 `market_core.TradingCalendar.trading_days_between`，日历由调用方注入、不在此重实现）。
    **未注入时退化为暦日差**——该退化偏严（周末/假日也被计入），会把周五到期的主张
    在周日误判逾期并误阻断健全的 MORNING/POST_CLOSE（2026-08-15 审计 B1，可用性回归）；
    仅作无日历环境的兜底，生产路径（preflight W6）必须注入交易日历。
    """
    t = datetime.strptime(_iso(today), "%Y-%m-%d").date()
    out = []
    for c in claims:
        if c["status"] != OPEN:
            continue
        due = datetime.strptime(c["adjudicate_on"], "%Y-%m-%d").date()
        elapsed = (sessions_between(due, t) if sessions_between is not None
                   else (t - due).days)
        if elapsed > grace_sessions:
            out.append(c)
    return out


# --------------------------------------------------------------------------
# 2. 影の帳簿（ShadowBook）—— 卖出后不失明
# --------------------------------------------------------------------------

def shadow_entry(symbol: str, exit_date, exit_price, replaced_by: Optional[str],
                 entry_price_of_replacement=None) -> Dict[str, object]:
    """已平仓标的进入影子帐簿：继续被定价，用于自动计算「卖出 vs 买入」。"""
    return {
        "symbol": symbol,
        "exit_date": _iso(exit_date),
        "exit_price": str(_d(exit_price)),
        "replaced_by": replaced_by,
        "replacement_entry_price": (str(_d(entry_price_of_replacement))
                                    if entry_price_of_replacement is not None else None),
    }


def shadow_delta(entry: Dict[str, object], sold_now, bought_now) -> Dict[str, object]:
    """
    卖出标的与买入标的自入替日起的收益率之差（pp）。
    正数 = 替换有效；负数 = 「什么都不做」更好。**这是替换方法论唯一的直接证据。**
    """
    sold_ret = (_d(sold_now) / _d(entry["exit_price"]) - 1) * 100
    out = {"symbol": entry["symbol"], "replaced_by": entry["replaced_by"],
           "sold_return_pct": sold_ret, "bought_return_pct": None, "delta_pp": None}
    if entry.get("replacement_entry_price") and bought_now is not None:
        bought_ret = (_d(bought_now) / _d(entry["replacement_entry_price"]) - 1) * 100
        out["bought_return_pct"] = bought_ret
        out["delta_pp"] = bought_ret - sold_ret
    return out


# --------------------------------------------------------------------------
# 3. 记分卡 —— 样本不足时说「判定不能」，不说「有效」也不说「失败」
# --------------------------------------------------------------------------

def scorecard(claims: Sequence[Dict[str, object]], kind: Optional[str] = None,
              min_sample: int = 20) -> Dict[str, object]:
    """
    判断质量记分卡。**关键设计**：样本不足时 verdict 为「判定不能」，
    既不宣告方法有效、也不宣告方法失败。

    2026-08-15 的教训（L-026）：我在 4 个观测、3–7 日窗口上判定「替换方法论失败」
    并冻结引擎，而本仓库自己的 backtest.MIN_TRADES_FOR_SIGNIFICANCE=20 与 playbook
    的「≥3 独立交易日或 5 样本、禁止单日过拟合」早已写明不可如此。规则写在文件里
    没能阻止违反——所以此处把它变成**返回值**，让调用方无法在不看见它的情况下下结论。
    """
    sel = [c for c in claims if kind is None or c["kind"] == kind]
    hits = [c for c in sel if c["status"] == HIT]
    misses = [c for c in sel if c["status"] == MISS]
    voids = [c for c in sel if c["status"] == VOID]
    opens = [c for c in sel if c["status"] == OPEN]
    n = len(hits) + len(misses)
    sufficient = n >= min_sample
    rate = (Decimal(len(hits)) / Decimal(n) * 100) if n else None
    return {
        "kind": kind or "ALL",
        "n_adjudicated": n,
        "n_hit": len(hits),
        "n_miss": len(misses),
        "n_void": len(voids),
        "n_open": len(opens),
        "hit_rate_pct": rate,
        "min_sample": min_sample,
        "sufficient": sufficient,
        "verdict": ("统计充分" if sufficient else
                    "样本不足（%d/%d）—— 判定不能：不得据此宣告方法有效或失败（L-026）" % (n, min_sample)),
    }


# --------------------------------------------------------------------------
# 4. 教训执行状态 —— 散文教训必须作为已知缺口可见
# --------------------------------------------------------------------------

def lesson_enforcement(registry: Dict[str, Dict[str, str]],
                       lesson_ids: Sequence[str]) -> Dict[str, object]:
    """
    每条教训必须在 registry 里声明 CODIFIED（附 test 名）或 PROSE_ONLY（附 reason）。
    未声明 = 缺陷（既非已生效也未被承认为缺口）。

    依据：已代码化的 L-022 此后零违反；停在散文的 L-010 被违反三次。
    教训是否被遵守，取决于它是否变成了可执行的检查。
    """
    undeclared, codified, prose = [], [], []
    for lid in lesson_ids:
        rec = registry.get(lid)
        if not rec or rec.get("status") not in (CODIFIED, PROSE_ONLY):
            undeclared.append(lid)
        elif rec["status"] == CODIFIED:
            if not rec.get("test"):
                undeclared.append(lid)      # 声称已代码化却指不出测试 = 未声明
            else:
                codified.append(lid)
        else:
            if not rec.get("reason"):
                undeclared.append(lid)      # 声称散文却说不出为何不可代码化
            else:
                prose.append(lid)
    total = len(lesson_ids)
    return {
        "total": total,
        "codified": len(codified),
        "prose_only": len(prose),
        "undeclared": undeclared,
        "coverage_pct": (Decimal(len(codified)) / Decimal(total) * 100) if total else None,
        "ok": not undeclared,
    }


# --------------------------------------------------------------------------
# 4.5 替换成交 ↔ claim 的即时耦合（L-020 根穴的恒久封堵，2026-08-15）
# --------------------------------------------------------------------------
#
# 现有 5 条 claim 全部是事后人工遡及登记的：「替换成交」与「claim 登记」之间
# 没有任何机械耦合，下次漏登记不会有任何检查变红——L-020 的根穴仍然敞着。
# 此处提供纯函数：从账本成交表识别「替换对」＝同一 executed 日同时存在
# 平仓 与 建仓；每对必须有 claim `RPL-<日>-<卖>-<买>`，缺失即孤儿替换，
# preflight 将其升级为硬 ERROR（ORPHAN_REPLACEMENT）。
# 显式排除：减仓（部分止盈/止损）与不成对的单腿成交不是替换，不得误伤
# （例：ETN 2026-08-14 止盈-减仓50% 与 LLY→TSM 替换同日，前者不参与配对）。

TRADE_OPEN, TRADE_CLOSE = "建仓", "平仓"
_TRADE_ID_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9.\-]*-.+-\d{2}$")
_TRADE_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_ledger_trades(ledger_text: str) -> List[Dict[str, str]]:
    """
    最小账本成交解析（纯函数，输入为 portfolio-ledger.md 全文）。
    只认「| trade_id | 日期 | 代码 | 动作 | … |」形状的表行——trade_id 必须匹配
    `YYYY-MM-DD-SYM-…-NN`，其余行（持仓表、表头、分隔线、散文）全部忽略。
    刻意不解析数量/价格：替换配对只需要 (日期, 代码, 动作)（低耦合）。
    """
    out = []
    for line in ledger_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        if not _TRADE_ID_RE.match(cells[0]) or not _TRADE_DATE_RE.match(cells[1]):
            continue
        out.append({"trade_id": cells[0], "date": cells[1],
                    "symbol": cells[2], "action": cells[3]})
    return out


# 替换标记：CLOSED 持仓 note 固定以「**确定性替换退出（trade <平仓trade_id>，…」开头
# （实数据 5 条全部如此，模板义务）。标记是账本自己对「这笔平仓是替换退出」的声明。
_REPLACEMENT_MARKER_RE = re.compile(
    r"确定性替换退出（trade\s+(\d{4}-\d{2}-\d{2}-[A-Z][A-Z0-9.\-]*-平仓-\d{2})")


def parse_replacement_markers(ledger_text: str) -> List[str]:
    """
    从账本全文提取被标记为**替换退出**的平仓 trade_id（升序、去重）。

    为什么需要标记（2026-08-15 审计 B3）：仅按「同日 平仓+建仓」配对，会把无关的
    素的平仓（规则性主动退出）与同日别标的的新建仓误配成替换对，进而向不存在的
    claim 要求登记 → ERROR 误阻断健全运行（可用性回归）。标记把配对锚在账本自己
    声明的替换事实上。写 CLOSED note（含标记）与登记 claim 是两个独立动作——
    漏登 claim 时标记仍在，ORPHAN_REPLACEMENT 的检出力不丢。
    """
    return sorted(set(_REPLACEMENT_MARKER_RE.findall(ledger_text)))


def replacement_pairs(trades: Sequence[Dict[str, str]],
                      replacement_close_ids: Optional[Sequence[str]] = None
                      ) -> List[Dict[str, str]]:
    """
    识别替换对：同一成交日同时存在 平仓 与 建仓，按表内出现顺序一一配对。
    减仓与孤立的单腿成交不构成替换（显式排除，防误伤）。输出按日期升序、确定性。

    replacement_close_ids（2026-08-15 审计 B3）：若给出（来自 parse_replacement_markers），
    **只有其中的平仓参与配对**——素的平仓＋同日无关建仓不再被误配为替换对。
    None = 全部平仓参与（旧口径，仅供合成数据单测；生产路径 preflight 必须传标记）。
    """
    allowed = None if replacement_close_ids is None else set(replacement_close_ids)
    by_date: Dict[str, Dict[str, List[str]]] = {}
    for t in trades:
        if (allowed is not None and t["action"] == TRADE_CLOSE
                and t["trade_id"] not in allowed):
            continue
        d = by_date.setdefault(t["date"], {TRADE_CLOSE: [], TRADE_OPEN: []})
        if t["action"] in (TRADE_CLOSE, TRADE_OPEN):
            d[t["action"]].append(t["symbol"])
    pairs = []
    for day in sorted(by_date):
        for sold, bought in zip(by_date[day][TRADE_CLOSE], by_date[day][TRADE_OPEN]):
            pairs.append({"date": day, "sold": sold, "bought": bought,
                          "claim_id": "RPL-%s-%s-%s" % (day, sold, bought)})
    return pairs


def orphan_replacements(trades: Sequence[Dict[str, str]],
                        claim_ids: Sequence[str],
                        replacement_close_ids: Optional[Sequence[str]] = None
                        ) -> List[str]:
    """
    返回缺失 claim 登记的替换对 claim_id（升序、去重）。空列表 = 无孤儿。
    这是 preflight ORPHAN_REPLACEMENT 检查的唯一根据（纯函数，便于单测）。
    replacement_close_ids 同 replacement_pairs（B3：生产路径必须传标记，防误配）。
    """
    known = set(claim_ids)
    out = []
    for p in replacement_pairs(trades, replacement_close_ids):
        if p["claim_id"] not in known and p["claim_id"] not in out:
            out.append(p["claim_id"])
    return out


# --------------------------------------------------------------------------
# 5. IO 边界（JSONL，原子追加）
# --------------------------------------------------------------------------

def load_jsonl(path: str) -> List[Dict[str, object]]:
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def append_jsonl(path: str, record: Dict[str, object]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())


def rewrite_jsonl(path: str, records: Sequence[Dict[str, object]]) -> None:
    """裁定后整体重写（先 .tmp 再 rename，原子）。"""
    tmp = path + ".tmp"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(tmp, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)


def register_claim(root: str, claim: Dict[str, object]) -> Dict[str, object]:
    """登记一条主张（重复 claim_id 拒绝，防止同一决策被登记两次冲淡记分卡）。"""
    path = os.path.join(root, CLAIMS_FILE)
    existing = {c["claim_id"] for c in load_jsonl(path)}
    if claim["claim_id"] in existing:
        raise ValueError("claim_id 重复：%s" % claim["claim_id"])
    append_jsonl(path, claim)
    return claim


def load_claims(root: str) -> List[Dict[str, object]]:
    return load_jsonl(os.path.join(root, CLAIMS_FILE))


def save_claims(root: str, claims: Sequence[Dict[str, object]]) -> None:
    rewrite_jsonl(os.path.join(root, CLAIMS_FILE), claims)


def load_shadow(root: str) -> List[Dict[str, object]]:
    return load_jsonl(os.path.join(root, SHADOW_FILE))


def summary(root: str, today,
            sessions_between: Optional[Callable[[date, date], int]] = None
            ) -> Dict[str, object]:
    """给 run-summary / preflight 用的一次性汇总。sessions_between 同 overdue_claims
    （交易日计数器注入口，生产路径应注入交易日历，见 B1 口径说明）。"""
    claims = load_claims(root)
    return {
        "n_claims": len(claims),
        "due_today": [c["claim_id"] for c in due_claims(claims, today)],
        "overdue": [c["claim_id"] for c in overdue_claims(
            claims, today, sessions_between=sessions_between)],
        "replacement": scorecard(claims, KIND_REPLACEMENT),
        "all": scorecard(claims),
        "shadow_tracked": len(load_shadow(root)),
    }
