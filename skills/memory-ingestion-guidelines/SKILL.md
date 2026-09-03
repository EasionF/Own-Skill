---
name: memory-ingestion-guidelines
description: Memory 写入规范。用于将已验证的设计决策、修复经验、失败模式、环境约束、可复用流程或重要事实写入 Memory MCP。只负责写入候选记忆，不负责读取或治理。
---

# Memory 写入规范

## 默认行为

- 只写入对未来任务可复用的信息。
- 优先写入已验证结果，不写临时猜测。
- 使用 `memory_ingest_candidate` 写入候选记忆。
- 写入前过滤敏感信息、凭据、私密数据和噪声。
- 写入内容必须有来源、验证状态和副作用分类。

## 应该写入

- 已确认的关键设计决策。
- 验证通过的修复经验。
- 稳定复现的失败模式。
- 明确的环境约束。
- 可复用的执行流程。
- 影响后续任务的接口、数据、权限或部署约束。

## 不应该写入

- 未验证猜测。
- 临时日志。
- 用户私密信息。
- 凭据、token、密钥。
- 一次性无复用价值的中间状态。
- 与当前任务无关的闲聊内容。

## Reference 使用

- 候选记忆策略：`references/candidate-policy.md`
- 验证状态：`references/verification-policy.md`
- 安全过滤：`references/safety-policy.md`
