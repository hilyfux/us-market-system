# 美股决策系统 · 总纲（SYSTEM.md）

canonical_spec_version: 2.5
derived_from: strategy-playbook VERSION 2.0.0
last_updated: 2026-07-27
state_root: /Users/linqing.wang/Desktop/Claude/us-stock-system

## 0. 机制以代码为准，本文只写策略

2026-07 的停摆事故根因不是某个 bug，而是**总纲是散文**：每次运行都由 LLM 重新手工
实现一遍阶段判定、去重、校验，没有任何东西可被测试，两套"实现"（散文与实际行为）
必然漂移。因此机制部分已抽成库，**本文不再复述**：

| 关注点 | 唯一实现源 | 说明 |
|---|---|---|
| 交易日历、阶段路由、检查点吸附 | `lib/market_core.py` | 早收盘、夏冬令时、调度延迟 |
| 调度对齐证明 | `lib/market_core.py: verify_schedule_alignment` | 证明 cron 能命中每阶段且有 jitter 余量 |
| 市场环境分类（决定仓位上限） | `lib/market_core.py: classify_regime` | 确定性阈值，不再靠判断 |
| 槽位会计 | `lib/market_core.py: slot_report` | 显式区分 occupied/available/manageable/frozen |
| 账务校验 | `lib/integrity.py: validate_accounting` | C1–C6，**有检出力** |
| 陈旧度 / 存活 / 死信看门狗 | `lib/integrity.py` | W1–W4 |
| 行情溯源与来源黑名单 | `lib/integrity.py: PriceRecord` | P1–P5 |
| 入队、去重、修订键、抑制 | `lib/outbox.py` | 路径可用性强制校验 |
| 状态文件解析 | `lib/state.py` | 只读，不做隐式写入 |
| 知识库闭环（读-决策-回写） | `lib/knowledge.py` | 增量追加、幂等、只对决策阶段开放写入 |

**每次运行的第一步必须是 `python3 tools/preflight.py`。** 退出码非 0 即不得进入任何
阶段流程（不得交易、不得发正常报告、不得在别处初始化）。
规范改动必须先在 `tools/selftest.py` 补用例并全绿（当前 101/101）；
改阈值就是改策略，测试用例即策略的可执行定义。

> 这是整套美股决策系统的**唯一共享规则源**。所有任务的 SKILL 只写"本任务独有的部分"，共享铁律一律以本文件为准。修改共享规则只改这里，不要在各 SKILL 里各写一份。

---

## 1. 系统概述与数据流

这是一个**单一决策闭环**，由**一个**定时任务 `us-market-system` 按美东时间自动路由到晨间/盘前/盘中/盘后四个阶段驱动，共享同一个状态目录。核心思想：账本是唯一真源，数据不可靠时只持有，状态写入并校验通过后才推送。

每个任务运行时**按此顺序**读取状态文件：
`portfolio-ledger.md → sim-wallet.md → strategy-playbook.md → alert-state.md → system-state.md`

一个美股交易日的时间线（新加坡时间 SGT）：

```
晨间决策 08:30 ──▶ 盘前候选触发 20:00–22:00 ──▶ 盘中候选触发 21:30…次日05:30（每半小时）──▶ 盘后候选触发 次日04:30/05:30
（按估值日去重）           （按 ET 与交易状态路由，不交易）       （仅实际连续交易时段执行）                    （按实际收盘时间结算+学习）
```

## 2. 状态文件职责

| 文件 | 角色 | 允许写入方 |
|---|---|---|
| `portfolio-ledger.md` | 持仓与交易的**唯一真源**；状态只有 OPEN / CLOSED | 晨间、盘后；盘中禁止交易写入 |
| `sim-wallet.md` | 模拟资金账务（现金/市值/盈亏/仓位） | 晨间、盘后；盘中只读 |
| `strategy-playbook.md` | 策略手册：CORE / ACTIVE / HYPOTHESIS / REJECTED / VERSION | 盘后（策略学习） |
| `alert-state.md` | 推送去重键（alert_key / report_key） | 所有任务（errcode=0 后） |
| `system-state.md` | 配置（state_root、企业微信 webhook）+ 各次运行日志 | 所有任务 |

## 3. 任务地图（单一定时任务）

整套系统只有**一个**定时任务 `us-market-system`，它按美东时间自动路由到四个阶段之一。这样是单一状态机、单一 owner，天然避免多任务共享状态时的去重/账本/时序打架。

