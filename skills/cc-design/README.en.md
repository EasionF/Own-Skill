# cc-Design

> *"Type. Hit enter. A finished design lands in your lap."*
> *「打字。回车。一份能交付的设计。」*

A skill for high-fidelity prototypes, slide decks, animations, infographics, and expert design review using HTML. Say one sentence to your agent — Claude Code, Cursor, Codex, Trae all work — and get back a deliverable design.

3 to 30 minutes — you ship a **product launch animation**, a clickable App prototype, an editable PPT deck, a print-grade infographic.

## Install

```
npx skills add EasionF/cc-design
```

Then in any skills-compatible agent:

```
"Make an AI psychology presentation, recommend 3 style directions to pick from"
"Build an AI pomodoro iOS prototype, 4 core screens, really clickable"
"Turn this logic into a 60-second animation, export MP4 and GIF"
"Give this design a 5-dimension expert review"
```

## What it does

| Capability | Deliverable | Typical time |
|------|--------|----------|
| Interactive prototype (App / Web) | Single-file HTML · real iPhone bezel · clickable · Playwright verified | 10–15 min |
| Presentation decks | HTML deck (browser presentation) + editable PPTX (text boxes preserved) | 15–25 min |
| Timeline animation | MP4 (25fps / 60fps interpolation) + GIF (palette-optimized) + BGM | 8–12 min |
| Design variants | 3+ side-by-side comparisons · Tweaks real-time · cross-dimension exploration | 10 min |
| Infographic / visualization | Print-grade typography · exportable PDF/PNG/SVG | 10 min |
| Design direction advisor | **Three parallel logics** (seconds-roulette + real-world award winners + best designer) · 3 real visual versions | 5 min |
| 5-dimension expert review | Radar chart + Keep/Fix/Quick Wins · actionable fix list | 3 min |

## Core mechanics

### Brand asset protocol

When involving real brands (Stripe, Linear, Anthropic, your company, etc.), 5 mandatory steps:

| Step | Action | Purpose |
|------|------|------|
| 1 · Ask | Does the user have brand guidelines? | Respect existing assets |
| 2 · Search official brand page | `<brand>.com/brand` · `brand.<brand>.com` · `<brand>.com/press` | Grab authoritative colors |
| 3 · Download assets | SVG → full official HTML → product screenshots | Three fallbacks, fail-fast to next |
| 4 · grep colors | Extract all `#xxxxxx`, sort by frequency, filter black/white/gray | **Never guess brand colors from memory** |
| 5 · Solidify spec | Write `brand-spec.md` + CSS variables, all HTML uses `var(--brand-*)` | Otherwise it gets lost |

### Design direction advisor (Fallback)

Triggered when the user's request is too vague to start:

- First clarify via conversation + actively ask for references (name / logo / brand colors / liked reference sites)
- Grab all content-essential real images (public domain / royalty-free, one-shot script)
- **Three complementary parallel subagents**, each producing one real visual version: ① seconds roulette (`date +%S`, 20-pick-1, breaks the model's habit of always picking safe minimalism) ② real-world reference (award-winning websites / PPT / iOS prototypes to migrate from) ③ best designer (the studio philosophy that best fits the user's product)
- **Never let the user pick a style without seeing visuals** — three versions laid out, pick by looking
- After selection, enter the main Junior Designer flow
- Backed by a **40-entry HTML-native style library** (20 web + 20 PPT, sorted by bold/neutral/quiet, pure CSS, no image generation needed) as ammunition, not dogma

### Junior Designer workflow

Default mode, running through all tasks:

- Send the question list in one batch before starting, wait for answers before acting
- Write assumptions + placeholders + reasoning comments in HTML first
- Show the user early (even just gray boxes with labels)
- Fill content → variations → Tweaks — show once at each step
- Eyeball the browser via Playwright before delivery

### Anti-AI-slop rules

Avoid the visual lowest-common-denominator of AI training data (purple gradients / emoji icons / rounded cards + left border accent / SVG faces / Inter as display). Use `text-wrap: pretty` + CSS Grid + carefully chosen serif displays and oklch colors.

## Repository structure

```
cc-design/
├── SKILL.md                 # Main doc (read by agent)
├── README.md                # Chinese README (default)
├── README.en.md             # English README (this file)
├── assets/                  # Starter Components
│   ├── animations.jsx       # Stage + Sprite + Easing + interpolate
│   ├── ios_frame.jsx        # iPhone 15 Pro bezel
│   ├── android_frame.jsx
│   ├── macos_window.jsx
│   ├── browser_window.jsx
│   ├── deck_stage.js        # HTML slide engine
│   ├── deck_index.html      # Multi-file deck assembler
│   ├── design_canvas.jsx    # Side-by-side variants
│   ├── showcases/           # 24 preset samples (8 scenes × 3 styles)
│   └── bgm-*.mp3            # 6 scene-specific BGM tracks
├── references/              # Per-task deep-dive sub-documents
│   ├── animation-pitfalls.md
│   ├── design-styles.md     # 40-entry HTML-native style library (20 web + 20 PPT)
│   ├── slide-decks.md
│   ├── editable-pptx.md
│   ├── critique-guide.md
│   ├── video-export.md
│   └── ...
├── scripts/                 # Export toolchain
│   ├── render-video.js      # HTML → MP4
│   ├── convert-formats.sh   # MP4 → 60fps + GIF
│   ├── add-music.sh         # MP4 + BGM
│   ├── export_deck_pdf.mjs
│   ├── export_deck_pptx.mjs
│   ├── html2pptx.js
│   └── verify.py
└── demos/                   # 9 capability demos (c*/w*), bilingual GIF/MP4/HTML + hero v10
```

## Limitations

- **No pixel-level editable PPTX-to-Figma**. Produces HTML — screenshottable, recordable, exportable as images, but not draggable into Keynote to edit text positions.
- **No Framer Motion-level complex animation**. 3D, physics simulation, particle systems are out of scope.
- **A completely blank brand designed from scratch will drop to 60–65 quality**. Designing hi-fi from nothing is a last resort.

## License

MIT. See [LICENSE](LICENSE).

## Acknowledgments

This skill is a study-based modification of [huashu-design](https://github.com/alchaincyf/huashu-design) (MIT-licensed). Many thanks to the original author 花叔 for open-sourcing it.

The original project's methodology, references, starter components, scripts, and design philosophy form the foundation of this skill. This modification retains the original author's copyright notice and introduces no new personal attribution — it is for study and personal use only. If the original author considers any part of this modification inappropriate, please contact for removal.
