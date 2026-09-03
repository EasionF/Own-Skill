## 文档名称

PPT 模板创建流程说明

Author: Wang Wei Yuan
Time: 2026-03-30

## 适用范围

用于在 `ppt-master` 中新增模板目录、生成模板文件，并校验模板是否满足库内使用要求。

## 功能数据流转

用户提出模板需求  
-> 收集模板信息  
-> 创建模板目录  
-> 调用 `template-designer.md` 指引生成模板  
-> 校验模板完整性  
-> 输出模板路径与文件清单

## 详细步骤

### 1. 收集模板信息

确认以下内容：

| 项目 | 是否必填 | 说明 |
|------|----------|------|
| 模板名称 | 是 | 英文标识，例如 `my_company` |
| 模板显示名 | 是 | 便于文档和管理识别 |
| 参考来源 | 否 | 现有项目或模板路径 |
| 主色值 | 否 | HEX 颜色值 |
| 设计风格 | 否 | 使用场景与设计语气 |

如有参考来源，先检查其目录结构与资产情况。

### 2. 创建模板目录

在 `templates/layouts/<new_template_name>/` 下创建模板目录。

### 3. 生成模板内容

读取并遵循 [template-designer.md](./template-designer.md)，生成以下内容：

1. `design_spec.md`
2. `01_cover.svg`
3. `02_chapter.svg`
4. `03_content.svg`
5. `04_ending.svg`
6. 可选 `02_toc.svg`

### 4. 校验模板完整性

至少检查：

- `design_spec.md` 是否存在
- 必需 SVG 是否齐全
- SVG `viewBox` 是否正确
- 占位符是否统一使用 `{{PLACEHOLDER}}`

### 5. 返回结果

输出模板名称、模板路径、已生成文件和缺失项。

## 审查要点

- 检查模板目录命名是否规范。
- 检查模板设计说明与 SVG 文件是否一致。
- 检查颜色、占位符和版式是否保持一致。
- 检查是否错误依赖了项目级临时文件。

## 备注

- SVG 技术约束以 [template-designer.md](./template-designer.md) 为准。
- 本文档归类到 `references/`，因为它是过程指引，不是运行时脚本入口。