| 定时任务 | 触发 cron（UTC） | 说明 |
|---|---|---|
| `us-market-system` | `0,30 0-5,8,20-23 * * *`（Asia/Singapore） | 每天 SGT 08:00/08:30 及 20:00–次日05:30 每半小时触发；每次先判 ET 与交易所实际状态，只跑一个阶段，否则仅写心跳 |

阶段（由 ET + 交易所状态判定，见 `Scheduled/us-market-system/SKILL.md`）：

| 阶段 | 何时 | 职责 | 可改模拟持仓 |
|---|---|---|---|
| MORNING | SGT 08:30；按上一正式收盘交易日去重 | 用上一交易日正式收盘管理持仓 + 扫描新机会；休市日不得基于同一估值日重复交易 | 是（通过全部门槛后） |
| PREMARKET | 交易日 ET 08:30–09:29 | 盘前市场/持仓/催化固定报告 | 否 |
| INTRADAY | 实际连续交易时段内 ET `:00/:30` | 每半小时分析全部持仓并报告；只读账本与钱包 | 否，仅建议未执行 |
| POST_CLOSE | 距当日实际正式收盘约 20–60 分钟 | 正式结算、信号验证、策略闭环学习；兼容早收盘 | 是（账务校验后） |

## 4. 共享铁律（所有任务必须遵守）

CORE（引自 strategy-playbook VERSION 2.0.0）：
- CORE-001 账本是持仓/交易唯一真源；钱包只覆盖模拟资金。
- CORE-002 真实持仓的数量/状态只有在用户明确确认成交后才变更。
- CORE-003 数据未核实/过期/冲突时不得交易，唯一动作为 `持有` 并记录失败。
- CORE-004 绝不仅凭固定涨跌幅或盘中触价交易。
- CORE-005 状态写入与账务校验成功之后才推送。

数据门 **ACT-001**（system control）：来源冲突 >1%、日期错误、盘中报价延迟 >20 分钟、或缺正式收盘 → 阻断建仓/加仓/减仓/平仓，动作只能 `持有`，记录 `DATA_FAILURE`。

真实/模拟分离：
- 真实持仓：所有动作都是**建议未执行**；真实数量未知者不计入钱包市值与组合盈亏。
- 盘中阶段：只分析与标记风险，不执行真实或模拟交易，不改账本/钱包；任何减仓/平仓/止盈/止损均为建议未执行，留待正式收盘确认。
- 模拟交易：仅晨间或盘后可执行；必须生成唯一 `trade_id = 市场交易日-代码-动作-序号`，并记录含时区的 `executed_at`、`market_session_date`、`valuation_source_date`，先查重再同时写账本与钱包。
- 账务校验（误差 ≤ USD 0.05）：由 `lib/integrity.py: validate_accounting` 执行 C1–C6。

> **2026-07-25 修正**：旧总纲写的"账务守恒"（`现金 + 市值 = 总资产`、
> `累计盈亏 = 总资产 − 100000`）是**恒等式而非校验**——总资产与累计盈亏本就由这两式
> 定义，故恒返回 0.000000，包括在数据完全错误时，检出能力为 0。现改为：
> C1 `sum(股数 × 收盘价)` 对比存储市值 ｜ C2 `初始资金 − sum(成本基础)` 对比存储现金
> （可抓幽灵交易、漏记成本、手改现金）｜ C3 各仓未实现之和对比总未实现 ｜
> C4/C5 逐仓市值与盈亏一致性 ｜ C6 累计盈亏 = 已实现 + 未实现。
> 两条恒等式保留但显式标注 WARN 级"无检出力，仅供人工可读性核对"。

动作词表（唯一合法集合）：`持有 / 建仓 / 加仓 / 减仓 / 平仓 / 止盈-减仓X% / 止盈-平仓 / 止损-减仓X% / 止损-平仓`。

其它：盘中价不得写成正式收盘净值；止盈须盈利且催化兑现/趋势衰竭/高位风险经**收盘**确认；止损须逻辑或基本面破坏且**收盘**技术确认（ACT-002 / ACT-003）。

模拟风险预算（ACT-004）：总槽位 ≤ 8；单只初始通常 5%、单只 ≤ 20%、行业 ≤ 35%、单笔计划风险 ≤ 总资产 1%。

环境仓位上限由 `classify_regime()` **确定性推导**（旧版本靠人工判断，不可复现）：

