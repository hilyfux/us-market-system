#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quote_extract — 把抓回来的行情页文本压成「只剩报价」的小字典。

背景（2026-07-27 自检发现的瓶颈）：允许的行情源（如 stockanalysis.com）确实能返回
服务端渲染、可核实的价格，但整页还夹带大量新闻/导航噪声（一次 SPY 抓取就吐出整条
新闻流）。让生成报告的那步在整页里“肉眼找价格”既慢又易错。本模块把抓回的文本
交给确定性解析，抽出：正式收盘价/涨跌/涨跌幅/as-of、盘后价/as-of、前收盘。

刻意只做**纯文本解析**，不发网络请求——抓取仍由 agent 的 web_fetch 工具完成
（沙箱出网受限），本模块只负责把结果去噪，符合总纲“机制以代码为准、可测试”的原则。
用法：
    from quote_extract import extract_quote
    q = extract_quote(fetched_text)   # -> {"price","change","change_pct","as_of",...}
未命中的字段返回 None，绝不臆造（P/CORE-003：宁缺勿造）。
"""
import re
from typing import Dict, Optional

# 一个「价格块」= 价格行 + 涨跌(涨跌幅) 行 + 标签行（At close / After-hours）。
# 数字允许千分位逗号；涨跌幅允许正负号。标签大小写不敏感。
_PRICE = r"([0-9][0-9,]*\.[0-9]+)"
_CHG = r"([+\-][0-9][0-9,]*\.?[0-9]*)\s*\(\s*([+\-]?[0-9.]+)\s*%\s*\)"


def _block(text: str, label_re: str) -> Optional[Dict[str, str]]:
    pat = re.compile(_PRICE + r"\s*\n\s*" + _CHG + r"\s*\n\s*" + label_re +
                     r"\s*:?\s*([^\n]+)", re.I)
    m = pat.search(text)
    if not m:
        return None
    return {
        "price": m.group(1).replace(",", ""),
        "change": m.group(2).replace(",", ""),
        "change_pct": m.group(3),
        "as_of": m.group(4).strip(),
    }


def _table_num(text: str, label: str) -> Optional[str]:
    # markdown 表格行： | Previous Close | 738.18 |
    m = re.search(r"\|\s*" + re.escape(label) + r"\s*\|\s*([0-9][0-9,]*\.?[0-9]*)\s*\|",
                  text, re.I)
    return m.group(1).replace(",", "") if m else None


def extract_quote(text: str) -> Dict[str, Optional[str]]:
    """从抓取到的行情页文本抽取报价核心字段；未命中的字段为 None。"""
    if not text:
        return {"price": None, "change": None, "change_pct": None, "as_of": None,
                "after_hours_price": None, "after_hours_as_of": None,
                "previous_close": None, "open": None, "day_range": None}
    close = _block(text, r"At\s+close") or {}
    after = _block(text, r"After[-\s]?hours") or {}
    rng = re.search(r"\|\s*Day'?s\s+Range\s*\|\s*([0-9][0-9,.\s\-]+?)\s*\|", text, re.I)
    return {
        "price": close.get("price"),
        "change": close.get("change"),
        "change_pct": close.get("change_pct"),
        "as_of": close.get("as_of"),
        "after_hours_price": after.get("price"),
        "after_hours_as_of": after.get("as_of"),
        "previous_close": _table_num(text, "Previous Close"),
        "open": _table_num(text, "Open"),
        "day_range": rng.group(1).strip() if rng else None,
    }
