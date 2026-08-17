# 信息源注册表（§13 数据域 1）

> 机器真源：`lib/integrity.py: APPROVED_SOURCES / BAD_SOURCES`（selftest 断言本文与代码同步、
> 且每个交易门槛指标 ≥2 核准源）。全部条目来自 2026-07-25 实测三源核验，非猜测。
> 修改规则：先改代码+测试，再改本文。

## 核准源（按指标分级）

| 指标 | 核准源 | 使用要点 |
|---|---|---|
| equity_close（个股/ETF 正式收盘与历史） | stockanalysis.com ｜ roic.ai ｜ stocktitan.net ｜ stockscan.io | stockanalysis **必须带缓存参数** `?v=`（实测无参给数周旧缓存）；stocktitan **必须核对 Last updated**（按标的冻结）；roic 注意区分盘后价；**stockscan.io 自 2026-08-11 起同样必须核对日期戳**（当日对 MSFT/ETN/ABT/NVDA/LLY 返回 7 月下旬旧行情、对 KTOS 却是定稿值，按标的冻结，L-022） |
| vix | cboe.com（发行方） ｜ investing.com ｜ google.com/finance ｜ tradingeconomics.com | cboe 必须带缓存参数（曾给六月快照）；investing **仅指数页可用**，其个股报价页陈旧、禁用于 equity_close |
| us10y | investing.com ｜ cboe.com（^TNX） ｜ tradingeconomics.com ｜ etftrends.com | 多源常差 1bp 内，取两源一致值 |
| breadth（市场宽度） | stockanalysis.com/markets | 环境分类用、非交易门槛；允许单源但须内部标注 |
| **closing_window_price（T-20min価＝引け20分前の盤中価、CLOSING約定フィル専用）** | stockanalysis.com ｜ roic.ai ｜ stocktitan.net ｜ stockscan.io | **用途を厳密限定（2026-08-17 用户裁定）**：この盤中価（CLOSING 窓時刻≈15:40 ET）は **CLOSING で約定した取引のフィル価格と、それに由来する保有成本（コスト基準）にのみ**用いる。取得口径＝**≥2 核准源・偏差≤1%・盤中タイムスタンプ**。盤中価ゆえ「At close／Adj.Close 定稿／全日出来高」は**要求しない**（それらは終値専用で盤中に適用不能）。**評価（mark-to-market・NAV）・離場判定・分析・戦略レビュー・データ門の取価には用いない——これらは全て公式收盘（equity_close，POST_CLOSE で更新）**。individual 个股详情页の报价头が「Market open」時に返す现价を用いる。当初 addendum は本価格を全会计書込・評価・データ門・離場まで拡大したが過剰と裁定され差し戻し。≥2核准源の可满足性は selftest `test_price_convention` が机器保证（`approved_for("closing_window_price") ≥ 2`） |

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

> ⚠️ **更正注记（2026-08-15 审计 B2）**：2026-08-11 的 LNG 结算曾以黑名单源 **stockinvest.us** 作为
> 「双源」的第二源（见 portfolio-ledger `morning_note_2026-08-12` 与 system-state 8/12 MORNING 记录）。
> 当日值与核准源 stockanalysis 偏差 0.00%、且 stockscan/roic 旁证同值，**数值本身未受影响**，
> 但按 P2（黑名单源出现即整条记录作废）属**口径违反**；`PriceRecord.validate`（P1–P5）未配线到
> 实结算路径，故机器未拦截。恒久对策已登记 gap-ledger **G-B2**；源列表的晋升/删除属策略判断，
> 本注记不改动黑名单本身。

## 分级晋升/降级

新源须连续 ≥3 个交易日与两个既有核准源零偏差才可入册（先加代码+测试）；
任一核准源单日偏差 >1% 或陈旧 → 当日弃用并记 knowledge，两次即降级入黑名单。

## 抓取方法规则（2026-07-28，来自 7/27 结算失败的教训）

> **適用範囲**：本節の三条は **equity_close（正式收盘）** の抓取規則である。equity_close は POST_CLOSE の mark-to-market 評価・結算・検証と、離場判定・分析・データ門の取価に用いる（従来どおり）。**CLOSING約定フィル価格（closing_window_price＝引け20分前の盤中価）には適用しない**——約定フィルは引け20分前の盤中価を≥2核准源・偏差≤1%・盤中タイムスタンプで取得し「At close／定稿／全日出来高」を要求しない（上表）。以下の「收盘后60分／At close 日期≠当日→GAP」は正式收盘の定稿値検証に効く。

- **禁止**：收盘后 60 分钟内抓报价页当正式收盘——缓存必然陷阱（实测 T+31min 得到的是上一交易日）。（正式收盘检证＝POST_CLOSE 専用）
- **标准方法**：**历史页次晨回补**——`/stocks/<sym>/history/`（带缓存参数）+ roic.ai 双源；一次抓取即含近月全部收盘，7/27 回补实测 8/8 双源 ≤0.09% 偏差一次成功。（正式收盘检证＝POST_CLOSE 専用）
- POST_CLOSE 结算窗口内若报价页疑似陈旧（At close 日期≠当日）→ 直接登记 GAP，由次晨 MORNING 用历史页法回补，不做无谓重试。（本条は POST_CLOSE 正式收盘检证専用；CLOSING約定フィル価格には課さない）

## 程序化供应商现状（2026-07-28 实测）

- stooq.com 与 query1.finance.yahoo.com（免费无钥 API）：**沙箱代理不可达**（返回空），已排除，勿再重试。
- **Alpha Vantage MCP 连接器**：**已连接（2026-07-28），试用期第 1/3 天**。首日验证：TIME_SERIES_DAILY 对 8 持仓 + SPY 的 7/24 与 7/27 收盘与本系统双源核验值 **18/18 完全一致（0.00%）**；SPY MA50 计算值 745.00 与既有记录 745.07 相互印证。已知限制：`outputsize=full` 为付费功能（MA200 暂不可得）；免费层 ~25 请求/日（日常 13 标的收盘足够）。观察项：AV 的 SPY 2026-07-16 收盘 750.72 vs 本系统旧记录 750.83（0.015%，或为拆分调整口径，试用期内继续观察）。连续 3 个交易日零偏差后按规则入册 APPROVED。
- 开源客户端库（yfinance 等）不可用：沙箱禁止程序化 HTTP 且网络受限。