| 环境 | 触发条件（自上而下，首个命中生效） | 仓位上限 |
|---|---|---:|
| STRESS | VIX ≥ 30 或 SPY < 200 日线 | 0% |
| DEFENSIVE | VIX ≥ 22 或 SPY < 50 日线 | 50% |
| CHOPPY | VIX ≥ 16 或 宽度 < 1.0 | 75% |
| RISK_ON | 其余 | 90% |

**模拟盘硬约束（用户 2026-07-27 明确）**：初始资金 **US$100,000**、**最多 8 个持仓**。这两条是交易的硬边界，不得逾越。

**槽位语义**（旧字段 `open_slots` 含义不明，而它直接决定能否建仓）：
由 `slot_report()` 返回 `occupied / available / manageable / frozen / sim_open / real_tracked`。
**2026-07-27 变更**：8 槽风险预算**只对模拟持仓计数**——模拟盘拥有独立的 8 槽。真实持仓是用户真金白银、仅供顾问跟踪（一律「建议未执行」），单列在 `real_tracked`，**不占用模拟预算**。旧口径把两者混在一个 8 槽里，导致 5 只真实持仓占满、模拟盘 8.5 万现金在 50% 上限下无槽可用（结构性死锁）——已解除。
`frozen` = 真实持仓且数量未知（现已全部补齐，为 0），单列不再挤占预算。
当前状态：模拟盘 **占用 3/8、可用 5**（GEV/ETN/ABT）；真实持仓 5 只单列跟踪、不占槽；DEFENSIVE 上限 50%，模拟盘已投 ~15%（约 1.49 万），可再部署约 3.5 万美元。

## 5. 通知协议（企业微信，经 outbox 转发）

> **重要**：任务跑在代码执行沙箱里，沙箱出网被拦，**不能直接 POST 企业微信**（会 403）。
> 因此"推送"= **写一条消息文件到 outbox**，由本机 launchd 转发器（沙箱外、用本机网络）代发。
> 转发器实现见附录 §9；本节只规定 agent 的行为。

- **"推送"的唯一动作 = 原子写 outbox 文件**，不得在沙箱内 curl/urlopen 企业微信。
- webhook 从 `system-state.md` 的 `## Notification` 段读取（**单一真源、不得硬编码**），把读到的 URL 原样写进消息的 `webhook` 字段。
- 顺序：**先写状态并重新读取校验，后写 outbox**（state_write_then_enqueue）。
- **路径可用性探针的语义（2026-07-27 修正）**：`assert_path_usable()` 只验证 `enqueue()` 真正依赖的能力——建目录 + 原子写（写 `.tmp` 再 `rename`）+ 读回；这三者任一失败才判 `ENQUEUE_PATH_UNAVAILABLE`。`unlink`（仅用于清理探针）失败是**非致命**的：`enqueue()` 从不 unlink（归档/删除由宿主机转发器完成，那侧 unlink 正常），且部分沙箱 FUSE 挂载允许 open/write/rename 却拒绝 unlink（EPERM）。旧探针用 write-then-`remove`，把 unlink 当硬条件，会在 outbox 实际可用时**误报**并间歇性阻断健康运行（含可交易的 MORNING/PREMARKET）——由 `tools/selftest.py` 回归用例锁定。死信计数（`queue_state`/W3）同口径：`failed/` 里只有 `.json` 消息文件算死信，探针点文件（如 `.wp`）与 `failed/archive/` 归档子目录不计入。
- outbox 目录（**2026-07-25 迁移**）：`~/.local/share/us-stock-outbox/`。
  - 迁移原因：旧位置 `~/Desktop/Claude/us-stock-outbox/` 在 `~/Desktop` 下受 macOS TCC 保护，launchd 后台转发器读它必然 `PermissionError (Errno 1)`，除非给解释器授予**完整磁盘访问**——而那会让该解释器跑的**任何**脚本都获得全盘权限，过宽且不必要。
  - `~/.local/share` **不受 TCC 保护**：沙箱挂载后可写，launchd 可直接读，**无需任何特殊权限**。
  - 前置条件：运行时必须挂载 `~/.local/share`（与 `state_root` 一样属于必需挂载）。若本次运行读/写不到该 outbox，**不得**改写到 `~/Desktop` 下当替代（那边转发器读不到，等于静默丢消息）；应在 run-summary 记 `ENQUEUE_PATH_UNAVAILABLE` 并结束。
  - 旧目录保留为历史归档，不再写入。
