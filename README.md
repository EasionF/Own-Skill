# Own-Skill

个人 Codex / Trae / AI Coding Skill 收藏库。按能力域分类，便于快速检索和安装。

> 收录来源：自研扩展 + Anthropic 官方示例 + OpenAI 官方示例 + 社区高 Star 项目。  
> 全部保留原始 LICENSE / 署名信息，详见各 skill 目录。

## 目录结构

\\\
Own-Skill/
├── README.md                          # 本文档（索引 + 说明）
├── .gitignore
└── skills/
    ├── 🏗️ 工程设计/                     # 工程设计 & 架构规范
    ├── ⚙️ 开发执行/                      # 开发执行流程规范
    ├── 🔍 问题诊断/                      # 调试 & 问题排查
    ├── 🧠 知识推理/                      # 思维 & 推理框架
    ├── 🎨 前端设计/                      # 前端 UI/UX & 可视化
    ├── 📊 PPT/文档/数据/                  # 办公自动化
    ├── 🔗 飞书工具链/                     # 飞书全家桶集成
    ├── 🛠️ Skill 制作/                     # 制作 & 发布 Skill
    ├── 🔌 Codex 扩展/                   # Plugin / MCP / Hook
    ├── 🌀 Anthropic 官方/               # Anthropic 官方 Skills
    ├── 🤖 OpenAI 官方/                   # OpenAI 官方 Skills
    └── 🧰 超级工具包/                     # Superpowers 全家桶
\\\

## 分类索引

### 🏗️ 工程设计规范

| Skill | 说明 |
|---|---|
| [engineering-coding-design](skills/engineering-coding-design/SKILL.md) | 工程级编码设计规范 — 架构调整、模块设计、接口契约 |
| [engineering-coding-execution](skills/engineering-coding-execution/SKILL.md) | 工程级编码执行规范 — 修复 bug、重构落地、补测试 |

### ⚙️ 开发执行流程

| Skill | 说明 |
|---|---|
| [interview](skills/interview/SKILL.md) | 需求访谈 — 需求模糊时触发，智能访谈 + SPEC 生成 |
| [pua](skills/pua/SKILL.md) | 证据优先执行模式 — 硬核任务、持续卡死时切换 |
| [self-improvement](skills/self-improvement/SKILL.md) | 自我改进 — 捕获失败教训，持续优化 |
| [superpowers-brainstorming](skills/superpowers-brainstorming/SKILL.md) | 头脑风暴（Superpowers 版） |
| [review-agent](skills/review-agent/SKILL.md) | 提交前验证（Codex 内置） |
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | 系统性调试 — 发现 bug 后首选用 |

### 🔍 问题诊断

| Skill | 说明 |
|---|---|
| [systematic-debugging](skills/systematic-debugging/SKILL.md) | 系统性调试方法论，防御性边界控制 |
| [superpowers-systematic-debugging](skills/superpowers-systematic-debugging/SKILL.md) | Superpowers 版调试，含压力测试用例 |
| [pua](skills/pua/SKILL.md) | 证据优先模式，绕过反复失败陷阱 |
| [codex-plugin-runtime-debug](skills/codex-plugin-runtime-debug/SKILL.md) | Skill/Plugin/MCP/Hook 运行时问题排查 |

### 🧠 知识 & 推理

| Skill | 说明 |
|---|---|
| [learning-explanation-guidelines](skills/learning-explanation-guidelines/SKILL.md) | 费曼学习法 — 把复杂内容讲清楚 |
| [memory-preflight](skills/memory-preflight/SKILL.md) | 记忆预检 — 工程实现前必读 |
| [memory-retrieval-guidelines](skills/memory-retrieval-guidelines/SKILL.md) | 记忆读取规范 |
| [memory-ingestion-guidelines](skills/memory-ingestion-guidelines/SKILL.md) | 记忆写入规范 |
| [memory-governance-guidelines](skills/memory-governance-guidelines/SKILL.md) | 记忆治理规范 |
| [memory-guard](skills/memory-guard) | Memory 守卫，防止敏感信息泄漏 |

### 🎨 前端 & 设计

| Skill | 说明 |
|---|---|
| [cc-design](skills/cc-design/SKILL.md) | 品牌设计 — 让 AI 像设计师一样工作 |
| [frontend-design](skills/frontend-design/SKILL.md) | 前端设计 — 组件化、TypeScript、状态管理 |
| [visualize](skills/visualize/SKILL.md) | 数据可视化 — 对话内生成图表 |
| [architecture-diagrams-d2](skills/architecture-diagrams-d2/SKILL.md) | 架构图生成 — D2 语言绘制架构图 |

### 📊 PPT / 文档 / 数据

