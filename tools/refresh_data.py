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

# 真实仓成本自账本派生（单一真源，CORE-001）：entry = 账本 cost（每股代理价），
# cost_basis = cost × qty（用户 2026-07-30 起「保留股数、成本随代理价浮动」口径）。
# 不再硬编码——账本是唯一真源，改账本即改视图。


def build_positions_table(positions, wallet):
    """纯函数：返回 (markdown_str, totals_dict)。可测试。"""
    rows, tot = [], {"real_mv": Decimal(0), "real_upnl": Decimal(0), "real_cost": Decimal(0),
                     "sim_mv": Decimal(0), "sim_upnl": Decimal(0)}
    for p in positions:
        sym, kind = p["symbol"], p["kind"]
        qty = Decimal(str(p["quantity"]))
        close = Decimal(str(p["last_close"]))
        if kind == "real":
            cost = Decimal(str(p["cost"]))            # 每股成本代理，来自账本 cost 列
            cost_basis = (cost * qty).quantize(Decimal("0.01"))
            mv = (qty * close).quantize(Decimal("0.01"))
            upnl = mv - cost_basis
            tot["real_mv"] += mv
            tot["real_upnl"] += upnl
            tot["real_cost"] += cost_basis
            entry_s = str(cost.quantize(Decimal("0.01")))
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
    # 2026-07-30 起为统一模拟盘：若仍存在真实仓则单列，否则只显示统一组合小计。
    real_line = ""
    if tot["real_mv"] != 0:
        real_line = ("**真实盘小计**: 市值 %s ｜ 未实现 %s（成本基 $%s，建议未执行，不入模拟钱包）\n"
                     % (tot["real_mv"], tot["real_upnl"], tot["real_cost"]))
        book_label = "模拟盘小计"
    else:
        book_label = "组合小计（统一模拟盘，8 仓）"
    content = (
        "# 持仓归一化视图（GENERATED — 勿手编，真源是 portfolio-ledger.md）\n\n"
        "生成器: tools/refresh_data.py ｜ 估值日: %s ｜ 状态: %s\n\n%s\n\n"
        "%s"
        "**%s**: 市值 %s ｜ 未实现 %s ｜ 现金 %s ｜ 总资产 %s\n\n"
        "> 2026-07-30 起全部持仓统一为模拟（demo）盘，系统主动交易全部 8 仓。entry = 账本 cost 列"
        "（每股成本代理）；无券商成交价者以官方收盘为代理（PWR/MP/BE/KTOS 按 2026-07-16 收盘，"
        "RMBS 按用户更正 114），股数保留、成本基 = cost×qty。真实成交价一到即在账本替换，本视图随之刷新。\n"
        % (w["valuation_date"], "VERIFIED", md, real_line, book_label,
           tot["sim_mv"], tot["sim_upnl"], w["cash"], w["total_assets"]))
    with open(out, "w", encoding="utf-8") as f:
        f.write(content)
    print("written %s (%d positions; real mv %s / sim mv %s)"
          % (out, len(s["positions"]), tot["real_mv"], tot["sim_mv"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
