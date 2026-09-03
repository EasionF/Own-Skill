---
version: v5
name: ppt-master
display_name: PPT Master
description: 将 PDF、DOCX、网页、Markdown 或对话需求转换为项目化 PPT 产物，支持内容导入、项目初始化、SVG 后处理与 PPTX 导出，适用于生成演示文稿、整理 PPT 工程、执行导出流水线和调用相关脚本工具的场景。
category: presentation/ppt-master
typical_phase: orchestration
execution_mode: both
enabled: true
tags:
  - ppt
  - svg
  - pptx
  - workflow
  - presentation
  - export
input_schema:
  type: object
  required:
    - argv
  properties:
    argv:
      type: array
      description: 传给 skill 入口的命令参数数组，第一个元素为子命令。
      items:
        type: string
    cwd:
      type: string
      description: 可选工作目录，默认使用 skill 根目录。
    env:
      type: object
      description: 传给子进程的附加环境变量。
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
      description: 标准输出、标准错误和返回码等执行信息。
    artifacts:
      type: array
      items:
        type: string
      description: 生成的文件产物路径。
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
  allowed_paths:
    - "*"
  allowed_domains:
    - "*"
  allow_process_spawn: true
  allowed_secrets:
    - GEMINI_API_KEY
    - OPENAI_API_KEY
    - QWEN_API_KEY
    - DASHSCOPE_API_KEY
  max_runtime_seconds: 1800
  max_memory_mb: 2048
  max_output_bytes: 5242880
  dependency_source: platform_managed
  allow_dynamic_install: false
  retryable: true
  cacheable: false
  side_effect_level: high
---

## What it does

协调 PPT 工程的初始化、素材导入、脚本调用、SVG 后处理和 PPTX 导出。
既可以作为命令分发入口直接执行子命令，也可以作为完整工作流中的统一执行节点。

## Inputs

- `argv`：子命令参数数组，例如 `["init", "demo"]`、`["export", "<project_path>"]`。
- `cwd`：可选工作目录，用于解析相对路径。
- `env`：可选附加环境变量，用于网页抓取、图像生成和导出流程。

## Outputs

- `status`：执行状态。
- `summary`：执行摘要，包含子命令或流水线信息。
- `outputs.stdout` / `outputs.stderr` / `outputs.returncode`：脚本执行结果。
- `artifacts`：导出的 PPTX 或显式输出文件路径。

## Execution

1. 解析 `argv` 并识别目标子命令。
2. 为项目管理、导出和后处理命令选择对应脚本。
3. 在需要时串行执行 `total_md_split.py`、`finalize_svg.py`、`svg_to_pptx.py`。
4. 汇总标准输出、错误信息和产物路径。
5. 以统一结构返回执行结果。

## Resources

- `scripts/main.py`
- `scripts/project_manager.py`
- `scripts/finalize_svg.py`
- `scripts/svg_to_pptx.py`
- `scripts/total_md_split.py`
- `scripts/pdf_to_md.py`
- `scripts/doc_to_md.py`
- `scripts/web_to_md.py`
- `scripts/web_to_md.cjs`
- `references/canvas-formats.md`
- `references/shared-standards.md`
- `references/strategist.md`
- `references/executor-base.md`
- `references/executor-general.md`
- `references/executor-consultant.md`
- `references/executor-consultant-top.md`
- `references/image-generator.md`
- `references/template-designer.md`
- `references/create-template-workflow.md`
- `references/module-overview.md`
- `references/change-log.md`
- `references/delivery-standards.md`
- `templates/`

## Constraints

- 依赖本地 Python/Node 运行环境和若干第三方库。
- 会读写项目目录、导入用户文件并生成中间产物，副作用较高。
- 某些子流程需要网络访问、外部模型或网页抓取能力。
- 压缩包已移除历史 demo、legacy、副本镜像和缓存文件，但保留主流程所需脚本、模板与引用文档。
- 程序性说明统一收敛到 `references/`，不再保留 `workflows/` 目录。

## Failure Policy

- 子命令返回非零退出码时直接判定失败。
- 导出流水线任一步失败时停止后续步骤并返回错误。
- 缺少项目路径、输入参数或运行依赖时直接失败。
- 不对失败结果做静默降级，错误信息原样回传。
