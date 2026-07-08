---
name: expert-skill-forge
description: >
  把某领域人类专家的隐性判断力锻造成 AI 可稳定执行的高质量 skill 的方法论工具。
  适用于任何"AI 做出来的东西永远是 generic 平均值"的场景，不限定领域。
  Invoke when: 用户想做一个新 skill / 现有 skill 效果不理想想诊断原因 /
  想把专家经验封装成可复用 AI 能力 / 提到 huashu-design 或 ppt-master 作为参照 /
  用户说"AI 做出来的东西不够专业"或"纠正方向不对"。
---

# Expert Skill Forge

## 描述

大部分人做 skill 失败的原因不是 prompt 写得不够长，是**方法论用错了**——以为质量来自"更好的 AI"或"更精巧的 prompt 措辞"，其实质量来自三样东西：**把专家的隐性判断翻译成显性规则、用强制流程逼 AI 不偷懒、建立资产体系让产出可复用**。

huashu-design（17k+ star）和 ppt-master（3万+ star）这两个真实跑出效果的开源项目，领域不同（一个做网页设计、一个做 PPT），但底层遵循同一套方法论。这个 skill 把这套方法论提炼成可执行的六阶段流程，用于锻造任何领域的专家级 skill。

**核心解决的问题**：你在没有诊断框架的情况下凭直觉纠正，纠正力气花对了地方（确实在改），但方向靠猜，猜对猜错全看运气。这个 skill 的作用就是在动手改之前，先逼自己（或协助你的 Agent）走一遍固定的诊断顺序，把"该往哪个方向纠正"从"凭感觉"变成"按流程推导"。

## 使用场景

- 想让 AI 稳定产出某个专业领域的高质量成果（设计/文案/代码架构/数据分析/任何有"内行看得出好坏"标准的领域）
- 现在已经有一个 skill/prompt，但效果总是"看起来还行，但没有内行的味道"，想知道问题出在哪
- 发现自己做出来的东西总是 AI 训练语料的"最大公约数"（设计永远是紫渐变圆角卡片，文案永远是"赋能""闭环"这类空话）
- 想把自己或者某个专家的隐性经验，变成可以稳定复用、可以教给别人（或 AI）执行的东西
- 在纠正一个 skill 的效果问题前，需要先诊断"到底该往哪个方向纠正"

## 不适用场景

- 任务本身没有"内行标准"，纯粹是信息检索/格式转换类任务，不需要专家判断力
- 一次性、不会重复使用的任务——skill 的投入产出比建立在"反复使用"上，一次性任务直接让 AI 做就行

## 六阶段流程（编排层）

> 每个阶段的详细执行指导见 [references/phase-guides.md](references/phase-guides.md)。主文件只讲流程顺序和加载时机，不展开细节——避免每次调用都吃掉整个方法论，信号被稀释。

| 阶段 | 一句话目标 | 完成标志 | 何时加载详细指导 |
|---|---|---|---|
| **1. 收窄问题** | 把"AI 做 XX"收窄到"AI 做的 XX，问题具体是 ___，导致 ___" | 能写出具体痛点句式 | 进入此阶段时读 phase-guides.md §1 |
| **2. 研究真人专家** | 说清"一个真正的 [专家] 拿到任务，第一步做什么、第二步做什么" | 能口述专家工作流程 | 读 phase-guides.md §2 + assets/expert-interview-template.md |
| **3. 隐性→显性** | 把"有品味"拆成可判断是/否的规则，不留形容词 | 每条规则能被外行人执行 | 读 phase-guides.md §3（最难最核心的一步） |
| **4. 强制流程** | 设计"必须先 A 再 B"+"必须产出多个变体"的顺序 | 流程里有强制顺序 + 多变体环节 | 读 phase-guides.md §4 |
| **5. 资产体系** | 让这个 skill 用过一次后留下可复用的沉淀 | 能说出"第二次用会比第一次好在哪" | 读 phase-guides.md §5 |
| **6. 真实验证** | 真的跑一次端到端案例，让局外人评判 | 局外人能看出"像专家做的" | 读 phase-guides.md §6 + references/self-check.md |

## 按需加载的参照资源

- **[references/case-studies.md](references/case-studies.md)** — huashu-design 和 ppt-master 的逐阶段剖析。在需要"好例子长什么样"时加载，不是每次都读。
- **[references/anti-patterns.md](references/anti-patterns.md)** — "凭直觉纠正"的常见症状和对应的正确方向。在感觉"改了但没改对"时**优先加载**——这是这个 skill 为什么要存在的直接原因。
- **[references/self-check.md](references/self-check.md)** — 六步自查清单。写完 skill 后逐条打勾。
- **[assets/methodology-canvas.md](assets/methodology-canvas.md)** — 空白方法论画布，用于新领域时填充。
- **[assets/expert-interview-template.md](assets/expert-interview-template.md)** — 专家工作流程访谈模板，用于第 2 步。

## 触发条件

```json
{
  "keywords": ["做一个skill", "AI帮我做", "设计一套流程", "专家经验",
               "怎么让AI做得更专业", "AI做出来的东西不够好", "AI生成的太generic",
               "参考huashu-design", "参考ppt-master", "纠正方向不对",
               "skill效果不理想", "把经验封装成skill"],
  "context_signals": [
    "已有一个 prompt/skill 但效果不理想，想诊断原因",
    "打算把某个人类专业能力封装成可复用的 AI 能力",
    "对比研究成功的开源 skill/prompt 项目",
    "反复纠正一个 skill 的效果但始终不到位"
  ]
}
```

## 作用域

- **Origin scope**：通用方法论，抽取自 huashu-design + ppt-master 逆向分析，不绑定任何具体项目或领域
- **Availability scope**：可在任何需要设计专家级 skill 的场景下复用（设计/写作/代码/数据/任何专业判断类任务）
- **不适用**：纯信息检索、格式转换、一次性任务

## 关于这个 skill 自身的设计

这个 skill 自身也遵循它教的第 5 条原则（资产体系），做了文件分离——不是把所有东西塞进一个 SKILL.md：

- `SKILL.md`（本文件）是**编排层**：每次调用都会被读，所以只放流程概览和加载时机，不放细节
- `references/` 是**细节层**：按需加载，避免 context 膨胀
- `assets/` 是**可复用工具层**：模板、画布
- `accumulated/` 是**运行时积累层**：你用这个 skill 锻造过哪些 skill、踩过哪些坑。初始为空，随使用增长。详见 [accumulated/index.md](accumulated/index.md)

这是刻意的——如果这个 skill 自己都把方法论塞进一个文件，它就没有资格教别人做资产分离。
