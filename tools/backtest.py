#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest (runner) — 读 data/decision-log.jsonl，跑 lib/backtest 引擎，写 data/backtest-report.md。

只做 I/O 与编排；所有计算在 lib/backtest（纯函数、单测锁定）。
用法：python3 tools/backtest.py
诚实性：报告顶部显式打印样本充分性；样本不足时指标标注为「方向参考，非 edge」。
"""
import json
import os
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "lib"))
import backtest as bt  # noqa: E402
import state as st      # noqa: E402


def load_log(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for ln in f:
            ln = ln.strip()
            if ln:
                rows.append(json.loads(ln))
    return rows


def main():
    log = os.path.join(ROOT, "data", "decision-log.jsonl")
    rows = load_log(log)
    equity_rows = sorted([r for r in rows if r.get("type") == "equity"], key=lambda r: r["date"])
    trades = [r for r in rows if r.get("type") == "trade"]
    decisions = [r for r in rows if r.get("type") == "decision"]

    equity = [r["total_assets"] for r in equity_rows]
    bench = [r["benchmark_spy"] for r in equity_rows if "benchmark_spy" in r]
    res = bt.run(equity, trades, benchmark=bench if len(bench) == len(equity) else None)

    s = res["sample"]
    t = res["trades"]
    pf = t["profit_factor"]
    pf_s = "∞" if pf == Decimal("Infinity") else str(pf)
    # 事件后 vs 事件前入场：方向性对照（决策数据挖掘）
    ev = [d for d in decisions if d.get("entry_type") == "event_confirmed"]
    pre = [d for d in decisions if d.get("entry_type") in ("pre_event", "pre_event_or_migrated")]

    lines = []
    lines.append("# 回测/绩效报告（GENERATED — tools/backtest.py ｜ 引擎 lib/backtest.py）\n")
    lines.append("> **样本充分性：%s**" % s["verdict"])
    lines.append("> 成交 %d 笔（阈值 %d）｜权益点 %d（阈值 %d）。以下为**已发生决策**的确定性度量，"
                 "非预测、非已验证 edge。\n" % (s["n_trades"], s["min_trades"],
                                              s["n_equity_points"], s["min_equity_points"]))

    lines.append("## 权益（统一模拟盘口径）\n")
    lines.append("| 指标 | 值 |")
    lines.append("|---|---:|")
    lines.append("| 总收益 | %s%% |" % res["total_return_pct"])
    lines.append("| 最大回撤 | %s%% |" % res["max_drawdown_pct"])
    if "vs_benchmark" in res:
        vb = res["vs_benchmark"]
        lines.append("| 组合收益 vs SPY | %s%% vs %s%%（超额 %s pp） |"
                     % (vb["portfolio_return"], vb["benchmark_return"], vb["excess_pp"]))
    lines.append("")

    lines.append("## 成交统计（已平仓）\n")
    lines.append("| 指标 | 值 |")
    lines.append("|---|---:|")
    lines.append("| 笔数 / 胜 / 负 | %d / %d / %d |" % (t["n"], t["wins"], t["losses"]))
    lines.append("| 胜率 | %s%% |" % t["win_rate"])
    lines.append("| 净已实现 | $%s |" % t["net_realized"])
    lines.append("| 盈亏比(profit factor) | %s |" % pf_s)
    lines.append("| 平均盈 / 平均亏 | $%s / $%s |" % (t["avg_win"], t["avg_loss"]))
    lines.append("| 期望/笔 | $%s |" % t["expectancy"])
    lines.append("")

    lines.append("## 决策挖掘：事件后入场 vs 事件前入场\n")
    ev_syms = list(dict.fromkeys(d["symbol"] for d in ev))
    pre_syms = list(dict.fromkeys(d["symbol"] for d in pre))
    lines.append("- 事件后确认入场（L-010）：%d 銘柄 — %s" % (len(ev_syms), ", ".join(ev_syms) or "—"))
    lines.append("- 事件前/迁移入场：%d 銘柄 — %s" % (len(pre_syms), ", ".join(pre_syms) or "—"))
    lines.append("- 观察（方向性，样本不足）：唯一已平仓且盈利的是事件后入场的 ABT；"
                 "事件前入场组普遍深浮亏（BE/RMBS/MP）。这与 ACT-005/L-010 一致，但 n=1 不足以证实。\n")

    # 个股交易指标（per-stock）：从账本读持仓 + 决策日志的已实现
    realized_by_sym = {}
    for tr in trades:
        realized_by_sym[tr["symbol"]] = realized_by_sym.get(tr["symbol"], Decimal("0")) + Decimal(str(tr.get("realized", 0)))
    try:
        positions = [p for p in st.load_positions(ROOT) if p.get("kind") == "sim"]
    except Exception:
        positions = []
    if positions:
        lines.append("## 个股交易指标（per-stock）\n")
        lines.append("| 代码 | 成本基 | 市值 | 未实现 | 未实现% | 已实现 |")
        lines.append("|---|---:|---:|---:|---:|---:|")
        for p in positions:
            cb = Decimal(str(p["cost_basis"])); mv = Decimal(str(p["market_value"]))
            un = Decimal(str(p["unrealized_pnl"]))
            pct = (un / cb * 100).quantize(Decimal("0.01")) if cb else Decimal("0")
            rz = realized_by_sym.get(p["symbol"], Decimal("0"))
            lines.append("| %s | %.2f | %.2f | %+.2f | %+.2f%% | %s |"
                         % (p["symbol"], cb, mv, un, pct, ("$%.2f" % rz) if rz else "—"))
        lines.append("")

    lines.append("## 下一步：让回测有意义\n")
    lines.append("- 阈值：≥%d 笔已平仓成交 + ≥%d 权益点后，本报告的胜率/盈亏比/回撤才具统计意义。"
                 % (s["min_trades"], s["min_equity_points"]))
    lines.append("- 累积方式：每次 MORNING/POST_CLOSE 成交与结算自动 append 到 data/decision-log.jsonl；"
                 "复盘据此按 ACT 规则的 rollback 指标验证或回滚。")

    out = os.path.join(ROOT, "data", "backtest-report.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print("written %s" % out)
    print("sufficient=%s trades=%d equity_points=%d total_return=%s%% maxDD=%s%%"
          % (s["sufficient"], t["n"], len(equity), res["total_return_pct"], res["max_drawdown_pct"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
