# 验证状态

## 1. verification_status

建议使用清晰状态：

- `verified_fix`：修复已验证。
- `verified_design_decision`：设计决策已确认。
- `verified_environment`：环境事实已确认。
- `observed_failure`：失败已观察但未修复。
- `unverified_candidate`：仅候选，不得作为稳定事实。

## 2. side_effect_class

按实际影响填写：

- `none`
- `read_only`
- `external_resource`
- `state_change`
- `approval`

## 3. 写入前检查

- 是否已验证。
- 是否对未来有复用价值。
- 是否有明确适用条件。
- 是否会泄露敏感信息。
- 是否有可追溯来源。
