# Gap 台账 —— 「写了却没生效」的恒久可视化

> 目的：三次审计（①教训实效性 ②守卫检出力 ③「写了就算数」全域扫描，2026-08-15）发现的全部缺口集中于此表，每项必须处于三态之一——ENFORCED（机器已强制，附真实测试名）/ CODIFIABLE_PENDING（可代码化、含策略判断故待设计者批准，附落点）/ INHERENTLY_MANUAL（本质人工，附理由）。本台账是设计者决定强制顺序的唯一底册。`tools/selftest.py` 的 `test_gap_ledger` 机械检查三态完整性与 ENFORCED 挙证的真实性（W7 同思想，防虚报）。

## 元缺陷（本台账存在的根本原因）

- **preflight 未 import `lib/selection.py` 与 `lib/knowledge.py`** —— 判断系义务（ACT-004~009 各门、九维打分、扫描、知识回写）在运行时**零强制**：代码存在、selftest 通过，但没有任何 preflight 检查会因「运行时没走这些门」而变红。账目被 40+ 路监视，判断流程零监视——这是三次审计共同指向的根。
- 现状对策 = **W6（到期裁定强制）+ W7（教训状态申告）+ 本台账**。W6 是唯一咬住「判断结果」的硬升级；ORPHAN_REPLACEMENT（本次新增）把「替换必登记 claim」补为第二颗牙。
- **W7 的结构性极限须明记**：W7 只强制「申告的正直」（CODIFIED 必须指向真实测试、PROSE_ONLY 必须给理由），**不强制「行为的遵守」**——一条教训可以永远诚实地停在散文。消除这一极限 = 对本台账 CODIFIABLE_PENDING 项逐项裁定并接入 preflight，此为设计者决策，不得由实现者自行推进。

## 台账