- 去重（两段式，保持"errcode=0 后才写 alert-state"不变）：
  - `report_key`（`PREMARKET+ET日期`、`INTRADAY+ET日期+HHmm`、`MORNING+估值交易日`、`POSTCLOSE+ET交易日`）为永久幂等键；`alert_key = 代码+fact_id+动作+触发带` 采用 24h 抑制。
  - **入队前查重**：若该 `report_key` 已在 `alert-state`（已确认送达）**或**已存在于 `~/.local/share/us-stock-outbox/`（含 `sent/`，即已入队/在途），则本次不重复入队。
  - **送达确认**：转发器成功（errcode=0）后会把 `report_key` 追加到 `~/.local/share/us-stock-outbox/.delivered-keys`。每次运行开头读该账本，把新确认的 `report_key` 写入 `alert-state`。**仍然只有 errcode=0 后才写 alert-state**，只是确认是下一轮异步观测到的。
  - 结算事务另以 `POSTCLOSE+ET交易日` 在状态写入前查重。
- 交付可靠性由转发器负责：失败自动重试 5 次，仍失败进 `failed/` 并记日志（可观测）；agent 不重试、不阻塞。
- 篇幅：盘前/盘中/盘后 ≤ 650 字，晨间 ≤ 700 字，markdown。
- **可读性与无歧义（强制，不合格即不得推送）**：推送正文必须结构化、简洁、清晰，且不含任何逻辑歧义。具体标准：
  - 固定用 markdown；首行标题写明「阶段 + 日期」；字段/小节顺序稳定，一眼可读；不堆叠冗长句。
  - 每个持仓一行给出「代码 · 动作 · 唯一驱动事实」；动作只能取自 §4 动作词表，禁止模糊动词（如“观察”“注意”）。
  - 每个数字都带口径与单位（价 / % / pp / 净值），并注明 as-of 时间与来源；盘中价与正式收盘净值绝不混写。
  - 真实持仓动作一律显式标注「建议未执行」，与已落账的模拟交易明确区分；数据降级时写清唯一动作为「持有」及其原因。
  - 任何待确认信号（YELLOW / RED_PENDING_CLOSE 等）必须写明确认条件；不得出现自相矛盾、可两解、或省略前提的表述。
  - 宁可显式标注数据缺口，也不得输出模棱两可的结论。含混或有歧义的报告视为不合格：修正后再入队（可用 `KEY#rN` 修订键），不得原样推送。
  - **篇幅是硬约束，须主动写紧凑（2026-07-27 自检教训）**：8 持仓 + 环境 + 钱包 + 催化 + 检查条件很容易越过 650 字上限（实测一版 722 字被 L2 挡下，压到 591 才过）。因此每仓固定压成**一行**「代码 · 动作 · 唯一驱动事实」，环境/槽位/钱包各一行，检查条件 ≤2 条；先写要点再删冗词。宁可少写修饰，不可超限被硬门拦回。
  - **动作词只出现在“动作行”，不要写进叙述/检查条件行（2026-07-27 自检教训）**：L4 会把任意含 减仓/平仓/止盈/止损 的行当成一次交易动作。前瞻性的检查条件（“开盘后检查：若…再议减仓”）虽已被条件守卫豁免，但仍建议改用中性措辞（“若…则复核仓位”），避免歧义。
  > **机器可验证子集已成硬门**：`lib/report_lint.py: lint_report()` 断言 L1 标题+日期、L2 篇幅、
  > L3 动作词表（模糊动词一律违规）、L4 盘前/盘中非“持有”交易动作须标注“建议未执行”、
  > L5 数据时间来源。**L4 的否定语境（“无减仓/平仓信号”）与条件/检查语境（“若…待收盘确认…再议减仓”）均豁免**
  > ——只判**当下的、非条件的**未标注交易动作，既堵真实漏标又不误杀前瞻检查条件（2026-07-27 修复，见 `_CONDITIONAL`）。
  > `outbox.enqueue()` 默认 `lint=True`，阶段报告不合格即抛 `ReportLintError`
  > （响亮失败，绝不静默推送歧义报告），修正后用 `KEY#rN` 重发。`tools/selftest.py` 有对应用例。
  > 纯语义类要求（自相矛盾、可两解、省略前提）无法在不做语言理解下稳定判定，不在硬门内，
  > 由生成报告的一步自检遵守——高精确、低误报是刻意取舍，以免误杀合规推送。
