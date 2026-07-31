#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backtest — 决定论回测/绩效引擎（纯函数，可测试）。

定位（SYSTEM.md §0 机制以代码为准）：这是「盘后复盘→策略优化」闭环的量化底座。
把持续累积的**决策数据**（data/decision-log.jsonl）与**权益/成交**回放成可复现的
绩效指标——收益、回撤、胜率、盈亏比、期望、对基准超额。

诚实边界（写在代码里，避免过拟合，L-001/L-007）：
- 指标只是对**已发生**决策与成交的确定性度量；样本不足时数字是噪声不是 edge。
- 引擎的正确性由合成数据单测锁定；数据的充分性由 `sample_sufficiency()` 显式标注。
- 无 I/O、无随机、无隐藏状态：同输入恒同输出。
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List, Optional, Sequence

# 有意义统计所需的最小样本（保守；低于此仅作方向参考，不得当作 edge）。
MIN_TRADES_FOR_SIGNIFICANCE = 20
MIN_EQUITY_POINTS_FOR_TREND = 20


def _D(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def _q2(x: Decimal) -> Decimal:
    return x.quantize(Decimal("0.01"), ROUND_HALF_UP)


def total_return(equity: Sequence) -> Decimal:
    """权益序列首→末的总收益率（%）。序列 < 2 点时返回 0。"""
    e = [_D(v) for v in equity]
    if len(e) < 2 or e[0] == 0:
        return Decimal("0")
    return _q2((e[-1] - e[0]) / e[0] * 100)


def max_drawdown(equity: Sequence) -> Decimal:
    """最大回撤（%，正数表示回撤幅度）。峰值到谷底的最大跌幅。"""
    e = [_D(v) for v in equity]
    if len(e) < 2:
        return Decimal("0")
    peak = e[0]
    mdd = Decimal("0")
    for v in e:
        if v > peak:
            peak = v
        if peak > 0:
            dd = (peak - v) / peak * 100
            if dd > mdd:
                mdd = dd
    return _q2(mdd)


def trade_stats(closed_trades: Sequence[Dict[str, object]]) -> Dict[str, object]:
    """
    对**已平仓**成交做统计。每笔至少含 realized（已实现盈亏，USD）。
    返回 n / wins / losses / win_rate% / gross_profit / gross_loss /
    profit_factor / avg_win / avg_loss / expectancy。
    """
    realized = [_D(t["realized"]) for t in closed_trades]
    n = len(realized)
    wins = [r for r in realized if r > 0]
    losses = [r for r in realized if r < 0]
    gross_profit = sum(wins) if wins else Decimal("0")
    gross_loss = -sum(losses) if losses else Decimal("0")   # 正数
    pf = (gross_profit / gross_loss) if gross_loss > 0 else (
        Decimal("Infinity") if gross_profit > 0 else Decimal("0"))
    return {
        "n": n,
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": _q2(Decimal(len(wins)) / n * 100) if n else Decimal("0"),
        "gross_profit": _q2(gross_profit),
        "gross_loss": _q2(gross_loss),
        "profit_factor": (pf if pf == Decimal("Infinity") else _q2(pf)),
        "avg_win": _q2(gross_profit / len(wins)) if wins else Decimal("0"),
        "avg_loss": _q2(-gross_loss / len(losses)) if losses else Decimal("0"),
        "net_realized": _q2(sum(realized)) if realized else Decimal("0"),
        "expectancy": _q2(sum(realized) / n) if n else Decimal("0"),
    }


def benchmark_relative(equity: Sequence, benchmark: Sequence) -> Dict[str, object]:
    """组合总收益 − 基准总收益（超额，pp）。两序列需同期同长度。"""
    r_port = total_return(equity)
    r_bench = total_return(benchmark)
    return {"portfolio_return": r_port, "benchmark_return": r_bench,
            "excess_pp": _q2(r_port - r_bench)}


def sample_sufficiency(n_trades: int, n_equity_points: int) -> Dict[str, object]:
    """显式标注样本是否足以支撑统计结论——防止把噪声当 edge（L-001/L-007）。"""
    ok = (n_trades >= MIN_TRADES_FOR_SIGNIFICANCE
          and n_equity_points >= MIN_EQUITY_POINTS_FOR_TREND)
    return {
        "sufficient": ok,
        "n_trades": n_trades,
        "n_equity_points": n_equity_points,
        "min_trades": MIN_TRADES_FOR_SIGNIFICANCE,
        "min_equity_points": MIN_EQUITY_POINTS_FOR_TREND,
        "verdict": ("统计充分" if ok else
                    "样本不足——以下指标仅供方向参考，不得当作已验证 edge（L-001/L-007）"),
    }


def run(equity: Sequence, closed_trades: Sequence[Dict[str, object]],
        benchmark: Optional[Sequence] = None) -> Dict[str, object]:
    """一次性汇总：收益、回撤、成交统计、对基准、样本充分性。纯函数。"""
    out = {
        "total_return_pct": total_return(equity),
        "max_drawdown_pct": max_drawdown(equity),
        "trades": trade_stats(closed_trades),
        "sample": sample_sufficiency(len(closed_trades), len(equity)),
    }
    if benchmark is not None:
        out["vs_benchmark"] = benchmark_relative(equity, benchmark)
    return out
