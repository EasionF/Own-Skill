# cc-Design

> *「打字。回车。一份能交付的设计。」*

用 HTML 做高保真原型、幻灯片、动画、可视化与专家评审的 skill。在你的 agent 里打一句话，拿回一份能交付的设计。

3 到 30 分钟，你能 ship 一段**产品发布动画**、一个能点击的 App 原型、一套能编辑的 PPT、一份印刷级的信息图。

## 装上就能用

```
npx skills add EasionF/cc-design
```

然后在 Claude Code / Codex / Cursor / Trae 等任意支持 skills 的 agent 里直接说话：

```
「做一份 AI 心理学的演讲 PPT，推荐 3 个风格方向让我选」
「做个 AI 番茄钟 iOS 原型，4 个核心屏幕要真能点击」
「把这段逻辑做成 60 秒动画，导出 MP4 和 GIF」
「帮我对这个设计做一个 5 维度评审」
```

## 能做什么

| 能力 | 交付物 | 典型耗时 |
|------|--------|----------|
| 交互原型（App / Web） | 单文件 HTML · 真 iPhone bezel · 可点击 · Playwright 验证 | 10–15 min |
| 演讲幻灯片 | HTML deck（浏览器演讲）+ 可编辑 PPTX（文本框保留） | 15–25 min |
| 时间轴动画 | MP4（25fps / 60fps 插帧）+ GIF（palette 优化）+ BGM | 8–12 min |
| 设计变体 | 3+ 并排对比 · Tweaks 实时调参 · 跨维度探索 | 10 min |
| 信息图 / 可视化 | 印刷级排版 · 可导 PDF/PNG/SVG | 10 min |
| 设计方向顾问 | **三套逻辑并行**（秒数轮盘 + 现实参照获奖站 + 最佳设计师）· 直接出 3 版真实视觉 | 5 min |
| 5 维度专家评审 | 雷达图 + Keep/Fix/Quick Wins · 可操作修复清单 | 3 min |

## 核心机制

### 品牌资产协议

涉及具体品牌（Stripe、Linear、Anthropic、自家公司等）时强制执行 5 步：

| 步骤 | 动作 | 目的 |
|------|------|------|
| 1 · 问 | 用户有 brand guidelines 吗？ | 尊重已有资源 |
| 2 · 搜官方品牌页 | `<brand>.com/brand` · `brand.<brand>.com` · `<brand>.com/press` | 抓权威色值 |
| 3 · 下载资产 | SVG 文件 → 官网 HTML 全文 → 产品截图取色 | 三条兜底，前一条失败立刻走下一条 |
| 4 · grep 提取色值 | 从资产里抓所有 `#xxxxxx`，按频率排序，过滤黑白灰 | **绝不从记忆猜品牌色** |
| 5 · 固化 spec | 写 `brand-spec.md` + CSS 变量，所有 HTML 引用 `var(--brand-*)` | 不固化就会忘 |

### 设计方向顾问（Fallback）

当用户需求模糊到无法着手时触发：

- 先对话澄清 + 主动索要参考（名字 / logo / 品牌色 / 喜欢的参考站）
- 取齐内容必需的真图（公共领域 / 免版权，脚本一键抓），再开工
- **三套互补逻辑并行 subagent**，各出一版**真实视觉**：① 秒数轮盘（`date +%S` 取秒，20 选 1，打破模型偷选极简的惯性）② 现实参照（世界级获奖网站 / PPT / iOS 原型迁移）③ 最佳设计师（预算无上限时最适合的工作室哲学）
- **绝不让你在没看到视觉时盲选风格**——三版摆出来，看着选
- 选定后进入主干 Junior Designer 流程
- 底层是 **40 种 HTML 原生风格库**（网页 20 + PPT 20，按大胆 / 中性 / 安静分级，纯 CSS 无需生图）作弹药，不是教条

### Junior Designer 工作流

默认工作模式，贯穿所有任务：

- 开工前 show 问题清单一次性发给用户，等批量答完再动手
- HTML 里先写 assumptions + placeholders + reasoning comments
- 尽早 show 给用户（哪怕只是灰色方块）
- 填充实际内容 → variations → Tweaks 这三步分别再 show 一次
- 交付前用 Playwright 肉眼过一遍浏览器

### 反 AI slop 规则

避免一眼 AI 的视觉最大公约数（紫渐变 / emoji 图标 / 圆角+左 border accent / SVG 画人脸 / Inter 做 display）。用 `text-wrap: pretty` + CSS Grid + 精心选择的 serif display 和 oklch 色彩。

## 仓库结构

```
cc-design/
├── SKILL.md                 # 主文档（给 agent 读）
├── README.md                # 中文 README（本文件）
├── README.en.md             # 英文 README
├── assets/                  # Starter Components
│   ├── animations.jsx       # Stage + Sprite + Easing + interpolate
│   ├── ios_frame.jsx        # iPhone 15 Pro bezel
│   ├── android_frame.jsx
│   ├── macos_window.jsx
│   ├── browser_window.jsx
│   ├── deck_stage.js        # HTML 幻灯片引擎
│   ├── deck_index.html      # 多文件 deck 拼接器
│   ├── design_canvas.jsx    # 并排变体展示
│   ├── showcases/           # 24 个预制样例（8 场景 × 3 风格）
│   └── bgm-*.mp3            # 6 首场景化背景音乐
├── references/              # 按任务深入读的子文档
│   ├── animation-pitfalls.md
│   ├── design-styles.md     # 40 种 HTML 原生风格库（网页 20 + PPT 20）
│   ├── slide-decks.md
│   ├── editable-pptx.md
│   ├── critique-guide.md
│   ├── video-export.md
│   └── ...
├── scripts/                 # 导出工具链
│   ├── render-video.js      # HTML → MP4
│   ├── convert-formats.sh   # MP4 → 60fps + GIF
│   ├── add-music.sh         # MP4 + BGM
│   ├── export_deck_pdf.mjs
│   ├── export_deck_pptx.mjs
│   ├── html2pptx.js
│   └── verify.py
└── demos/                   # 9 个能力演示 (c*/w*)，中英双版 GIF/MP4/HTML + hero v10
```

## Limitations

- **不支持图层级可编辑的 PPTX 到 Figma**。产出 HTML，可截图、录屏、导图，但不能拖进 Keynote 改文字位置。
- **Framer Motion 级别的复杂动画不行**。3D、物理模拟、粒子系统超出 skill 边界。
- **完全空白的品牌从零设计质量会掉到 60–65 分**。凭空画 hi-fi 本来就是 last resort。

## License

MIT。详见 [LICENSE](LICENSE)。

## 致谢

本 skill 基于 [huashu-design](https://github.com/alchaincyf/huashu-design)（MIT 协议）学习改造而来，感谢原作者花叔开源。

原项目的方法论、references、starter components、scripts 与设计哲学是本 skill 的基础。本改造保留原作者版权声明，不引入任何新的个人署名，仅做学习与个人使用。如原作者认为本改造有任何不妥，请联系移除。