| 编号 | 项目 | 状态 | 依据（ENFORCED=测试名）/ 落点（PENDING）/ 理由（MANUAL） |
|---|---|---|---|
| G-P4 | P4 cache-buster 检出力（无 ?v= 参数即失败） | ENFORCED | `P4 无 cache-buster URL 必须被检出（passed=False）` |
| G-C3 | C3 盈亏分解检出力（总未实现被改必须发） | ENFORCED | `C3 检出力：仅篡改总未实现 -> C3 passed=False` |
| G-C4 | C4 逐仓市值检出力（单仓市值被改必须发） | ENFORCED | `C4 检出力：仅篡改 GEV market_value -> C4 GEV passed=False` |
| G-C5 | C5 逐仓成本一致检出力（单仓未实现被改必须发） | ENFORCED | `C5 检出力：仅篡改 ETN unrealized -> C5 ETN passed=False` |
| G-W3 | W3 死信目录非空必须 ERROR | ENFORCED | `W3 死信非空必须 ERROR 检出` |
| G-W4 | W4 队列积压超时必须 ERROR | ENFORCED | `W4 积压超时必须 ERROR 检出` |
| G-W8 | W8 记分卡落黄（统计充分且命中率<50%） | ENFORCED | `preflight W8：充分样本且命中率<50% -> [WARN] 落黄（检出力）` |
| G-ORP | 替换成交↔claim 登记的即时强制（L-020 根穴） | ENFORCED | `preflight：替换对缺 claim -> 硬升级 ORPHAN_REPLACEMENT 且 ok=False` ＋ `ORPHAN_REPLACEMENT 现实账本+现实 claims 无孤儿（当前必须绿）` |
| G-L010 | L-010 催化日强收盘追高（3 日涨幅 ≤8% 门拦不住的形态；被违反 3 次＝最大实损） | CODIFIABLE_PENDING | 疑与 PEAD（财报后漂移）冲突，须策略裁定。落点：selection.momentum_chase_gate ＋ NVDA 8/07 重放检出力测试 |
| G-L014 | L-014 共识量级 sanity（与最近季度实际偏离 >3 倍拒绝入档） | CODIFIABLE_PENDING | 落点：integrity 入档时检查（共识数据写入前的量级校验） |
| G-L002 | L-002 财报前对既有仓只有「持有」 | CODIFIABLE_PENDING | 落点：decision-log 成交记录 × 财报日程的机械对照（距财报 ≤5 交易日的非持有动作即红） |
| G-L003 | L-003 止盈止损须收盘确认 | CODIFIABLE_PENDING | 落点：trade/decision 记录必须带收盘确认字段，preflight 对照成交表检查 |
| G-L004 | L-004 盘中网页行情不可用于交易 | CODIFIABLE_PENDING | 落点：trade 记录的 valuation_source_date 必须为官方收盘（记录字段机械校验） |
| G-L006 | L-006 代理成本要显式标注 | CODIFIABLE_PENDING | 落点：report_lint 加 PROXY 一致性检查（账本 PROXY 仓在报告与视图里必须带标注） |
| G-L015 | L-015 离场判据须双向执行过才算规则 | CODIFIABLE_PENDING | 落点：alert-state 数值判据登记检查（每个 OPEN 仓必须有已登记的数值判据行） |
| G-L016 | L-016 部分止盈同一事务须生成下一档判据 | CODIFIABLE_PENDING | 落点：减仓 trade 与 alert-state 下一档数值判据的同事务耦合检查 |
| G-L017 | L-017 同源自洽先于跨源一致 | CODIFIABLE_PENDING | 落点：integrity 增加 self-consistency 机器断言（prev_close + change == close） |
| G-L019 | L-019 代理成本仓的时机得分不计入方法有效性证据 | CODIFIABLE_PENDING | 落点：backtest/复盘统计按 PROXY 标记机械排除 |
| G-SCORE | 九维打分的登记（打分被打分：分数须可对照结果） | CODIFIABLE_PENDING | 落点：decision-log 必须落 thesis_score 记录 → preflight 验证件数 == OPEN 仓数 |
| G-SCAN | MORNING 全市场扫描的实施痕迹 | CODIFIABLE_PENDING | 落点：decision-log scan 记录 ≥3 主题 / 8 候选 / 3 行业的机械验证 |
| G-KNOW | 知识回写（决策后 ticker 页必须更新） | CODIFIABLE_PENDING | 落点：成交日的 trade × knowledge/tickers/<sym>.md 当日追记的存在对照 |
| G-PC | POST_CLOSE 复盘 + post-close 结算节 | CODIFIABLE_PENDING | 落点：每交易日 knowledge/reviews/<date>.md 与 data/post-close.md 当日节的存在检查 |
| G-P3 | P3 非数值 figure 崩溃（鲁棒性：守卫自身可被坏输入击穿） | CODIFIABLE_PENDING | 落点：PriceRecord.validate 输入显式校验（非数值 figure → 显式失败而非 InvalidOperation 崩溃） |
| G-L001 | L-001 结论必须来自可复现测试 | INHERENTLY_MANUAL | 过程纪律，约束研发行为而非产物状态；selftest 无法断言自己被引用 |
| G-L005 | L-005 行业情绪≠公司破坏 | INHERENTLY_MANUAL | 「有无已核实的公司减值」依赖人工事实调查，机械不可判 |
| G-L007 | L-007 「能通过的检查」不等于「检查对了东西」 | INHERENTLY_MANUAL | 元纪律，无机器化的元断言可逐守卫核查；本台账已强制各行是其逐项局部执行 |
| G-L011 | L-011 基本面超预期≠价格上涨 | INHERENTLY_MANUAL | 仍是 playbook HYP-001 假设，教训本身要求攒样本；未成规则故无可断言行为 |
| G-L018 | L-018 单日 ≥5% 波动须写明当日驱动事实（事实侧） | INHERENTLY_MANUAL | 「当日驱动事实」是否存在依赖人工调查；其复检侧同型义务已由 W6 承担 |
| G-B2 | 价格溯源口径乖离：黑名单源被用作结算「双源」（8/11 LNG 以 stockinvest.us 为第二源，P2 违反）且 `PriceRecord.validate`（P1–P5）未配线到实结算路径，机器未拦截 | CODIFIABLE_PENDING | 落点：结算路径配线 PriceRecord.validate（P1–P5 机器执行）或按 sources.md 晋升规则先整合。sources.md 与 system-state 已附更正注记（2026-08-15，值本身与核准源 0.00% 一致故数值未受影响）；源列表的晋升/删除属策略判断，本次仅登记 |
| G-B6 | 判定门槛二重定义：learning.scorecard 的 min_sample=20 与 backtest.MIN_TRADES_FOR_SIGNIFICANCE=20 各自硬编码，改一处会静默漂移 | CODIFIABLE_PENDING | 落点：scorecard 既定值改为引用 backtest 常数。注意 lib/backtest.py 与 tools/backtest.py 同名，import 解析依赖调用方 sys.path 顺序（隐式耦合），须先消歧后改，故本次仅登记不改 |
| G-RO | 1MB 级状态文件多重读取（portfolio-ledger.md / system-state.md 在一次运行内被多处各自重读，read-once 缺失） | CODIFIABLE_PENDING | 落点：一次读取、显式传递的读取层（preflight 的 ORPHAN 检查已顺手合并为单次读取，其余调用点待统一，属结构改动须设计者批准） |
| G-RSIM | tools/routing_sim.py 与 lib/market_core.route 乖离的二重实现（路由逻辑两处并存，漂移即假证明） | CODIFIABLE_PENDING | 落点：routing_sim 改为委托 market_core.route 或删除（保留与否属设计者判断，本次不动） |
| G-STATE | system-state.md 再肥大（约 3459 行 / ~1MB，持续追加使读取变慢并加剧 G-RO） | CODIFIABLE_PENDING | 落点：月度轮转归档 + 尺寸上限检查（轮转属状态文件结构变更，须设计者批准） |
| G-SAVE | save_claims 未配线：裁定流程要求 `save_claims()` 落盘，但没有任何检查证明运行时真的调用了它（与元缺陷同型：代码存在≠被执行） | CODIFIABLE_PENDING | 落点：裁定日翌交易日起 claims.jsonl 不得残留已到期 OPEN（W6 已部分咬合）＋ run-summary 与 claims 落盘状态的机械对照 |
| G-CLOSE1 | G-CLOSE 引け窓執行への移行 · Phase 1（routing/証明/文書）：CLOSING 阶段＝引け20分前 in-session 執行窓を route() に実装（日历 close_time 追従・16:00 非依存）、提案発火 ET15:40 が MOC 締切前に CLOSING 命中を証明、SYSTEM/SKILL に口径反映 | ENFORCED | `CLOSING (a) 15:45 ET 普通日 -> CLOSING（收盘执行窗）` ＋ `CLOSING (d) 早收盘日 12:45 ET -> CLOSING（close=13:00 自动追従、窓 12:40–13:00）` ＋ `提案cron ET15:40+jitter 命中 CLOSING 且 MOC 15:50 前有余裕` ＋ `CLOSING 境界：15:40 ET -> CLOSING（窓下端 close-20、包含）` |
| G-CLOSE2 | G-CLOSE 引け窓執行への移行 · Phase 2（ライブcron切替、2026-08-17 実施）：OS 定時タスク（cron `0,30,40 0-5,8,20-23`）＋preflight.REQUIRED_CRON を同時に分40 追加へ更新（引け20分前 ET15:40＝夏SGT03:40/冬SGT04:40 発火）、CLOSING を STAGES 編入して五阶段全可達を再証明。実行タイミングだけ現実化（記帳口径は不変）。分割：CLOSING＝①既存仓分析・仓位管理・替換執行／POST_CLOSE＝②市場レビュー＋戦略見直し（不変）。ライブ OS 定時タスクは repo と lockstep で同値更新済み | ENFORCED | `CLOSING (g) preflight.REQUIRED_CRON に分40 追加済み（ライブ cron と一致）` ＋ `CLOSING (g) CLOSING は STAGES（ライブ到達性契約）に編入済み` ＋ `CLOSING (g) 新 cron 全阶段到达 ok=True（SCHEDULE_MISALIGNED なし・脆弱点なし）` ＋ `必须五阶段（含 CLOSING）全可达且稳健` |
| G-PRICE | T-20min価（引け20分前）の適用範囲を「CLOSING約定フィル価格＋その保有成本」のみに限定（2026-08-17 用户裁定＝過剰統一の巻き戻し）：当初 addendum が valuation/mark-to-market/NAV・データ門 ACT-001・離場判定 ACT-002/003 まで T-20min価に統一したのを「取引専用であり翌日の取引戦略分析には含まれない・取引価格と保有成本にのみ影響」との裁定で過剰と判断し差し戻し。**評価・離場・分析・戦略レビュー・データ門は全て公式收盘（従来どおり）**；POST_CLOSE は公式收盘で mark-to-market 評価・結算・valuation 更新（読み取り専用への縮小は撤回）。closing_window_price は sources.md/integrity に登録維持だが CLOSING約定フィル専用に限定、L-004/L-021 の例外も約定フィル限定に狭め、L-003/L-017/L-022 は公式收盘必須に復帰。C1 会计恒等式は price ラベル不問で挙動不変 | ENFORCED | `(a) SYSTEM.md：CLOSING約定フィル価格＝T-20min価（保有成本もこれに由来）が明记` ＋ `(b1) strategy-playbook：ACT-002/003 離場は official close（T-20min 完全不在）` ＋ `(c) SYSTEM.md §4.3：POST_CLOSE は公式收盘で valuation/結算（読み取り専用でない）` ＋ `(c2) lib/integrity.py：valuation 入力＝公式收盘价（T-20min は valuation に用いない）` ＋ `(d) lessons L-004：例外が約定フィル限定・分析/評価/離場は公式收盘` ＋ `(e) sources.md：closing_window_price 登録維持＋CLOSING約定フィル専用に限定` |
