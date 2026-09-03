---
name: script-skill-optimizer
description: Find script-backed skills from marketplaces or public sources, normalize them to the user's local skill template, test and fix them, store them under the optimized-skill folders, and update the skill inventory Excel.
---

# Script Skill Optimizer

用于把外部脚本型 skill 拉取、规范化、测试、修复、归档，并同步更新技能清单。

## 适用范围

- 只处理真正带脚本的 skill。
- 优先来源：
  - marketplace
  - skillsmp
  - awesome skill 列表
  - 公开仓库或可下载技能包
- 不默认接收纯提示词、纯方法论、纯说明文档型 skill。
- 不默认使用大厂官方 skill 仓库，除非用户明确要求。

## 硬性要求

- 候选 skill 必须存在 `SKILL.md`。
- 必须存在真实可执行内容，例如：
  - `scripts/`
  - shell 脚本
  - Python 入口
  - Node 入口
  - 其他可执行 helper
- 不允许直接修改原始来源包，必须创建规范化副本。

## 用户模板目标

始终对齐用户本地 skill 模板规范；若原模板文件缺失，则继续沿用以下规则作为强制标准。

## 目录结构要求

每个规范化后的 skill 根目录只允许保留：

- `SKILL.md`
- `scripts/`
- `references/`
- `assets/`
- `tests/`

必须清理：

- `__pycache__`
- `.pyc`
- zip / rar / 7z 等压缩包
- 根目录重复脚本
- 与交付无关的缓存文件

## 命名规则

- skill 文件夹名必须全小写。
- 只能使用字母、数字和 `-`。
- 禁止使用 `_`。
- 所有目录名与 `name` 一律使用 `-` 连接，不允许出现 `_`。
- `SKILL.md` 中的 `name` 必须与文件夹名完全一致。
- 如发现 `_`，必须重命名为 `-`，并同步修改 `name`。

## SKILL.md Frontmatter 规则

frontmatter 必须能被标准 YAML 解析器稳定解析。

### 禁止事项

- 元数据中出现空行
- 零宽字符
- 占位符值
- 空字符串占位
- 任意导致 YAML 解析失败的内容

### 明确禁止的占位值

- `xxx`
- `todo`
- `tbd`
- `...`
- `|`

### 必填字段

- `version`
- `name`
- `display_name`
- `description`
- `category`
- `typical_phase`
- `execution_mode`
- `enabled`
- `tags`
- `input_schema`
- `output_schema`
- `execution`
- `runtime`

### 当前模板标准

- `version: v4`
- `enabled: true`

### execution 规则

- 必须存在统一入口。
- script 型 skill 一律按异步入口建模。
- `execution.entry.async` 必须为 `true`。

推荐结构：

```yaml
execution:
  kind: python
  entry:
    module: scripts.main
    function: run
    async: true
```

### runtime 规则

必须补齐以下字段：

- `network_access`
- `sandbox`
- `allowed_paths`
- `allowed_domains`
- `allow_process_spawn`
- `allowed_secrets`
- `max_runtime_seconds`
- `max_memory_mb`
- `max_output_bytes`
- `dependency_source`
- `allow_dynamic_install`
- `retryable`
- `cacheable`
- `side_effect_level`

推荐结构：

```yaml
runtime:
  network_access: false
  sandbox: required
  allowed_paths: []
  allowed_domains: []
  allow_process_spawn: false
  allowed_secrets: []
  max_runtime_seconds: 120
  max_memory_mb: 512
  max_output_bytes: 1048576
  dependency_source: bundled_only
  allow_dynamic_install: false
  retryable: true
  cacheable: false
  side_effect_level: low
```

### 正文固定 section

- `## What it does`
- `## Inputs`
- `## Outputs`
- `## Execution`
- `## Resources`
- `## Constraints`
- `## Failure Policy`

## 可用性和阻塞规则

### 已优化

- 结构已按模板规范化
- 统一入口已建立
- 基础校验已通过

### 可直接调用

- 已优化
- 不依赖外部账号、OAuth、API key、认证 CLI

### 已验证可用

- 已优化
- 不依赖外部账号、OAuth、API key、认证 CLI
- 本机 smoke 已跑通

如果存在以下任一情况，不允许归入“可直接调用”或“已验证可用”：

- API key
- OAuth
- 外部登录账号
- 认证 CLI
- 付费远程服务

## 测试流程

1. 语法校验
2. 入口校验
3. `tests/smoke.json` 业务化 smoke
4. 失败则修复
5. 修复后重测

常用方式：

- Python：`python -m py_compile`
- Node：`node --check`
- Shell：`bash -n`

优先再做：

- `--help`
- dry-run
- 最小真实输入

## 存储位置

总目录：

- `E:\skills-汇总`

主目录：

- `E:\skills-汇总\已优化skill`
- `E:\skills-汇总\可直接调用skill`
- `E:\skills-汇总\已验证可用skill`

## Excel 更新规则

更新文件：

- `E:\skills-汇总\skills清单.xlsx`

至少包含列：

- `skill名称`
- `功能`
- `category`
- `是否已优化`
- `外部账号/API阻塞`
- `归属人`
- `路径`

规则：

- `功能` 优先取 skill 自带中文说明。
- 没有中文说明时，再退到中文 `description`。
- `归属人` 固定为 `修远`。
- `外部账号/API阻塞 = 是` 的单元格标红。

## 执行流程

1. 发现 skill
2. 判断是否属于 script-backed
3. 下载或复制来源
4. 规范化目录
5. 重写 `SKILL.md`
6. 修正文件夹名与 `name`
7. 建立 `scripts/main.py`
8. 补 `tests/smoke.json`
9. 运行测试
10. 修复问题
11. 放入目标目录
12. 更新 Excel

## 审计要求

每次批量处理后，至少检查：

- 文件夹名是否含 `_`
- `name` 是否含 `_`
- frontmatter 是否可解析
- frontmatter 是否存在空行
- `execution.entry.async` 是否为 `true`
- `runtime` 是否补齐

## 汇报要求

- 明确区分：
  - 新增了什么
  - 修了什么
  - 测了什么
  - 还剩什么阻塞
- 不把“语法通过”表述成“可用”
- 不把有外部阻塞的 skill 表述成“可直接调用”