- **可修订键**：`report_key` 仍永久幂等，但允许 `KEY#rN` 修订（`outbox.next_revision()`）。
  旧设计下，一份用降级数据发出的报告会永久烧掉该键，之后无法重发更正版。
- **抑制重复无变化报告**（治理告警疲劳）：`outbox.enqueue()` 比对内容指纹，
  与上一条同阶段报告完全一致且**无风险标记**时不入队。
  带 🚨 风险标记或 `force=True` 一律放行——安全信息绝不被抑制。
  背景：旧节奏一个交易日可推 ~16 条，其中绝大多数是同一句"全部持有 + 数据降级"。
- **盘中节奏已下调**：见 §10。

## 6. 夏冬令时（DST）自动兼容

调度器固定使用 Asia/Singapore，每天 SGT 20:00–次日 05:30 每半小时提供候选。每次运行必须核实 ET、交易日历和交易所实际开收盘状态；仅有效阶段执行并推送，其余候选只写最小心跳。

| 时段 | 夏令时(EDT) SGT | 冬令时(EST) SGT | 有效检查点 |
|---|---|---|---|
| 盘前 ET 08:30–09:29 | 20:30–20:59 | 21:30–21:59 | 阶段内首个未去重的 `:00/:30` 候选 |
| 正常盘中 ET 09:30–16:00 | 21:30–次日04:00 | 22:30–次日05:00 | ET 09:30、10:00、10:30…15:30 |
| 正常盘后（收盘约 +30min） | 次日04:30 | 次日05:30 | 以实际正式收盘时间计算 |
| 早收盘日 | 依交易所日历动态计算 | 依交易所日历动态计算 | 以当日实际开收盘时间路由 |

## 7. 故障与恢复

- `STATE_INTEGRITY_FAILURE`：任一必需状态文件不可访问、格式错误或跨文件不一致时，**不得在别处初始化，不得交易，不得发正常报告**；只在真源可写时记录本地失败。盘前阶段仍须**写一条“盘前系统故障”消息到 outbox**（§5、§9），webhook 优先取自 `system-state.md`；若连 `system-state.md` 都读不到、拿不到 webhook，则不得猜测或硬编码，只记录本地失败。
- `MARKET_DATA_DEGRADED`：行情延迟、来源冲突或无法核实，但状态文件完整时，所有动作强制 `持有`；盘前/盘中可发送明确标记的数据降级报告，不得交易或把盘中价写为正式估值。
- 云端运行且桌面应用未连接 → 读不到本地状态文件，按 `STATE_INTEGRITY_FAILURE` 处理并结束。
- 历史因证书/授权错误导致的任务失败属于执行缺口，不产生交易，也不写去重键。

## 10. 盘中节奏与数据可行性（2026-07-25 新增）

实测结论：**盘中逐半小时核实 8 持仓 + 5 基准的 ≤20 分钟报价，靠网页抓取不可行。**
7-24 全部运行都是 `MARKET_DATA_DEGRADED`，系统正确地拒绝行动，于是一天产出 13 条
内容相同的"持有 + 降级"——这是设计出来的告警疲劳，而非市场信息。
同一天取**官方收盘价**却轻松做到 8/8 三源零偏差。

据此调整：

- 盘中检查点从"每半小时"改为**只在 ET 10:00 / 12:30 / 15:30 三个锚点**产出报告，
  其余半小时点仍运行（用于风险标记与陈旧度看门狗）但**默认不推送**，
  除非出现 🚨 风险标记或持仓动作发生变化（由内容指纹抑制机制自动处理）。
- 收盘决策（MORNING / POST_CLOSE）保持完整强度——那才是本系统数据可靠的地方。
- 若未来接入有 SLA 的行情源，可恢复更密的盘中节奏；在那之前不假装能做到。

## 11. 高可用设计（2026-07-25 新增）

事故教训：**系统只能在运行时报告，无法报告自己没在运行。** 停摆 6 个交易日期间，
证据一直摆在 `last_successful_official_settlement: 2026-07-16` 里，但无人断言，
而 71% 的空心跳让每次运行看起来都"成功"。

