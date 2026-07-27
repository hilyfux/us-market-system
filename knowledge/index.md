# 知识库总目录（Knowledge Wiki）

> 模式来自 [llm_wiki](https://github.com/nashsu/llm_wiki)：**增量维护一个持久、互链的 wiki**，
> 而不是每次从零推理。每个 MORNING / POST_CLOSE 运行：**决策前读相关页面，决策后回写学到的东西**。
> 规则见 SYSTEM.md §12（知识闭环）。

## 结构

| 目录/文件 | 内容 | 谁写 |
|---|---|---|
| `tickers/<SYM>.md` | 每标的一页：论点、关键位、财报史、事件反应、经验教训 | MORNING / POST_CLOSE |
| `regime/<YYYY-MM>.md` | 当月市场环境演变（VIX/宽度/利率/轮动） | POST_CLOSE |
| `reviews/<YYYY-MM-DD>.md` | 每日复盘：当日事实 → 决策 → 结果 → 教训 | POST_CLOSE（每交易日一篇） |
| `lessons.md` | 跨标的的持久教训（错误分类学），只增不删 | POST_CLOSE / 维护 |
| `index.md` | 本页 | 维护 |

## 持仓页

真实（顾问跟踪，动作一律建议未执行）：
[PWR](tickers/PWR.md) · [MP](tickers/MP.md) · [BE](tickers/BE.md) · [KTOS](tickers/KTOS.md) · [RMBS](tickers/RMBS.md)

模拟（10 万美元模拟盘，最多 8 槽）：
[GEV](tickers/GEV.md) · [ETN](tickers/ETN.md) · [ABT](tickers/ABT.md)

## 其他入口

- [持久教训 lessons.md](lessons.md)
- [2026-07 市场环境](regime/2026-07.md)
- [每日复盘目录 reviews/](reviews/)
- 策略手册（正式规则真源）：`../strategy-playbook.md`

## 维护规约

1. **增量**：只追加与修订，不推倒重写；每条目注明日期。
2. **互链**：复盘引用标的页，标的页引用教训条目（`lessons.md#L-xxx`）。
3. **事实与推断分离**：事实带来源与 as-of；推断显式标注"推断"。
4. **教训必须可操作**：写成"下次遇到 X 就做 Y"，否则进不了 lessons.md。
