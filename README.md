# us-market-system

美股决策系统：单一定时任务按美东时间路由 MORNING/PREMARKET/INTRADAY/POST_CLOSE 四阶段，
账本为唯一真源、数据不可靠时只持有、账务校验通过后才推送（企业微信经 outbox 转发）。

- 总纲（唯一共享规则源）：`SYSTEM.md`
- 机制库：`lib/`（路由/校验/outbox/lint/行情去噪/知识库）
- 可执行规范：`tools/selftest.py`（101 条断言）；每次运行守卫：`tools/preflight.py`
- 知识库闭环（模式来自 [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)）：`knowledge/`
  —— 每日决策前读、决策后回写的持久互链 wiki；复盘历史即策略演化史（SYSTEM.md §12）
- 状态：`portfolio-ledger.md` / `sim-wallet.md` / `strategy-playbook.md` / `alert-state.md`
- `system-state.md` 含 webhook 密钥，被 .gitignore；见 `system-state.example.md`

运行入口（本机调度器每半小时触发）：先 `python3 tools/preflight.py`，非 0 退出即不进入阶段流程。
