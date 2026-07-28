#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh_data — 从账本+钱包生成 data/positions.md（归一化持仓视图，SYSTEM.md §13）。

账本仍是唯一真源；本文件是**派生视图**：真实与模拟持仓同一套列
（含真实仓的市值/盈亏——账本真实表原本缺这几列，分析时每次现算易错）。
确定性、幂等；MORNING/POST_CLOSE 状态写入后运行。
用法：python3 tools/refresh_data.py   （在 state_root 下）
"""
import os
import sys
from decimal import Decimal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "lib"))

import state as st  # noqa: E402

# 真实仓成本（用户确认 $10k/仓；PWR/MP/BE/KTOS 为入场日收盘代理价，RMBS 为账载 115.00）
REAL_COST_BASIS = Decimal("10000")
REAL_ENTRY = {"PWR": ("666.33", "PROXY"), "MP": ("53.00", "PROXY"),
              "BE": ("244.61", "PROXY"), "KTOS": ("48.19", "PROXY"),
              "RMBS": ("115.00", "RECORDED")}


def build_positions_table(positions, wallet):
    """纯函数：返回 (markdown_str, totals_dict)。可测试。"""
    rows, tot = [], {"real_mv": Decimal(0), "real_upnl": Decimal(0),
                     "sim_mv": Decimal(0), "sim_upnl": Decimal(0)}
    for p in positions:
        sym, kind = p["symbol"], p["kind"]
        qty = Decimal(str(p["quantity"]))
        close = Decimal(str(p["last_close"]))
        if kind == "real":
            entry, basis_kind = REAL_ENTRY[sym]
            cost_basis = REAL_COST_BASIS
            mv = (qty * close).quantize(Decimal("0.01"))
            upnl = mv - cost_basis
            tot["real_mv"] += mv
            tot["real_upnl"] += upnl
            entry_s = "%s(%s)" % (entry, basis_kind)
        else:
            cost_basis = Decimal(p["cost_basis"])
            mv = Decimal(p["market_value"]).quantize(Decimal("0.01"))
            upnl = Decimal(p["unrealized_pnl"]).quantize(Decimal("0.01"))
            tot["sim_mv"] += mv
            tot["sim_upnl"] += upnl
            entry_s = str((cost_basis / qty).quantize(Decimal("0.01")))
        pct = (upnl / cost_basis * 100).quantize(Decimal("0.01"))
        rows.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s%% |" % (
            sym, kind, qty, entry_s, cost_basis.quantize(Decimal("0.01")),
            close, p["close_date"], mv, pct))
    hdr = ("| symbol | kind | qty | entry(basis) | cost_basis | last_close "
           "| close_date | market_value | upnl% |\n|---|---|---:|---|---:|---:|---|---:|---:|")
    md = hdr + "\n" + "\n".join(rows)
    return md, tot


def main():
    s = st.load_all(ROOT)
    md, tot = build_positions_table(s["positions"], s["wallet"])
    out = os.path.join(ROOT, "data", "positions.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    w = s["wallet"]
    content = (
        "# 持仓归一化视图（GENERATED — 勿手编，真源是 portfolio-ledger.md）\n\n"
        "生成器: tools/refresh_data.py ｜ 估值日: %s ｜ 状态: %s\n\n%s\n\n"
        "**真实盘小计**: 市值 %s ｜ 未实现 %s（成本 $50,000，动作一律建议未执行，不入模拟钱包）\n"
        "**模拟盘小计**: 市值 %s ｜ 未实现 %s ｜ 现金 %s ｜ 总资产 %s\n\n"
        "> 真实仓 entry 标注 PROXY = 入场日官方收盘代理价（非券商成交价，用户 2026-07-27 授权），"
        "RECORDED = 账载成交价。真实成交价一到即替换。\n"
        % (w["valuation_date"], "VERIFIED", md,
           tot["real_mv"], tot["real_upnl"], tot["sim_mv"], tot["sim_upnl"],
           w["cash"], w["total_assets"]))
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    print("written %s (%d positions; real mv %s / sim mv %s)"
          % (out, len(s["positions"]), tot["real_mv"], tot["sim_mv"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
