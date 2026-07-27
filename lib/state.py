#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
state — 状态文件解析。让校验能真正跑在真实文件上，而不是靠人抄数字。

刻意只做「读」。写入仍由每次运行按 SYSTEM.md 的事务顺序完成
（先写状态并重读校验，后写 outbox），避免解析器成为账本的隐式写入方。
"""
import os
import re
from typing import Dict, List

FILES = ("portfolio-ledger.md", "sim-wallet.md", "strategy-playbook.md",
         "alert-state.md", "system-state.md")


def _read(root: str, name: str) -> str:
    p = os.path.join(root, name)
    if not os.path.exists(p):
        raise FileNotFoundError("必需状态文件缺失：%s" % p)
    with open(p, encoding="utf-8") as f:
        return f.read()


def _scalar(text: str, key: str, default=None):
    m = re.search(r"^%s:\s*(.+)$" % re.escape(key), text, re.M)
    return m.group(1).strip() if m else default


def _num(s):
    if s is None:
        return None
    m = re.search(r"-?\d+(?:\.\d+)?", str(s).replace(",", ""))
    return m.group(0) if m else None


def load_wallet(root: str) -> Dict[str, object]:
    t = _read(root, "sim-wallet.md")
    rows = dict()
    for line in t.splitlines():
        m = re.match(r"\|\s*([^|]+?)\s*\|\s*([-\d.,]+)\s*\|\s*$", line)
        if m:
            rows[m.group(1).strip().lower()] = m.group(2).strip().replace(",", "")
    need = {"cash": "cash", "total market value": "total_market_value",
            "total assets": "total_assets", "cumulative p&l": "cumulative_pnl",
            "realized p&l": "realized_pnl", "unrealized p&l": "unrealized_pnl"}
    out = {}
    for k, dest in need.items():
        if k not in rows:
            raise ValueError("sim-wallet.md 缺少余额行：%s" % k)
        out[dest] = rows[k]
    out["valuation_date"] = _scalar(t, "valuation_date")
    if not out["valuation_date"]:
        raise ValueError("sim-wallet.md 缺少 valuation_date")
    return out


def load_positions(root: str) -> List[Dict[str, object]]:
    """
    解析账本中的真实与模拟 OPEN 持仓。
    表头列数不同，故按 kind 分别解析，并要求 status 明确为 OPEN/CLOSED。
    """
    t = _read(root, "portfolio-ledger.md")
    out = []
    section = None
    for line in t.splitlines():
        if line.startswith("## OPEN real positions"):
            section = "real"
            continue
        if line.startswith("## OPEN simulated positions"):
            section = "sim"
            continue
        if line.startswith("## ") and not line.startswith("## OPEN"):
            section = None
            continue
        if section is None or not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not cells or cells[0] in ("symbol", "") or set(cells[0]) <= set("-: "):
            continue
        if len(cells) < 3 or cells[1] not in ("OPEN", "CLOSED"):
            continue
        if section == "real":
            out.append({"symbol": cells[0], "status": cells[1], "kind": "real",
                        "quantity": cells[4], "last_close": _num(cells[5]),
                        "close_date": cells[6] if len(cells) > 6 else None})
        else:
            out.append({"symbol": cells[0], "status": cells[1], "kind": "sim",
                        "quantity": _num(cells[4]), "cost_basis": _num(cells[5]),
                        "last_close": _num(cells[6]), "close_date": cells[7],
                        "market_value": _num(cells[8]), "unrealized_pnl": _num(cells[9])})
    if not out:
        raise ValueError("portfolio-ledger.md 未解析到任何 OPEN 持仓（格式可能已变）")
    return out


def alert_state_keys(root: str) -> List[str]:
    t = _read(root, "alert-state.md")
    keys = []
    for line in t.splitlines():
        m = re.match(r"\|\s*([A-Z]+\+[^|\s]+)\s*\|", line)
        if m:
            keys.append(m.group(1))
    return keys


def webhook(root: str) -> str:
    t = _read(root, "system-state.md")
    w = _scalar(t, "webhook")
    if not w or "qyapi.weixin.qq.com" not in w:
        raise ValueError("system-state.md 未提供合法的企业微信 webhook（单一真源，不得硬编码）")
    return w


def load_all(root: str) -> Dict[str, object]:
    for n in FILES:
        _read(root, n)          # 任一缺失即抛 -> STATE_INTEGRITY_FAILURE
    positions = load_positions(root)
    sim = [p for p in positions if p["kind"] == "sim" and p["status"] == "OPEN"]
    return {
        "wallet": load_wallet(root),
        "positions": [p for p in positions if p["status"] == "OPEN"],
        "sim_positions": sim,
        "alert_keys": alert_state_keys(root),
        "webhook": webhook(root),
        "benchmarks": _scalar(_read(root, "system-state.md"), "benchmarks"),
    }
