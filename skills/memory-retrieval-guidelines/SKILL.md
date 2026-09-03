---
name: memory-retrieval-guidelines
description: Memory 读取规范。用于需要从 Memory MCP 读取历史上下文、设计决策、失败经验、事实层、resident snapshot、summary 或 procedural 经验时。只负责读取和使用记忆，不负责写入或治理。
---

# Memory 读取规范

## 默认行为

- 需要历史上下文、相似经验、既有约束或设计决策时读取 memory。
- 优先使用 `memory_retrieve_context` 组装任务上下文。
- 调试单层数据时使用 `memory_query_layer`。
- 读取前可用 `memory_health` 或 `memory://health` 判断服务状态。
- memory 不可用时降级继续任务，不中断当前工作。
- memory 结果作为上下文输入，不作为绝对事实。

## 使用规则

- 读取前明确当前任务问题和检索目的。
- `fingerprint_status` 必须显式传入。
- `matched` 时可以使用 procedural memory。
- `matched_or_na` 时可以使用 factual、summary、resident，谨慎使用 procedural。
- `mismatch` 时不要把 procedural memory 当作当前环境可执行经验。
- `unknown` 时保守使用，只作为参考线索。
- 与当前代码、用户输入或实时事实冲突时，以当前证据为准。

## 常见场景

- 设计前查历史架构约束和类似设计。
- 执行前查类似修复、常见失败和环境差异。
- 调试前查历史错误模式。
- 评审前查历史质量问题和已知限制。

## Reference 使用

- 读取策略：`references/retrieval-policy.md`
- 结果使用：`references/result-usage.md`
- 降级处理：`references/fallback-policy.md`