| 机制 | 实现 | 检出对象 |
|---|---|---|
| W1 陈旧度断言 | `staleness_check()` | 估值日落后最近交易日 > 1 个交易日 → `STALE_VALUATION` |
| W2 存活断言 | `liveness_check()` | 距上次运行超阈值 → 系统可能已停摆 |
| W3 死信监控 | `queue_health()` | `failed/` 非空（此前无人查看） |
| W4 积压监控 | `queue_health()` | 最旧待投递消息等待过久（转发器周期实测不稳定） |
| 调度对齐证明 | `verify_schedule_alignment()` | 阶段不可达或 jitter 余量不足 |
| 路径守卫 | `assert_path_usable()` | outbox 落在 TCC 保护区 → 拒绝启动 |
| 每日存活心跳 | 见下 | 让"没消息"变成可判断的信号 |

**故障必须响亮**：所有失败都映射到具名升级项（`STATE_INTEGRITY_FAILURE` /
`ENQUEUE_PATH_UNAVAILABLE` / `STALE_VALUATION` / `SCHEDULE_MISALIGNED` /
`MARKET_DATA_DEGRADED`），由 `tools/preflight.py` 统一输出，退出码非 0 即阻断。

**仍存在的单点**（已知，未消除，不假装已解决）：
1. `~/.local/share` 挂载是入队前提；缺失时记 `ENQUEUE_PATH_UNAVAILABLE` 并结束（响亮失败）。
2. webhook 单一通道，无备用。密钥轮换或撤销将导致全部通知静默——这也是需要存活心跳的原因。**用户决策（2026-07-27）**：明确接受该单点风险，暂不增设备用通道；缓解仅靠每日存活心跳。若未来通知长时间静默，应优先怀疑此通道。
3. 行情依赖无 SLA 的第三方页面。来源可靠性规则见 §9 附录与 `integrity.BAD_SOURCES`。
4. 送达确认异步：一次不发生的运行会让已送达键长期不被回写。
5. 转发器周期实测不稳（曾出现 51 分钟间隔），投递延迟无上界；队列可靠但不保证及时。

## 12. 知识库闭环（2026-07-27 新增，模式来自 nashsu/llm_wiki）

**思想**：像 llm_wiki 那样**增量维护一个持久、互链的知识 wiki**（`knowledge/`），而不是每次运行从零推理。这是 §0"机制以代码为准"的知识层对应物：判断沉淀成页面，页面进入下次判断。

- 结构：`knowledge/index.md`（总目录）｜`tickers/<SYM>.md`（每标的：论点/关键位/财报史/教训）｜`regime/<YYYY-MM>.md`（环境演变）｜`reviews/<YYYY-MM-DD>.md`（每日复盘）｜`lessons.md`（跨标的持久教训，L-xxx 编号，只增不删）。
- 闭环（实现 `lib/knowledge.py`，有测试）：MORNING/POST_CLOSE **决策前读**相关标的页与 lessons，**决策后回写**"事实→动作→理由"；POST_CLOSE 每交易日写复盘并回填昨日"待验证"项。盘前/盘中只读。
- 纪律：增量追加不覆盖；幂等（相同记录不重复）；事实带 as-of 与来源；教训必须写成"下次遇到 X 就做 Y"才能进 lessons.md；缺页返回 None、不臆造。
- 版本化：`knowledge/` 随仓库进 git（`hilyfux/us-market-system`），复盘历史即策略演化史。POST_CLOSE 状态写入后做**本地 commit**（沙箱无网不 push），并在盘后报告末尾提醒待推送提交数（`git rev-list --count @{u}..HEAD`，离线可算）；push 由用户在本机执行。

## 8. 变更记录

