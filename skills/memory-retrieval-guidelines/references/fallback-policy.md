# 降级处理

## 1. memory 不可用

- 继续完成当前任务。
- 不把 memory 不可用当作任务失败。
- 必要时说明未使用历史记忆。

## 2. 检索无结果

- 继续基于当前上下文设计或执行。
- 不编造历史约束。

## 3. 契约错误

- 缺少 `fingerprint_status` 时补齐后重试。
- 缺少 `fingerprint` 且需要 procedural retrieval 时，降级到 factual/summary/resident。

## 4. 结果不可信

- 降级为参考线索。
- 用当前代码、测试或用户确认验证后再采用。
