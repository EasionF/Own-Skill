# Own-Skill

自用 trae skill 集合仓库，收录自己开发/扩展的 skill，与第三方示例仓库隔离。

> 这里只放**自己开发或深度扩展**的 skill，不放 Anthropic/第三方原版的 skill。

## 目录结构

```
Own-Skill/
├── README.md
├── .gitignore
└── skills/
    ├── expert-skill-forge/          # 通用：如何把专家隐性判断力锻造成高质量 skill
    │   ├── SKILL.md
    │   ├── references/
    │   ├── assets/
    │   └── accumulated/
    └── cc-design/                   # 基于 huashu-design 扩展的 trae design skill
        ├── SKILL.md
        ├── references/
        ├── assets/
        ├── demos/
        ├── prototypes/
        ├── scripts/
        └── style-demos-v3.1/
```

## 设计原则

- 每个 skill 独立目录，包含 `SKILL.md` 和引用资源
- `SKILL.md` 是编排层，保持精简；详细内容放在 `references/` 按需加载
- `assets/` 放可复用工具模板
- `accumulated/` 放运行时积累（初始为空，随使用增长）
- 不要把所有内容塞进一个 `SKILL.md`

## 当前 skill

| skill | 作用 |
|---|---|
| [expert-skill-forge](skills/expert-skill-forge/SKILL.md) | 把某领域人类专家的隐性判断力锻造成 AI 可稳定执行的高质量 skill 的方法论工具 |
| [cc-design](skills/cc-design/SKILL.md) | 基于 huashu-design 扩展的 trae design skill，让 AI 像设计师一样工作 |

## 使用方式

在 trae 中新增或更新 skill 时：

1. 在这个仓库修改 skill 源码
2. 同步到 IDE 的 `~/.trae-cn/skills/` 目录
3. 测试验证后再 commit + push