| Skill | 说明 |
|---|---|
| [ppt-master](skills/ppt-master/SKILL.md) | PPT 工程项目管理 — PDF/DOCX → PPTX |
| [brand-pptx-outline-skill](skills/brand-pptx-outline-skill/SKILL.md) | 品牌叙事大纲生成 |
| [presentations](skills/presentations/SKILL.md) | PowerPoint 创建与编辑 |
| [documents](skills/documents/SKILL.md) | Word/Docx 文档创建与编辑 |
| [pdf](skills/pdf/SKILL.md) | PDF 读取、创建、表单处理 |
| [spreadsheets](skills/spreadsheets/SKILL.md) | Excel/XLSX/CSV 电子表格 |
| [template-creator](skills/template-creator/SKILL.md) | 模板 Skill 创建工具 |

### 🔗 飞书工具链

| Skill | 说明 |
|---|---|
| [lark-im](skills/lark-im/SKILL.md) | 飞书即时通讯 — 收发消息、管理群聊 |
| [lark-doc](skills/lark-doc/SKILL.md) | 飞书云文档 — 读取和编辑在线文档 |
| [lark-base](skills/lark-base/SKILL.md) | 飞书多维表格 — 建表、字段、视图 |
| [lark-sheets](skills/lark-sheets/SKILL.md) | 飞书电子表格 — 批量读写数据 |
| [lark-calendar](skills/lark-calendar/SKILL.md) | 飞书日历 — 创建会议、预定会议室 |
| [lark-task](skills/lark-task/SKILL.md) | 飞书任务 — 创建和管理待办 |
| [lark-wiki](skills/lark-wiki/SKILL.md) | 飞书知识库 — 知识空间与节点管理 |
| [lark-mail](skills/lark-mail/SKILL.md) | 飞书邮箱 — 起草、发送、搜索邮件 |
| [lark-slides](skills/lark-slides/SKILL.md) | 飞书幻灯片 — 创建和编辑 |
| [lark-markdown](skills/lark-markdown/SKILL.md) | 飞书 Markdown — 查看、创建、编辑 |
| [lark-contact](skills/lark-contact/SKILL.md) | 飞书通讯录 — 解析用户信息 |
| [lark-drive](skills/lark-drive/SKILL.md) | 飞书云盘 — 文件管理、导入导出 |
| [lark-vc](skills/lark-vc/SKILL.md) | 飞书视频会议 — 历史记录、参会人 |
| [lark-vc-agent](skills/lark-vc-agent/SKILL.md) | 飞书视频会议会中能力 |
| [lark-approval](skills/lark-approval/SKILL.md) | 飞书审批 — 查询和处理审批实例 |
| [lark-attendance](skills/lark-attendance/SKILL.md) | 飞书考勤打卡记录查询 |
| [lark-minutes](skills/lark-minutes/SKILL.md) | 飞书妙记 — 音视频转文字 |
| [lark-note](skills/lark-note/SKILL.md) | 飞书会议纪要直查 |
| [lark-okr](skills/lark-okr/SKILL.md) | 飞书 OKR 管理 |
| [lark-openapi-explorer](skills/lark-openapi-explorer/SKILL.md) | 飞书 OpenAPI 探索工具 |
| [lark-skill-maker](skills/lark-skill-maker/SKILL.md) | 飞书 CLI 自定义 Skill 制作 |
| [lark-event](skills/lark-event/SKILL.md) | 飞书实时事件监听 |
| [lark-whiteboard](skills/lark-whiteboard/SKILL.md) | 飞书画板 — 查看和编辑 |
| [lark-shared](skills/lark-shared/SKILL.md) | 飞书 CLI 认证/授权共享规范 |
| [daily-report-evidence](skills/daily-report-evidence/SKILL.md) | 工作日报证据汇总 |
| [lark-workflow-standup-report](skills/lark-workflow-standup-report/SKILL.md) | 日程待办摘要工作流 |
| [lark-workflow-meeting-summary](skills/lark-workflow-meeting-summary/SKILL.md) | 会议纪要整理工作流 |

### 🛠️ Skill 制作

| Skill | 说明 |
|---|---|
| [skill-creator](skills/skill-creator/SKILL.md) | 创建自定义 Codex Skill（完整流水线） |
| [skill-builder](skills/skill-builder/SKILL.md) | Skill 制作方法论指导 |
| [skill-installer](skills/skill-installer/SKILL.md) | Skill 安装工具 |
| [expert-skill-forge](skills/expert-skill-forge/SKILL.md) | 把专家判断力锻造成 AI Skill |
| [script-skill-optimizer](skills/script-skill-optimizer/SKILL.md) | 脚本类 Skill 优化与存储 |

### 🔌 Codex 扩展

