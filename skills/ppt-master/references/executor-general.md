## 文档名称

Executor General 执行说明

Author: Wang Wei Yuan
Time: 2026-03-30

## 适用范围

用于通用展示型、视觉优先型页面执行阶段，强调视觉冲击力、信息可读性和演示友好度。

## 审查要点

- 是否符合 general versatile 风格目标。
- 是否与 `executor-base.md` 的通用约束保持一致。
- 是否避免过度装饰影响信息表达。

## 详细执行规则


# Executor General — Creative Versatile Style

> Common guidelines: executor-base.md. Technical constraints: shared-standards.md.

---

## Role Definition

A creative, versatile-style SVG design executor. Suitable for product introductions, training materials, proposal presentations, marketing campaigns, and other **non-consulting** scenarios. Emphasizes visual impact and information engagement, striking a balance between professionalism and approachability.

---

## General-specific Layout Techniques

### 1. Flexible and Varied Layouts

The General style is not confined to fixed templates; layouts can be freely chosen based on content:

| Layout | Use Case | Layout Details (1280x720) |
|--------|----------|--------------------------|
| Full-image background + text overlay | Covers, emotional pages | `<image>` fills canvas + semi-transparent overlay + centered title |
| Left-right split (image-text mix) | Feature introductions, comparisons | Left x=40,w=580 / Right x=660,w=580 |
| Three-column cards | Feature lists, team introductions | x=40,450,860 each w=380, equal-height cards |
| Top-bottom split | Timelines, process flows | Top area: title+description h=250 / Bottom area: charts+content h=420 |
| Center-radiating | Core concepts, ecosystem diagrams | Center element + 4-6 surrounding nodes, lines pointing to center |
| Waterfall / Z-pattern | Storytelling, case studies | Content blocks alternate left-right, guiding the eye in a Z-pattern |

### 1.1 High-Risk Layout Guardrails

These rules were added to prevent recurring production defects in brand / product decks:

| Layout | Mandatory Guardrail |
|--------|---------------------|
| **Center-radiating** | Keep connector lines outside the central text zone; reserve a bottom annotation lane; if the bottom note is long, wrap to 2 lines and increase strip height; avoid generic oversized center circles — prefer a central rounded card/panel unless the design spec explicitly requires a circle |
| **Left-right chart pages** | Reserve a visible left gutter for Y-axis labels; keep chart title / chart note above the plotting area; move data labels inside bars/points when necessary |
| **Three-column / four-card pages** | Card body text must wrap instead of forcing single-line copy; if copy exceeds 2 lines, increase card height or reduce copy density |
| **Bottom summary strips / pills** | Treat as narrow containers; long text must use `<tspan>` wrapping instead of shrinking into one line |
| **Contact / ending cards** | Keep explicit vertical spacing between title, email, URL, and bottom border; never stack three lines at near-equal baselines |

### 2. Visual Rhythm Control

- **Information density alternation**: Follow a data-heavy page with a "breathing page" (large image / quote / transition) to prevent audience fatigue
- **Visual weight balance**: Dark/large-area elements are "heavy", light/small elements are "light" — balance left-right/top-bottom
- **Repetition and variation**: Maintain layout consistency within a chapter; vary between chapters to maintain freshness

### 3. Decorative Element Usage

| Element | Usage | Notes |
|---------|-------|-------|
| Gradient blocks | Background zones, title backing | Use `<linearGradient>` / `<radialGradient>`, limit to 2-3 colors |
| Rounded rectangle cards | Content containers, feature modules | `rx="12"` with light shadow (simulate with lighter rect) |
| Icon accents | List item prefixes, feature markers | Use `data-icon` placeholders, size 32-48px |
| Numbered circles | Step flows, ranked lists | `<circle>` + centered `<text>`, theme color fill |
| Divider lines | Content separation | `<line>` or `<rect height="2">`, opacity 0.2-0.3 |

---

## Visual Strategy

### Color Usage

- **Bold use of theme color**: Covers and chapter pages can use large areas of theme color background
- **Gradients enhance depth**: Title bars and card backgrounds can use same-hue gradients
- **Contrast creates focus**: Key numbers/words use accent color, creating contrast with surroundings
- **Color-mood matching**: Cool tones for tech feel, warm tones for energy, dark tones for gravitas

### Image Handling Strategy

| Scenario | Strategy | SVG Implementation |
|----------|----------|-------------------|
| Full-screen background | Image fills + dark gradient overlay | `preserveAspectRatio="xMidYMid slice"` + gradient rect |
| Portrait image display | Place left/right, maintain original ratio | Control width, height adapts |
| Multi-image grid | Grid arrangement, uniform sizing | Equal-width equal-height `<image>` matrix |
| Person photo | Circular crop effect | `<circle>` background + square image overlay (post-processing crops) |

### Typography Hierarchy

```
Title layer   → 28-36px, bold, theme color or white
Subtitle layer → 20-24px, medium weight, secondary color
Body layer    → 16-18px, regular, dark gray
Annotation layer → 12-14px, light gray, bottom-aligned
```

---

## Speaker Notes Style

### Narrative Tone

General style speaker notes use **conversational narration** — like talking with the audience, not reading a report. Natural tone with rhythm, using rhetorical devices where appropriate.

### Stage Direction Markers

| Marker | Purpose | Example |
|--------|---------|---------|
| `[Pause]` | Silence after key reveal, letting the audience absorb | "What does this number mean? [Pause] It means 1 in every 3 users..." |
| `[Interactive]` | Ask questions or guide audience participation | "[Interactive] How many of you have used this feature?" |
| `[Transition]` | Bridge from previous page, must be at start of each page's text | "[Transition] Now that we understand the context, let's see how it works." |

### Notes Writing Guidelines

- **Tell stories**: Use "scenario-conflict-resolution" structure for each page's narrative
- **Use metaphors**: Make abstract concepts tangible ("It's like adding a turbocharger to the system")
- **Create suspense**: Pose questions at the right time, answer on the next page
- **Conversational data**: 30% → "nearly one-third", 2.5x → "more than doubled"
- **Key points structure**: `Key points: (1) Core message (2) Supporting evidence (3) Call to action`

### Notes Example

```markdown
# 03_key_advantages

[Transition] Having covered the market landscape, you might be wondering: where is our opportunity?

Our core advantages can be summed up in three words: Fast, Accurate, Efficient.
Fast — deployment time cut from 3 months to 2 weeks; [Pause]
Accurate — recognition accuracy at 97.3%, far exceeding the industry average of 82%;
Efficient — overall costs reduced by nearly one-third.

[Interactive] If you were the decision-maker, which of these three numbers would impress you most?

Key points: (1) Three differentiating advantages (2) Quantitative data support (3) Prompt for reflection
Duration: 2 minutes
```

---

## Self-check Supplement (General-specific)

- [ ] Visual rhythm is reasonable: data-dense pages alternate with breathing pages
- [ ] Decorative elements are moderate: serving content, not overshadowing it
- [ ] Image-text ratio is appropriate: not just text walls, visual highlights present
- [ ] Notes are conversational: reads like speaking, not reading a script
- [ ] Center-radiating pages: lines do not intersect center text or bottom strip text
- [ ] Chart pages: Y-axis labels, chart titles, data labels, and X-axis labels all remain inside safe gutters
- [ ] Narrow strips / pills / cards: long text is wrapped with `<tspan>` rather than forced into one line
