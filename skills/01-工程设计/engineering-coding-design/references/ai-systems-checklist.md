# AI/Agent/RAG/MCP 工程设计检查表

AI 项目也必须按工程系统设计。额外关注不确定性、可评测性、权限边界、工具副作用和行为漂移。

## 1. AI 组件边界

- 模型负责什么。
- Prompt 负责什么。
- Tool 负责什么。
- Memory 负责什么。
- Retrieval 负责什么。
- 规则、策略或传统代码负责什么。
- 哪些决策不能交给模型。

## 2. Agent 状态机

- 任务生命周期。
- 输入状态。
- 计划状态。
- 工具调用状态。
- 等待用户确认状态。
- 成功终态。
- 失败终态。
- 可恢复状态。
- 不可恢复状态。

## 3. Tool 调用契约

- 工具名称和职责。
- 输入 schema。
- 输出 schema。
- 错误语义。
- side effect 分类。
- 幂等性。
- 超时。
- 重试策略。
- 审计字段。

## 4. Memory 策略

- 什么时候 retrieve。
- 什么时候 query layer。
- 什么时候 ingest candidate。
- 什么时候 governance。
- 需要哪些 fingerprint 或环境约束。
- mismatch 时如何降级。
- memory 不可用时如何继续。

## 5. Retrieval 与上下文组装

- 查询来源。
- 检索范围。
- rerank 或过滤规则。
- 上下文预算。
- 冲突信息处理。
- 引用和证据保留。
- 过期信息处理。

## 6. Prompt 与策略

- System prompt 职责。
- Skill 职责。
- 用户指令优先级。
- 安全策略。
- 工具使用策略。
- 输出格式策略。
- 不确定性表达策略。

## 7. 评测与回归

- Golden cases。
- Eval dataset。
- Tool call 回归。
- Retrieval 质量评估。
- Prompt 回归。
- 行为漂移检测。
- 人工评审样本。
- 失败样本沉淀。

## 8. 安全与权限

- 哪些 tool 有副作用。
- 哪些操作需要人工确认。
- 文件系统、网络、数据库、外部 API 的权限边界。
- 敏感信息处理。
- Prompt injection 风险。
- Tool injection 风险。
- 越权调用风险。

## 9. 错误与降级

- 模型调用失败。
- 工具调用失败。
- Retrieval 失败。
- Memory 失败。
- 上下文超限。
- 输出不符合 schema。
- 幻觉或不确定结果。
- fallback model 或 fallback path。

## 10. Trace 与审计

- 任务 ID。
- Step ID。
- Tool call trace。
- Prompt/version trace。
- Memory usage trace。
- Model/version trace。
- 决策记录。
- 人工确认记录。

## 11. MCP 专项

- Tools/resources 列表。
- stdio 日志边界。
- 输入 schema 与后端契约一致性。
- 错误码稳定性。
- Client config 模板。
- doctor 检查项。
- fake backend 与 real backend 验证边界。
- pack/install 验证。