| Skill | 说明 |
|---|---|
| [plugin-creator](skills/plugin-creator/SKILL.md) | 创建 Codex Plugin |
| [codex-plugin-runtime-debug](skills/codex-plugin-runtime-debug/SKILL.md) | Plugin 运行时问题排查 |
| [codex-sync-workflow](skills/codex-sync-workflow/SKILL.md) | 双机 Codex 同步工作流 |
| [mcp-builder](skills/mcp-builder) | MCP Server 构建指南 |
| [imagegen](skills/imagegen/SKILL.md) | AI 图片生成 Skill |
| [browser-use](skills/browser-use/SKILL.md) | 浏览器自动化操作 |
| [computer-use](skills/computer-use/SKILL.md) | 桌面 UI 表单操作 |
| [windows-browser-use](skills/windows-browser-use) | Windows 版浏览器使用 |
| [windows-computer-use](skills/windows-computer-use) | Windows 版桌面操作 |

### 🌀 Anthropic 官方示例

| Skill | 说明 |
|---|---|
| [algorithmic-art](skills/algorithmic-art) | 算法艺术生成 |
| [canvas-design](skills/canvas-design) | Canvas 设计 |
| [doc-coauthoring](skills/doc-coauthoring) | 文档协作 |
| [docx](skills/docx) | Word 文档处理 |
| [frontend-design](skills/frontend-design) | 前端设计 |
| [internal-comms](skills/internal-comms) | 企业内部通讯 |
| [pdf](skills/pdf) | PDF 处理 |
| [pptx](skills/pptx) | PowerPoint 处理 |
| [slack-gif-creator](skills/slack-gif-creator) | Slack GIF 制作 |
| [theme-factory](skills/theme-factory) | 主题工厂 |
| [web-artifacts-builder](skills/web-artifacts-builder) | Web 产物构建 |
| [webapp-testing](skills/webapp-testing) | Web 应用测试 |
| [xlsx](skills/xlsx) | Excel 处理 |
| [brand-guidelines](skills/brand-guidelines) | 品牌规范 |
| [graphify](skills/graphify) | 代码库图谱分析 |

### 🤖 OpenAI 官方

| Skill | 说明 |
|---|---|
| [openai-docs](skills/openai-docs/SKILL.md) | OpenAI API 文档检索 |
| [superpowers-api-curated](skills/superpowers-api-curated) | Superpowers API 技能集 |
| [circleci](skills/circleci) | CircleCI CI/CD |
| [sentry](skills/sentry) | Sentry 错误追踪 |

### 🧰 超级工具包（Superpowers）

| Skill | 说明 |
|---|---|
| [superpowers-using-superpowers](skills/superpowers-using-superpowers/SKILL.md) | 超级工具包使用入门 |
| [superpowers-brainstorming](skills/superpowers-brainstorming/SKILL.md) | 头脑风暴 |
| [superpowers-writing-plans](skills/superpowers-writing-plans/SKILL.md) | 编写实施计划 |
| [superpowers-executing-plans](skills/superpowers-executing-plans/SKILL.md) | 执行计划 |
| [superpowers-dispatching-parallel-agents](skills/superpowers-dispatching-parallel-agents/SKILL.md) | 并行 Agent 调度 |
| [superpowers-subagent-driven-development](skills/superpowers-subagent-driven-development/SKILL.md) | 子 Agent 驱动开发 |
| [superpowers-requesting-code-review](skills/superpowers-requesting-code-review/SKILL.md) | 请求代码评审 |
| [superpowers-receiving-code-review](skills/superpowers-receiving-code-review/SKILL.md) | 接收代码评审反馈 |
| [superpowers-finishing-a-development-branch](skills/superpowers-finishing-a-development-branch/SKILL.md) | 完成开发分支 |
| [superpowers-using-git-worktrees](skills/superpowers-using-git-worktrees/SKILL.md) | Git Worktree 隔离开发 |
| [superpowers-systematic-debugging](skills/superpowers-systematic-debugging/SKILL.md) | 系统性调试 |
| [superpowers-test-driven-development](skills/superpowers-test-driven-development/SKILL.md) | 测试驱动开发 |
| [superpowers-verification-before-completion](skills/superpowers-verification-before-completion/SKILL.md) | 提交前验证 |
| [superpowers-writing-skills](skills/superpowers-writing-skills/SKILL.md) | 编写 Skills |
| [superpowers-hooks](skills/superpowers-hooks) | Superpowers Hooks |
| [superpowers-curated](skills/superpowers-curated) | Superpowers 精选集 |

---

## 使用方式

在 Trae / Codex 中引用：

`
# 方式1：直接引用 skill 名
/skill skill-name

# 方式2：安装到本地后使用
cp -r skills/skill-name ~/.trae-cn/skills/
`

## 更新日志

- 2026-09-03: 首次全量同步，纳入 84 个 skill，1778 个文件