- 2026-07-27 · v2.5 — **知识库闭环上线**（§12，模式来自 nashsu/llm_wiki）。新增 `knowledge/` wiki（index/tickers×8/regime/reviews/lessons，已按 2026-07-24 数据播种）与 `lib/knowledge.py`（增量追加、幂等、非法输入拒绝、summary，9 条测试）；SKILL 在 MORNING/POST_CLOSE 强制「读-决策-回写」闭环，POST_CLOSE 每交易日写复盘并回填待验证项。`quote_extract` 7 条 + 槽位 1 条 + 知识 9 条，selftest 92→101 全绿。仓库将推送至 hilyfux/us-market-system（system-state.md 因含 webhook 密钥被 gitignore，另附 example 模板）。
- 2026-07-27 · v2.4 — **模拟盘独立槽位 + 硬约束显式化**。用户明确硬约束：模拟盘初始资金 US$100,000、最多 8 持仓。`slot_report()` 改为 8 槽风险预算**只对模拟持仓计数**，真实持仓单列 `real_tracked`、不占模拟预算（解除"5 真实仓占满、8.5 万现金无槽可用"的结构性死锁）。`tools/selftest.py` 更新 test_slots 至新契约并加 1 例（真实仓数量已知也不占模拟槽），91→92 全绿。**未决（须用户显式授权的红线变更）**：用户提出"盘前设止盈止损、盘中做交易决策、收到信息即可下单"，与现行契约冲突（§3/§4/§10：模拟交易仅 MORNING/POST_CLOSE 可执行，盘前/盘中只分析、不落账）；且 §10 已实测盘中抓取行情不可靠。此项**未实施**，等待显式授权与（若开放盘中执行）可靠行情源 + 对应红线测试。
- 2026-07-27 · v2.3 — **盘前自检发现的一轮优化**。(1) L4 lint 增加**条件/检查语境守卫**（`_CONDITIONAL`）：前瞻检查条件里的动作词（“若…再议减仓”）不再误判，同时保留对当下未标注交易动作的检出力。(2) 新增 `lib/quote_extract.py`：把抓回的行情页文本确定性去噪成 价格/涨跌/as-of/盘后/前收盘 小字典，治理“整页新闻流噪声”，未命中字段返回 None（宁缺勿造）。(3) §5 新增两条**撰写纪律**（篇幅须主动压紧凑；动作词只写进动作行）。(4) 账本：用户确认五个真实持仓各为 US$10,000，RMBS 依已记录入场价 115.00 解冻（数量 86.9565），PWR/MP/BE/KTOS 因缺每股成交价仍冻结、待补（不臆造，CORE-003）。(5) 通知单通道单点：用户明确接受风险、暂不增设备用（§11）。`tools/selftest.py` 补 9 条断言（82→91 全绿）。
- 2026-07-27 · v2.2 — **修复 `ENQUEUE_PATH_UNAVAILABLE` 误报**（间歇性阻断健康运行的根因）。`assert_path_usable()` 旧探针用 write-then-`os.remove`，把 `unlink` 当作可用性硬条件；但 `enqueue()` 只 write+`rename`、从不 unlink，而部分沙箱 FUSE 挂载允许 open/write/rename 却拒绝 unlink（EPERM `[Errno 1]`），导致 outbox 实际可用时误报、preflight 退出 1、MORNING/PREMARKET 等可交易阶段被无谓阻断。改为探针只验证 enqueue 真正依赖的路径（建目录 + 原子写 tmp→rename + 读回），unlink 清理改为尽力而为；探针终名为点文件 `.writeprobe`（非 `.json`），不会被 `queue_state()`/转发器误当成待投消息。**连带修复**：`queue_state()` 的死信计数从「`os.listdir(failed/)` 全量」收敛为「仅 `failed/` 顶层 `.json` 文件」，与 pending 口径一致——此前一个 2 字节探针残留点文件 `.wp` 会被 W3 误报成死信；该修复使 preflight 首次越过 outbox 门后暴露并清理了 3 条历史测试探针残留（已归档至 `failed/archive/`）。`tools/selftest.py` 补 6 条断言（76→82 全绿）：unlink 被拒仍可用（本次回归）、rename/建目录失败仍致命（保留检出力）、探针无 `.json` 残留、死信只计 `.json`。
- 2026-07-25 · v2.1 — §5 新增「可读性与无歧义」强制推送格式标准，并把其**机器可验证子集**做成硬门：新增 `lib/report_lint.py`（L1 标题+日期、L2 篇幅、L3 动作词表/模糊动词、L4 盘前盘中交易动作须标注“建议未执行”、L5 数据时间来源）；`outbox.enqueue()` 默认 `lint=True`，阶段报告不合格抛 `ReportLintError`（响亮失败，`KEY#rN` 重发）；`tools/selftest.py` 补 12 条断言（64→76 全绿）。纯语义类要求（自相矛盾/可两解/省略前提）不在硬门内，由报告生成步骤自检，取高精确低误报以免误杀合规推送。
- 2026-07-17 · v1.0 — 迁移到新电脑（`…/Desktop/Claude`）。抽出本总纲；各 SKILL 精简引用总纲。
- 2026-07-17 · v1.1 — **合并为单一定时任务** `us-market-system`：原 5 个美股任务（晨间/盘前/盘中晚间/盘中凌晨/盘后）改为一个按 ET 自动路由阶段的状态机。原 5 个任务保留为废弃说明。
- 2026-07-24 · v1.2 — 恢复盘中每半小时完整持仓分析；去重键加入分钟；盘中改为只读建议；盘后按交易所实际收盘时间兼容早收盘；拆分状态完整性故障与行情降级；统一调度为 Asia/Singapore。
- 2026-07-25 · **v2.0 — 机制代码化 + 高可用**。抽出 `lib/`（market_core / integrity /
  outbox / state），总纲不再用散文复述机制；新增 `tools/preflight.py`（每次运行的强制
  守卫）与 `tools/selftest.py`（64 条可执行断言）。修复：cron 改为 `0,30 0-5,8,20-23`
  使 MORNING 从"永不触发"变为可达、POST_CLOSE 结算窗口放宽到 20–75 分钟并留 10 分钟
  jitter 余量；**新增检查点吸附**（实测调度延迟 87–137 秒，严格 `minute in (0,30)`
  会使全部盘中运行失效）；账务恒等式换成 C1–C6 有检出力校验；市场环境改为确定性分类；
  槽位语义显式化；`report_key` 支持修订；重复无变化报告自动抑制；行情溯源落到单价级别
  并内置来源黑名单；盘中节奏下调至三个锚点（§10）；新增看门狗 W1–W4（§11）。
