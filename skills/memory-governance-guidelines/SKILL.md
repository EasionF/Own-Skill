---
name: memory-governance-guidelines
description: Memory / host-capture 治理规范。用于用户要求跑治理、阶段结束、多条候选写入后，先检查宿主对话和任务执行证据是否完整，再运行完整 host-capture governance，并按需刷新 Memory MCP summary、resident snapshot、index 和 lifecycle。只负责治理和汇报，不负责普通候选写入。
---

# Memory 治理规范

## 默认行为

- 用户说“启动治理”“跑治理”“做治理”时，默认执行完整治理，而不是只刷新低层 summary/resident/index。
- 大任务结束、多条候选写入后、需要刷新 resident/summary/index/lifecycle 时，才运行治理；小任务不要频繁治理。
- governance 失败不应回滚已完成任务，但必须说明失败原因、影响范围和补救动作。
- 治理前必须先判断本次是“全部线程增量治理”“指定线程治理”还是“低层 Memory MCP 刷新”。

## 完整治理路径

默认完整治理路径：

1. 确认治理目标范围。用户没有明确限定时，默认治理全部线程自上次治理以来的增量；只有用户明确说“当前线程”或指定 thread/session id 时，才限定到当前线程或指定线程。
2. 先运行本地全线程增量扫描脚本 `.codex\scripts\codex-governance-incremental-scan.ps1`，读取 `.codex\sessions\**\rollout-*.jsonl` 中全部宿主线程的增量聊天记录、tool call、MCP 调用、命令输出和任务执行步骤记录。
3. 检查扫描报告中的用户纠偏、失败、candidate drop、文件变更、工具异常，先人工判断哪些应该提升为 memory / knowledge / skill / rule。
4. 运行 `memory_preview_host_governance`，检查输入完整度、候选类型和缺失项。
5. 如果 MCP preview 在未指定 `thread_id` 时仍然自动选择单个线程，必须标记为“工具层不支持默认全部线程增量”，并把本地扫描报告作为补偿证据。
6. 对可能写入 memory / knowledge / skill / rule / governance evidence 的操作执行安全检查；如工具可用，使用 `rule_gate_check`。
7. 运行 `memory_run_full_governance`。
8. 按参数刷新 Memory MCP summary、resident snapshot、index 和 lifecycle。
9. 按“产物优先”的格式汇报结果。

如果完整治理工具不可用，再退回 HTTP / Ops Console 或低层 `memory_run_governance`，但必须明确标注“低层治理 / 输入不完整”，不能声称已经完成完整宿主治理。

如果完整治理工具可用但默认只选择单线程，也不能声称完成了全部线程增量治理；必须先使用本地全线程增量扫描报告补齐候选判断。

## 增量输入契约

完整治理不是只读取当前最后几条消息，也不是只读取当前所在聊天线程，更不是只读取 Memory MCP 里已有对象。除非用户明确限定“当前线程”或指定线程，否则它必须拿到全部线程“自上次治理以来”的增量输入。

必须包含：

1. 全部线程的增量聊天记录：用户新增要求、澄清、纠偏、偏好、拒绝项、确认结论。
2. 全部线程的增量任务执行步骤：计划、工具调用、命令、文件编辑、验证、失败、重试、最终产物。
3. 增量决策证据：为什么选择某个方案、为什么放弃某个方案、哪些边界被用户明确确认。
4. 增量产物证据：新增/修改的文件路径、生成的文档、图、配置、脚本、数据库或外部系统状态。
5. 增量异常证据：工具失败、MCP drop、权限问题、编码问题、路径问题、未完成项。

如果拿不到上述增量，必须在治理汇报里标注“输入不完整”，并说明缺了哪一类。不能只用统计数字替代证据说明。

## 低层 MCP 工具边界

- `memory_run_governance` 只是低层刷新步骤。
- 它负责基于 Memory MCP 数据库生成 conversation summary、重建 resident、同步 index、执行 lifecycle。
- 它不会自动读取当前 Codex/OpenClaw 线程 transcript，也不能替代 host-capture governance。
- 只有用户明确要求“只刷新 resident/index/lifecycle”时，才把它当作主路径。

## 输入完整性检查

运行前必须判断本次治理类型：

1. 全部线程增量治理：默认模式。需要读取 Codex / Claude Code / OpenClaw / OpenCode 等宿主全部线程自上次治理以来的增量聊天记录，以及全部增量任务执行步骤。
2. 指定线程治理：只有用户明确说“当前线程”或指定 thread/session id 时使用。此时必须在汇报中标注治理范围被用户限定。
3. 低层 Memory MCP 治理：只刷新 Memory MCP 数据库里的 task/message/artifact/candidate/memory/rule/skill/knowledge 对象。

如果 host-capture preview 只产生 `governance_evidence_candidate`，没有 memory / knowledge / skill / rule 候选，必须说明“本轮只是证据保留型治理”，不要强行声称完成了长期层沉淀。

## 产物优先汇报规则

每次治理完成后，必须先展示实际产物，再展示运行统计。

必须包含：

1. 实际记录了什么：列出新增、更新、退役或保持不变的 memory、knowledge、skill、rule、evidence、summary、resident snapshot、index、lifecycle 产物。
2. 内容摘要是什么：用人能看懂的话说明这些产物记录了什么，不要只给 ID。
3. 什么没记录：如果 memory / knowledge / skill / rule 没有新增，必须明确说没有，并解释原因。
4. 去哪里检查：给出文件路径、bundle ID、memory ID、snapshot ID 或其他可验证句柄。
5. 下一步补救：如果本次只保留证据或刷新状态，没记录用户真正想记录的内容，必须直接说明“不够”，并给出下一步应该写 skill、写 rule、写 memory 还是重新治理。

运行数字只作为辅助诊断，包括 message 数、command 数、tool-call 数、MCP-call 数、candidate 数。不要把这些数字当成主要结果。

## 四层汇报口径

治理汇报按四层说清楚：

1. Memory：用户偏好、事实、长期可复用经验、历史决策是否被写入、更新、退役或未变化。
2. Knowledge：知识库、证据包、索引、可检索资料是否被生成、同步、保留或未变化。
3. Skill：执行流程、工具使用规范、可复用操作方法是否写入或更新到对应 skill。
4. Rule：强制约束、准入检查、禁止项、默认行为是否写入或更新到规则层。

如果治理结果字段是英文，保留英文原文并附中文解释。不要只给 ID；必须解释这些 ID 对应的动作和影响。

## 层级划分原则

- 写 Skill：操作流程、执行方法、工具使用步骤、输出格式、某类任务应该怎么做。比如“治理默认必须读取全部线程的增量聊天记录和增量任务执行步骤”“治理完成后要产物优先汇报”。
- 写 Rule：强制约束、禁止项、必须遵守的边界。比如“不能只报统计数字就声称治理完成”。
- 写 Memory：用户长期偏好、已验证事实、历史决策、环境约束。比如“用户偏好学习型内容用费曼学习法解释”。
- 写 Knowledge：外部资料、项目研究结论、可检索文档、证据包。比如 OpenClaw 某个模块的字段说明和链路整理。
- 写 Evidence：本次执行证据、命令结果、工具调用记录、原始 transcript。Evidence 是治理依据，不等于已经沉淀成 Memory/Skill/Rule。

## Reference 使用

- 治理策略：`references/governance-policy.md`
- 运行参数：`references/run-options.md`
- 失败处理：`references/failure-policy.md`
