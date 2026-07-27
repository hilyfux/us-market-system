#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
knowledge — 知识库闭环（SYSTEM.md §12，模式来自 nashsu/llm_wiki）。

原则：**增量维护持久互链 wiki，而不是每次从零推理**。
每个 MORNING / POST_CLOSE 运行：决策前 `read_ticker()` 相关页面，
决策后 `append_ticker_note()` / `append_review()` 回写学到的东西。

刻意最小化：纯文件操作、确定性、可测试；不做任何网络/LLM 调用。
写入均为**追加**（增量原则），绝不覆盖已有内容。
"""
import os
import re
from typing import Dict, List, Optional

KNOWLEDGE_DIR = "knowledge"
_SUBDIRS = ("tickers", "regime", "reviews")
_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

_TICKER_TEMPLATE = """# {symbol} —（新建标的页，待补论点）

论点：待补。
持仓：待补。

## Log
"""


def root(state_root: str) -> str:
    return os.path.join(state_root, KNOWLEDGE_DIR)


def ensure_structure(state_root: str) -> str:
    """确保 knowledge/ 与子目录存在；幂等。返回 knowledge 根路径。"""
    k = root(state_root)
    for d in (k,) + tuple(os.path.join(k, s) for s in _SUBDIRS):
        os.makedirs(d, exist_ok=True)
    return k


def ticker_path(state_root: str, symbol: str) -> str:
    if not re.match(r"^[A-Z][A-Z0-9.]{0,9}$", symbol):
        raise ValueError("非法代码：%r" % symbol)
    return os.path.join(root(state_root), "tickers", "%s.md" % symbol)


def read_ticker(state_root: str, symbol: str) -> Optional[str]:
    """读标的页；不存在返回 None（调用方决定是否建页），绝不臆造内容。"""
    p = ticker_path(state_root, symbol)
    if not os.path.exists(p):
        return None
    with open(p, encoding="utf-8") as f:
        return f.read()


def append_ticker_note(state_root: str, symbol: str, date: str, note: str) -> str:
    """向标的页 Log 追加一条带日期的记录；页面不存在则先按模板建页。"""
    if not _DATE_RE.match(date):
        raise ValueError("date 须为 YYYY-MM-DD：%r" % date)
    note = " ".join(note.split())
    if not note:
        raise ValueError("空 note 不入库")
    ensure_structure(state_root)
    p = ticker_path(state_root, symbol)
    if not os.path.exists(p):
        with open(p, "w", encoding="utf-8") as f:
            f.write(_TICKER_TEMPLATE.format(symbol=symbol))
    line = "- %s · %s\n" % (date, note)
    with open(p, encoding="utf-8") as f:
        if line in f.read():
            return p          # 幂等：完全相同的记录不重复追加
    with open(p, "a", encoding="utf-8") as f:
        f.write(line)
    return p


def review_path(state_root: str, date: str) -> str:
    if not _DATE_RE.match(date):
        raise ValueError("date 须为 YYYY-MM-DD：%r" % date)
    return os.path.join(root(state_root), "reviews", "%s.md" % date)


def review_exists(state_root: str, date: str) -> bool:
    return os.path.exists(review_path(state_root, date))


def append_review(state_root: str, date: str, content: str) -> str:
    """写/追加当日复盘。已存在则追加小节（增量），不覆盖。"""
    ensure_structure(state_root)
    p = review_path(state_root, date)
    if not content.strip():
        raise ValueError("空复盘不入库")
    mode = "a" if os.path.exists(p) else "w"
    with open(p, mode, encoding="utf-8") as f:
        if mode == "w":
            f.write("# 每日复盘 — %s\n\n" % date)
        f.write(content.rstrip() + "\n")
    return p


def summary(state_root: str) -> Dict[str, object]:
    """给 run-summary 用：页面计数与最近复盘日期。"""
    k = root(state_root)
    if not os.path.isdir(k):
        return {"present": False, "tickers": 0, "reviews": 0, "latest_review": None}
    tick = [f[:-3] for f in os.listdir(os.path.join(k, "tickers")) if f.endswith(".md")] \
        if os.path.isdir(os.path.join(k, "tickers")) else []
    revs = sorted(f[:-3] for f in os.listdir(os.path.join(k, "reviews")) if f.endswith(".md")) \
        if os.path.isdir(os.path.join(k, "reviews")) else []
    return {"present": True, "tickers": len(tick), "ticker_symbols": sorted(tick),
            "reviews": len(revs), "latest_review": revs[-1] if revs else None}
