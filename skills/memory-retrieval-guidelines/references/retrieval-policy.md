# 读取策略

## 1. 选择工具

- 使用 `memory_retrieve_context`：需要面向当前任务组装上下文。
- 使用 `memory_query_layer`：只需要查看某一层 memory 内容。
- 使用 `memory_health`：需要确认 memory 服务是否可用。
- 使用 `memory://defaults`：需要确认默认 tenant、scope 或 transport。

## 2. retrieve_context 输入

- `task_request_id`：当前任务 ID。
- `query`：当前任务目标或问题。
- `fingerprint`：当前环境指纹，已知时传入。
- `fingerprint_status`：必须显式传入。
- `include_factual`：需要事实记忆时开启。
- `include_procedural`：需要经验流程时开启。
- `limit`：按任务复杂度控制。

## 3. query_layer 使用

可查询层：

- `resident`
- `factual`
- `procedural`
- `summary`
- `candidate`

只在需要调试或验证某一层时使用，不把它作为默认入口。
