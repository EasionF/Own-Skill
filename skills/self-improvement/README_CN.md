通过经验积累，如：
    命令/操作意外失败
    用户纠正的时候
    请求不存在能力，claude当前能力不足


触发层（脚本做的事）
activator.sh 每次 prompt 提交后输出一段 XML 注入到上下文：
<self-improvement-reminder>
    After completing this task, evaluate if extractable knowledge emerged...
</self-improvement-reminder>
就是一段提示词，Claude 读到后自己决定要不要记录。error-detector.sh 更简单，检测 bash 输出里有没有 error: / Traceback 等关键词，有就输出一段提醒。
评估层（Claude 自己做的事）
"这条 learning 够不够通用"没有任何算法，完全是 Claude 依据 SKILL.md 里写的判断标准自己决定：

    有没有 2+ 个 See Also 链接
    状态是不是 resolved
    是不是非项目特有

生成层（extract-skill.sh 做的事）
脚本只做一件事：创建一个空的 SKILL.md 骨架文件，所有 TODO 占位符都留着：
然后 Claude 读取 assets/SKILL-TEMPLATE.md 里的格式规范，把 .learnings/ 里的那条 learning 内容填进这个骨架，生成完整的 SKILL.md。
本质上：这整个 self-improving 机制就是"提示词注入 + Claude 自我判断 + 文件读写"，没有向量数据库、没有评分模型、没有任何传统意义上的 ML。骨架脚本只负责文件操作，所有智能判断都在 Claude 的上下文里发生。

这个会有个问题，上下文会爆炸，.learnings/文件越用会越长，可能里面的东西都是有用的有价值的。我们可以结合我们的存入向量数据库中，通过向量检索，查出每次要添加的额外提示词

# self-improving-agent — 中文说明

**来源**：https://github.com/peterskoett/self-improving-agent
**版本**：v1.0.11
**发布者**：社区第三方（ClawHub），非 Anthropic 官方出品

## 核心功能

让 Agent 在每次对话中持续积累经验——把错误、纠正、知识盲区、功能需求实时记录到 `.learnings/` 目录下的 Markdown 文件，经过沉淀后晋升为项目级永久记忆（CLAUDE.md、AGENTS.md 等），甚至抽取成可复用的新 Skill。

## 触发场景

- 命令/操作意外失败
- 用户纠正 Claude（"不对"、"其实应该是..."）
- 用户请求当前不存在的能力
- 外部 API 或工具调用失败
- Claude 发现自己的知识已过时或有误
- 发现某个反复出现的任务有更好的处理方式
- 开始重大任务前，主动回顾已有 learnings

## 三类记录文件

| 文件 | 记录内容 | ID 前缀 |
|------|---------|---------|
| `.learnings/LEARNINGS.md` | 纠正、知识盲区、最佳实践 | `LRN-` |
| `.learnings/ERRORS.md` | 命令失败、异常、工具错误 | `ERR-` |
| `.learnings/FEATURE_REQUESTS.md` | 用户请求但当前不支持的能力 | `FEAT-` |

ID 格式：`TYPE-YYYYMMDD-XXX`（如 `LRN-20250115-001`）

## 晋升机制（Promotion）

当某条 learning 反复出现或具有普遍适用性时，晋升到永久记忆文件：

| 目标文件 | 适合的内容 |
|---------|---------|
| `CLAUDE.md` | 项目约定、已知坑、所有 Claude 交互都需要知道的事 |
| `AGENTS.md` | Agent 工作流、工具使用模式、自动化规则 |
| `.github/copilot-instructions.md` | GitHub Copilot 的项目上下文 |
| `SOUL.md` | 行为准则、沟通风格（OpenClaw 专用） |
| `TOOLS.md` | 工具能力、集成坑（OpenClaw 专用） |

晋升触发条件（Simplify & Harden 规则）：`Recurrence-Count >= 3` + 跨至少 2 个不同任务 + 30 天内发生

## Skill 抽取机制

当某条 learning 足够通用时，可直接抽取为新 Skill：

```bash
./scripts/extract-skill.sh skill-name --dry-run  # 预览
./scripts/extract-skill.sh skill-name             # 执行
```

抽取标准：有 2+ 个相关 `See Also` 链接 / 状态为 `resolved` / 非项目特有 / 用户明确要求保存

## Hook 集成（自动触发）

在 `.claude/settings.json` 配置 hook 后可自动触发：

| 脚本 | Hook 类型 | 作用 |
|------|----------|------|
| `scripts/activator.sh` | UserPromptSubmit | 每次提交 prompt 后提醒评估是否需要记录 |
| `scripts/error-detector.sh` | PostToolUse（Bash） | 命令报错时自动触发记录 |

token 开销约 50-100 token/次。

## 支持的 Agent 环境

| 环境 | 触发方式 |
|------|---------|
| Claude Code | Hook 自动触发（推荐） |
| Codex CLI | Hook 自动触发 |
| GitHub Copilot | 手动（无 hook 支持） |
| OpenClaw | Workspace 注入 + 跨 session 消息传递 |

## 文件结构

```
self-improving-agent/
├── SKILL.md
├── _meta.json
├── .learnings/                    ← 预置的空白记录文件模板
│   ├── ERRORS.md
│   ├── FEATURE_REQUESTS.md
│   └── LEARNINGS.md
├── assets/
│   ├── LEARNINGS.md               ← 记录文件模板
│   └── SKILL-TEMPLATE.md          ← 新 Skill 抽取模板
├── hooks/openclaw/
│   ├── HOOK.md
│   ├── handler.js
│   └── handler.ts
├── references/
│   ├── examples.md
│   ├── hooks-setup.md
│   └── openclaw-integration.md
└── scripts/
    ├── activator.sh               ← UserPromptSubmit hook
    ├── error-detector.sh          ← PostToolUse hook
    └── extract-skill.sh           ← Skill 抽取助手
```
