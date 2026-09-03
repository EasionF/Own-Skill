---
version: v5
name: brand-pptx-outline-skill
display_name: Brand PPTX Outline Skill
description: 根据品牌主题、受众、用途和语气生成可直接供 PPT 流程消费的结构化 outline.json，适用于品牌叙事大纲生成、品牌提案前置策划和品牌型 PPT 内容骨架定义。
category: presentation/brand-pptx-outline-skill
typical_phase: authoring
execution_mode: direct_tool
enabled: true
tags:
  - brand
  - ppt
  - outline
  - strategy
  - json
input_schema:
  type: object
  required:
    - topic
  properties:
    topic:
      type: string
      description: 品牌 PPT 的主题或品牌对象。
    count:
      type: integer
      description: 期望生成的页面数量，默认 10 页。
      default: 10
    audience:
      type: string
      description: 目标受众，如管理层、投资人、渠道伙伴。
    purpose:
      type: string
      description: 生成目的，如品牌发布、品牌解读、战略沟通。
    tone:
      type: string
      description: 期望语气，如克制、理性、清晰。
    focus:
      type: string
      description: 叙事重点，如品牌主张、产品语言、体验系统。
    model:
      type: string
      description: 可选模型名，默认读取环境变量。
    api_key:
      type: string
      description: 可选 API Key，未提供时读取环境变量。
    output:
      type: string
      description: 可选输出文件路径；提供后会落盘 outline.json。
    dry_run:
      type: boolean
      description: 为 true 时不发起模型调用，只返回归一化后的本地占位大纲。
      default: false
output_schema:
  type: object
  required:
    - status
    - summary
  properties:
    status:
      type: string
      enum: [success, failed]
    summary:
      type: string
    outputs:
      type: object
      description: 结构化执行结果与 outline 数据。
    artifacts:
      type: array
      items:
        type: string
      description: 写出的文件产物路径列表。
    error:
      type: object
      description: 失败时的错误信息。
execution:
  kind: python
  entry:
    module: scripts.main
    function: run
    async: true
runtime:
  network_access: true
  sandbox: required
  allowed_paths: []
  allowed_domains:
    - dashscope.aliyuncs.com
  allow_process_spawn: false
  allowed_secrets:
    - QWEN_API_KEY
    - DASHSCOPE_API_KEY
  max_runtime_seconds: 180
  max_memory_mb: 512
  max_output_bytes: 1048576
  dependency_source: platform_managed
  allow_dynamic_install: false
  retryable: true
  cacheable: false
  side_effect_level: low
---

## What it does

生成品牌型 PPT 的结构化 `outline.json`，只定义叙事顺序、页面角色与内容边界。
不负责视觉设计、版式、模板选择、配色、字体和图标方案。

## Inputs

- `topic`：品牌主题或品牌对象，是生成大纲的核心输入。
- `count`：输出页数，默认按 10 页品牌叙事框架生成。
- `audience`：受众类型，用于调整叙事角度。
- `purpose`：沟通目的，用于约束大纲目标。
- `tone`：语气要求，用于控制叙事风格。
- `focus`：重点关注的品牌维度。
- `model` / `api_key`：模型调用配置。
- `output`：可选输出路径。
- `dry_run`：仅做本地归一化，不调用外部模型。

## Outputs

- `status`：执行状态。
- `summary`：结果摘要。
- `outputs.outline`：归一化后的 `outline.json` 数据。
- `outputs.payload`：格式化 JSON 文本。
- `artifacts`：写入的文件路径。

## Execution

1. 校验输入并补齐默认参数。
2. 生成品牌大纲提示词。
3. 在正常模式下调用模型并解析 JSON。
4. 对结果做页序、字段和角色归一化。
5. 按需写出 `outline.json` 文件并返回结构化结果。

## Resources

- `scripts/main.py`
- `references/module-overview.md`
- `references/change-log.md`
- `references/delivery-standards.md`
- 运行时环境变量：`QWEN_API_KEY`、`DASHSCOPE_API_KEY`

## Constraints

- 依赖外部模型服务；无有效 API Key 时无法正式生成。
- 只输出内容大纲，不输出视觉设计参数。
- 默认不启动子进程，不动态安装依赖。

## Failure Policy

- 缺少必填输入或 API Key 时直接失败。
- 模型返回非 JSON 或无法解析时直接失败。
- 输出文件写入失败时直接失败并返回错误信息。