- 2026-07-25 · v1.4 — **outbox 迁出 TCC 保护区**：`~/Desktop/Claude/us-stock-outbox` → `~/.local/share/us-stock-outbox`。原因：launchd 转发器每 60s 因 `PermissionError (Errno 1)` 崩溃（累计 ~303KB 错误日志），消息只入队不投递；新位置不受 TCC 保护，**无需完整磁盘访问**。已迁移 `.delivered-keys` / `sent/` / `failed/` / 日志；旧目录留作归档。
- 2026-07-24 · v1.3 — **推送改经 outbox 转发**：沙箱出网被拦、直接 POST 企业微信会 403，故"推送"改为写 `~/Desktop/Claude/us-stock-outbox/` 消息文件，由本机 launchd 转发器代发（§5、§9）。去重改两段式但保持"errcode=0 后才写 alert-state"不变。

## 9. 附录 · outbox 消息契约（推送实现）

**agent 侧**：每次要推送时，**原子写**一个 JSON 文件到 `~/.local/share/us-stock-outbox/`：
- 写法：先写 `<report_key>.tmp`，再 `rename` 成 `<report_key>.json`（避免转发器读到半截文件）。
- 内容：
  ```json
  {
    "report_key": "PREMARKET-2026-07-24",
    "created_at": "<ISO8601>",
    "webhook":    "<从 system-state.md ## Notification 读到的 webhook 原样>",
    "payload":    { "msgtype": "markdown", "markdown": { "content": "<报告 markdown 正文>" } }
  }
  ```
- 写完即视为"已入队"，本次运行结束；**不在沙箱内自己发**。

**转发器侧**（本机、沙箱外、`~/.local/bin/us-stock-outbox-forwarder.py`，由 launchd `com.linqingwang.us-stock-outbox` 每 60s 拉起）：
- 扫 outbox 根目录的 `*.json`，POST 到消息里的 `webhook`（强制校验 host = `qyapi.weixin.qq.com`）。
- outbox 路径由脚本内 `OUTBOX` 默认值决定，可用环境变量 `US_STOCK_OUTBOX` 覆盖；当前默认 `~/.local/share/us-stock-outbox`（非 TCC 保护，无需完整磁盘访问）。
- 解释器（供排障参考）：launchd 下 `#!/usr/bin/env python3` 实际解析为 `/Library/Developer/CommandLineTools/usr/bin/python3`（Python 3.9.6，PATH=`/usr/bin:/bin:/usr/sbin:/sbin`），**不是** `/usr/bin/python3`（那只是转发 shim）。
- `errcode=0` → 追加 `report_key` 到 `.delivered-keys`、归档到 `sent/`；失败重试 5 次后归档 `failed/`；全程写 `forwarder.log`。
- 卸载：删 plist（`~/Library/LaunchAgents/com.linqingwang.us-stock-outbox.plist`）+ 脚本 + outbox 目录即可，无系统级改动。
