## 文档名称

PPT Master 模块说明

Author: Wang Wei Yuan
Time: 2026-03-30

## 适用范围

用于说明 `ppt-master` 打包副本的主要模块、调用关系、输入输出流转和审查关注点，方便集成、评审和版本管理。

## 功能数据流转

用户需求或源材料  
-> `scripts/main.py` 分发命令  
-> `scripts/project_manager.py` 初始化项目或导入素材  
-> 各类转换脚本把源内容转成 markdown 或项目资产  
-> SVG 处理脚本整理导出所需页面资源  
-> `scripts/svg_to_pptx.py` 输出 PPTX  
-> 返回执行摘要、产物路径和错误信息

## 详细代码模块

### 入口与路由

- `scripts/main.py`
  统一 async 入口，分发 `init`、`import-sources`、`validate`、`info`、`export`、`smoke`、`outline-to-md` 以及直接脚本调用。

### 项目管理

- `scripts/project_manager.py`
  负责项目创建、源文件导入、markdown 归一化和项目结构校验。
- `scripts/project_utils.py`
  提供项目格式识别和共享校验能力。

### 源内容转换

- `scripts/pdf_to_md.py`
  PDF 转 markdown。
- `scripts/doc_to_md.py`
  Office 与文档格式转 markdown。
- `scripts/web_to_md.py`
  网页内容转 markdown。
- `scripts/web_to_md.cjs`
  适配部分高限制网页抓取场景。

### 视觉处理

- `scripts/finalize_svg.py`
  导出前统一整理 SVG 结果。
- `scripts/text_layout_audit.py`
  检查文本溢出和布局异常。
- `scripts/embed_icons.py`
  处理图标嵌入。
- `scripts/embed_images.py`
  处理图片嵌入。
- `scripts/crop_images.py`
  处理图片裁切。
- `scripts/fix_image_aspect.py`
  修正图片比例问题。

### 导出相关

- `scripts/total_md_split.py`
  拆分讲稿备注。
- `scripts/svg_to_pptx.py`
  导出 native PPTX 与 SVG reference PPTX。
- `scripts/svg_to_shapes.py`
  尽可能将 SVG 转成可编辑原生形状。

### 指引文档

- `references/strategist.md`
- `references/executor-base.md`
- `references/executor-general.md`
- `references/executor-consultant.md`
- `references/executor-consultant-top.md`
- `references/shared-standards.md`
- `references/create-template-workflow.md`

## 审查要点

- 确认每个入口命令的职责边界。
- 确认关键字段、输出结构和错误返回。
- 确认导出链路中的前后依赖关系。
- 确认文件读写路径与产物位置。
- 确认依赖、约束和剩余风险说明。
