# 信息源注册表（§13 数据域 1）

> 机器真源：`lib/integrity.py: APPROVED_SOURCES / BAD_SOURCES`（selftest 断言本文与代码同步、
> 且每个交易门槛指标 ≥2 核准源）。全部条目来自 2026-07-25 实测三源核验，非猜测。
> 修改规则：先改代码+测试，再改本文。

## 核准源（按指标分级）

| 指标 | 核准源 | 使用要点 |
|---|---|---|
| equity_close（个股/ETF 正式收盘与历史） | stockanalysis.com ｜ roic.ai ｜ stocktitan.net ｜ stockscan.io | stockanalysis **必须带缓存参数** `?v=`（实测无参给数周旧缓存）；stocktitan **必须核对 Last updated**（按标的冻结）；roic 注意区分盘后价 |
| vix | cboe.com（发行方） ｜ investing.com ｜ google.com/finance ｜ tradingeconomics.com | cboe 必须带缓存参数（曾给六月快照）；investing **仅指数页可用**，其个股报价页陈旧、禁用于 equity_close |
| us10y | investing.com ｜ cboe.com（^TNX） ｜ tradingeconomics.com ｜ etftrends.com | 多源常差 1bp 内，取两源一致值 |
| breadth（市场宽度） | stockanalysis.com/markets | 环境分类用、非交易门槛；允许单源但须内部标注 |

## 使用规则（P1–P5，机器执行）

- P1 交易门槛指标每价 **≥2 独立核准源、≤1% 偏差**；不满足 → ACT-001，动作只能持有。
- P2 黑名单源出现即整条记录作废。
- P3 跨源偏差 >1% 作废。
- 抓取只用服务端渲染页面（JS 空壳源已入黑名单）；抓回文本经 `lib/quote_extract.py` 去噪。

## 黑名单（BAD_SOURCES，实测原因）

| 源 | 原因 |
|---|---|
| nasdaq.com / cnbc.com / finviz.com / zacks.com / barchart.com | JS 空壳，抓不到数据 |
| wsj.com / marketwatch.com / markets.businessinsider.com | 抓取被拒 |
| macrotrends.net / wallstreetzen.com / stockinvest.us / gurufocus.com | 数周陈旧 |
| finance.yahoo.com | 报价页严重陈旧（非延迟） |
| home.treasury.gov | 所有端点截断 |

## 分级晋升/降级

新源须连续 ≥3 个交易日与两个既有核准源零偏差才可入册（先加代码+测试）；
任一核准源单日偏差 >1% 或陈旧 → 当日弃用并记 knowledge，两次即降级入黑名单。
