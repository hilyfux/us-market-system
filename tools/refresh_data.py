#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh_data — 从账本+钱包生成 data/positions.md（归一化持仓视图，SYSTEM.md §13）。

单一账户（统一模拟盘，2026-07-31 起视图不再有任何 real/sim 区分）：
账本是唯一真源；本文件是**派生视图**。确定性、幂等；MORNING/POST_CLOSE 状态写入后运行。
用法：python3 tools/refresh_data.py   （在 state_root 下）
"""
import os
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "lib"))

import state as st  # noqa: E402


def build_positions_table(positions, wallet):
    """纯函数：返回 (markdown_str, totals_dict)。单一账户口径，无 real/sim 区分。可测试。"""
    rows, tot = [], {"mv": Decimal(0), "upnl": Decimal(0), "cost": Decimal(0)}
    for p in positions:
        sym = p["symbol"]
        qty = Decimal(str(p["quantity"]))
        cost_basis = Decimal(p["cost_basis"])
        mv = Decimal(p["market_value"]).quantize(Decimal("0.01"))
        upnl = Decimal(p["unrealized_pnl"]).quantize(Decimal("0.01"))
        tot["mv"] += mv
        tot["upnl"] += upnl
        tot["cost"] += cost_basis
        entry_s = str((cost_basis / qty).quantize(Decimal("0.01")))
        pct = (upnl / cost_basis * 100).quantize(Decimal("0.01"))
        rows.append("| %s | %s | %s | %s | %s | %s | %s | %s%% |" % (
            sym, qty, entry_s, cost_basis.quantize(Decimal("0.01")),
            Decimal(str(p["last_close"])), p["close_date"], mv, pct))
    hdr = ("| symbol | qty | avg_cost | cost_basis | last_close "
           "| close_date | market_value | upnl% |\n|---|---:|---:|---:|---:|---|---:|---:|")
    md = hdr + "\n" + "\n".join(rows)
    return md, tot


def main():
    s = st.load_all(ROOT)
    md, tot = build_positions_table(s["sim_positions"], s["wallet"])
    out = os.path.join(ROOT, "data", "positions.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w = s["wallet"]
    n = len(s["sim_positions"])
    content = (
        "# 持仓归一化视图（GENERATED — 勿手编，真源是 portfolio-ledger.md）\n\n"
        "生成器: tools/refresh_data.py ｜ 估值日: %s ｜ 状态: %s\n\n%s\n\n"
        "**组合小计（%d 仓）**: 市值 %s ｜ 未实现 %s ｜ 现金 %s ｜ 总资产 %s\n\n"
        "> 单一账户。avg_cost = cost_basis ÷ qty（账本派生）。标准初始仓 = 每标的 $10,000"
        "（selection.BASE_INITIAL_PCT；偏离须带 SIZE_EXCEPTION 标记，否则 preflight C7 报错）。\n"
        % (w["valuation_date"], "VERIFIED", md, n,
           tot["mv"], tot["upnl"], w["cash"], w["total_assets"]))
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    print("written %s (%d positions; mv %s)" % (out, n, tot["mv"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
