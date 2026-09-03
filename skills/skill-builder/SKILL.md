---
name: skill-builder
description: 用于指导后续生成新 skill 或把旧 skill 转换为最新规范的 skill。
---

## What it does

这个 skill 不是脚本执行型 skill，而是一个说明型、规则型 skill。

它用于指导两类任务：

1. 生成新 skill
2. 把旧 skill 转换为最新规范 skill

它的核心作用不是直接执行代码，而是提供统一生成口径、字段规范和避坑规则。

职责边界：

- 指导生成新的 `SKILL.md`
- 指导旧 skill 迁移到最新规范
- 统一 `version / name / category / typical_phase / execution_mode` 的写法
- 统一 `SKILL.md` 顶部只保留必要元数据，不再写 `author` 等非必要字段
- 统一 python 型 skill 以 Python 3.12 为脚本编写基线
- 统一脚本型 skill 的 `dependencies/requirements.txt` 与 `dependencies/.env` 规则
- 约束 skill 边界，避免把多个能力链路混成一个 skill
- 生成或修改 skill 后，要求同步维护技能台账

不负责：

- 自动执行脚本
- 自动创建完整工程目录
- 自动修复运行期依赖
- 自动判断业务逻辑是否正确

## Inputs

适用输入：

- 一个新 skill 的需求描述
- 一个已有 skill 的旧版 `SKILL.md`
- 一组待规范化的字段，如：
  - `name`
  - `description`
  - `category`
  - `typical_phase`
  - `tags`
  - `execution_mode`

建议在使用时至少提供：

- skill 做什么
- 输入输出是什么
- 是否是单能力 skill
- 是否依赖其他 skill
- 当前是生成新 skill 还是迁移旧 skill
- 如果是脚本型 skill，还应明确：
  - 三方 Python 依赖
  - 是否需要 API key / token / secret
  - 是否依赖系统级环境（如 LibreOffice、Tesseract、浏览器）

## Outputs

主要输出应包括：

- 一份符合当前规范的 `SKILL.md` 草稿
- 对字段的规范化建议
- 对潜在问题的 warnings
- 是否应拆 skill / 合并 skill / 改 category / 改 phase 的建议
- `dependencies/requirements.txt` 该怎么写
- `dependencies/.env` 是否需要以及该放哪些变量
- 技能台账需要同步哪些信息

## Execution

1. 判断当前任务是“新建”还是“迁移”
2. 提炼 skill 的单一职责
3. 规范化 `name / category / typical_phase / execution_mode`
4. 检查是否存在以下问题：
   - `name` 与目录名不一致
   - `category` 维度混乱
   - `typical_phase` 过粗
   - `typical_phase` 没有按当前单字段规则填写
   - 把 `typical_phase` 多选数组直接写进正式 skill
   - front matter 顶部混入 `author / owner / maintainer / created_at` 等非必要字段
   - python 型 skill 没有按 Python 3.12 作为编写基线
   - 缺少 `dependencies/requirements.txt`
   - 需要 secret 却缺少 `dependencies/.env`
   - 系统级依赖没有写进正文边界说明
   - 多条执行链路混入同一个 skill
5. 检查依赖文件：
   - `requirements.txt` 只包含实际三方 Python 依赖
   - `.env` 只放 API key / token / secret
   - 只要 skill 依赖 `requirements.txt` 中的三方包，`allow_dynamic_install` 默认应为 `true`
6. 提醒同步技能台账
7. 输出规范化后的 `SKILL.md`
8. 给出必要 warnings

## Resources

- `E:\skill-creator\Skill模板V5.md`

## Constraints

- 不访问外网
- 不直接执行脚本
- 不自动生成完整项目骨架
- 如果目标是脚本型 skill，默认按 Python 3.12 约束生成或转换
- 只输出规则和草稿，不替代人工确认业务边界
- `typical_phase` 当前按单字段生成；多选 phase 只作为待启用能力，不直接写入正式 skill
- front matter 只保留必要元数据，不加入 `author` 等非必要字段
- `requirements.txt` 不应写标准库
- `.env` 不应混入非 secret 配置
- `allow_dynamic_install` 默认应为 `true`，避免依赖已声明但运行期无法安装
- 如果 skill 有系统级依赖，必须写进 `Constraints`
- 生成或修改 skill 后，不能遗漏技能台账更新

## Failure Policy

- 如果需求本身不清晰，应先收敛 skill 的单一职责
- 如果一个 skill 同时覆盖多个执行链路，应优先建议拆分
- 如果只是字段不规范，应输出修正建议而不是直接放弃
- 如果发现依赖声明、密钥声明或台账维护缺失，应直接提示为不完整交付
