## 文档名称

Executor 通用执行说明

Author: Wang Wei Yuan
Time: 2026-03-30

## 适用范围

用于 `ppt-master` 的 Executor 通用阶段，约束模板遵循、设计参数确认、SVG 生成和布局安全边界。

## 功能数据流转

Strategist 输出设计规格  
-> Executor 读取通用规则与风格规则  
-> 生成 SVG 与讲稿备注  
-> 进入后处理与导出阶段

## 审查要点

- 是否在生成前确认设计参数。
- 是否遵循模板映射和布局安全约束。
- 是否在进入导出前完成文本布局检查。

## 详细执行规则


# Executor Common Guidelines

> Style-specific content is in the corresponding `executor-{style}.md`. Technical constraints are in shared-standards.md.

---

## 1. Template Adherence Rules

If template files exist in the project's `templates/` directory, the template structure must be followed:

| Page Type | Corresponding Template | Adherence Rules |
|-----------|----------------------|-----------------|
| Cover | `01_cover.svg` | Inherit background, decorative elements, layout structure; replace placeholder content |
| Chapter | `02_chapter.svg` | Inherit numbering style, title position, decorative elements |
| Content | `03_content.svg` | Inherit header/footer styles; **content area may be freely laid out** |
| Ending | `04_ending.svg` | Inherit background, thank-you message position, contact info layout |
| TOC | `02_toc.svg` | **Optional**: Inherit TOC title, list styles |

### Page-Template Mapping Declaration (Required Output)

Before generating each page, you must explicitly output which template (or "free design") is used:

```
📝 **Template mapping**: `templates/01_cover.svg` (or "None (free design)")
🎯 **Adherence rules / layout strategy**: [specific description]
```

- **Content pages**: Templates only define header and footer; the content area is freely laid out by the Executor
- **No template**: Generate entirely per the Design Specification & Content Outline

---

## 2. Design Parameter Confirmation (Mandatory Step)

> Before generating the first SVG page, you **must review the key design parameters from the Design Specification & Content Outline** to ensure all subsequent generation strictly follows the spec.

Must output confirmation including: canvas dimensions, body font size, color scheme (primary/secondary/accent HEX values), font plan.

**Why is this step mandatory?** Prevents the "spec says one thing, execution does another" disconnect.

---

## 3. Execution Guidelines

- **Proximity principle**: Place related elements close together to form visual groups; increase spacing between unrelated groups to reinforce logical structure
- **Absolute spec adherence**: Strictly follow the color, layout, canvas format, and typography parameters in the spec
- **Follow template structure**: If templates exist, inherit the template's visual framework
- **Phased batch generation** (recommended):
  1. **Visual Construction Phase**: Generate all SVG pages continuously, ensuring high consistency in design style and layout coordinates (Visual Consistency)
  2. **Logic Construction Phase**: After all SVGs are finalized, batch-generate speaker notes to ensure narrative coherence (Narrative Continuity)
- **Technical specifications**: See [shared-standards.md](shared-standards.md) for SVG technical constraints and PPT compatibility rules

### Layout Safety Guardrails (Mandatory)

The following rules are hard constraints, not style suggestions:

- **No visible overlap allowed**: text may not overlap icons, lines, axes, bars, circles, card borders, or other text blocks
- **No container overflow allowed**: if text does not fit, widen the container, reduce density, or insert manual `<tspan>` line breaks in `svg_output/`
- **CJK wrapping must be semantic**: Chinese copy may be shortened or manually re-broken, but must not be split into visually broken fragments (`Ap p`, `体 验`, `品 牌`) just to satisfy width limits
- **Chart pages must reserve gutters**:
  - left gutter between chart card border and Y-axis labels: **>= 24px**
  - right gutter between rightmost plotted element / X-axis label and chart card border: **>= 24px**
  - top gutter between chart title/annotation block and highest data label: **>= 32px**
  - bottom gutter between X-axis labels and card border: **>= 20px**
  - the plotted region must be fully enclosed by the axes: the X-axis end must sit to the right of the last bar / point / label, and the Y-axis top must start below the chart annotation block rather than cutting through it
  - when adapting `bar_chart.svg`, keep the template's logic: title block first, then plot box, then axes/grid, then bars/labels; do not let bars or labels extend outside the axis span
- **Relation / center-radiating pages**:
  - connector lines must not pass through central text or bottom annotations
  - bottom summary strips must be treated as narrow containers; when text exceeds one line, wrap to 2 lines and increase strip height
- **Card text wrapping**:
  - card padding must satisfy the same minimum safe padding used by `text_layout_audit.py`; do not place body text at visual positions that violate the audit padding threshold
  - small/medium cards may not keep long body copy on one line
  - for 16-18px body text, use `<tspan>` once content exceeds a safe single-line length for the available width
- **Ending / contact cards**:
  - vertical gap between stacked text lines must be **>= 12px**
  - bottom text must keep **>= 12px** distance from the card bottom edge
- **Cover / ending info panels**:
  - source lists, metadata panels, and contact/info blocks must be treated as audited containers even when they use fill-only rectangles without visible strokes
  - panel height must be derived from actual line count and line spacing before placement; do not hand-fill a fixed rectangle height first
  - the final text line inside these panels must keep **>= 16px** distance from the panel bottom edge
  - title-to-first-line gap inside these panels must keep **>= 14px**
- **No internal meta text on delivery pages**:
  - page SVGs must not show project names, test names, template filenames, script filenames, adaptation notes, generation pipeline notes, internal email placeholders, or local dates unless the Design Spec explicitly requires them
  - references such as `bar_chart.svg`, `matrix_2x2.svg`, `generated by ppt-master`, `Brand Test Deck`, `execution pipeline`, and test project identifiers belong only in `design_spec.md`, notes, or internal logs, never on exported pages
- **Matrix / axis pages**:
  - quadrant labels, axis labels, and title annotations must be treated as first-class layout elements, not decorative afterthoughts
  - by default, avoid rotated axis-title text in generated pages; prefer horizontal in-content labels unless the template explicitly requires rotation and the label has been geometry-validated
  - if an axis title or quadrant title competes with the plot area, reduce plot density or move the title block before shrinking text
  - bubble or node labels inside matrix points must use the node center as the text anchor: `text-anchor="middle"` and vertical centering equivalent to the node center
  - matrix nodes must not overlap quadrant titles, axis lines, or page annotations; keep every node outside title/axis exclusion zones before export
  - for matrix pages, determine bubble radius from measured text width/height plus symmetric padding before selecting the node center; do not place a fixed-size bubble first and force text into it
  - choose node centers only from each quadrant's remaining placement zone after subtracting title blocks, axis bands, and outer safety margins; legality alone is insufficient if the visual balance is poor
- **Performance discipline**:
  - do not iterate through repeated export-fix-export loops on finished PPTX files
  - fix generators, page prototypes, and shared helpers first; then regenerate, re-audit, and export once
- **Page numbers are optional, not default**:
  - do not show `X / N` style footer page numbers on delivery pages unless the Design Spec explicitly requests visible pagination
  - test decks and brand presentations should prefer clean footers over diagnostic pagination

### Validation Gate Before Export

Before any post-processing, the Executor MUST run:

```bash
python3 scripts/text_layout_audit.py <project_path>
```

If any issue is reported, export is blocked until `svg_output/` is fixed and the audit passes cleanly.

### SVG File Naming Convention

File naming format: `<number>_<page_name>.svg`

- **Chinese content** → Chinese naming: `01_封面.svg`, `02_目录.svg`, `03_核心优势.svg`
- **English content** → English naming: `01_cover.svg`, `02_agenda.svg`, `03_key_benefits.svg`
- **Number rules**: Two-digit numbers, starting from 01
- **Page name**: Concise and descriptive, matching the page title in the Design Specification & Content Outline

---

## 4. Icon Usage

Four approaches: **A: Emoji** (`<text>🚀</text>`) | **B: AI-generated** (SVG basic shapes) | **C: Built-in library** (`templates/icons/` 640+ icons, recommended) | **D: Custom** (user-specified)

**Built-in icons — Placeholder method (recommended)**:

```xml
<use data-icon="chart-bar" x="100" y="200" width="48" height="48" fill="#005587"/>
```

> No need to manually run `embed_icons.py`; `finalize_svg.py` post-processing tool will auto-embed icons.

**Common icons**: `chart-bar` `arrow-trend-up` `users` `cog` `circle-checkmark` `target` `clock` `file` `dollar` `lightbulb`

> ⚠️ **Icon validation rule**: If the Design Specification includes an icon inventory list, Executor may **only** use icons from that approved list. Using icon names not in the index is FORBIDDEN — verify against `templates/icons/icons_index.json` if uncertain.

Full index: `templates/icons/README.md`

---

## 5. Chart Reference

When the Design Spec includes a **VII. Chart Reference List**, read the referenced SVG templates from `templates/charts/` to understand common chart patterns.

**Adaptation rules**:
- **Must preserve**: Chart type (bar/line/pie etc.) as specified in the Design Spec
- **Must adapt**: Data values, labels, colors (match the project's color scheme), and dimensions to fit the page layout
- **May adjust**: Axis ranges, grid lines, legend position, spacing — as long as the chart remains accurate and readable
- **Must NOT**: Change chart type without Design Spec justification, or remove data points specified in the outline
- **Must reserve readable gutters**: axis labels, data labels, legends, and chart titles must stay inside the chart card and keep the minimum safe spacing defined above
- **Must wrap surrounding explanatory text**: if a chart page also contains interpretation cards, long copy must be wrapped with `<tspan>` rather than left as one-line text

> Chart templates: `templates/charts/` (33 types). Index: `templates/charts/charts_index.json`

---

## 6. Image Handling

Handle images based on their status in the Design Specification's "Image Resource List":

| Status | Source | Handling |
|--------|--------|----------|
| **Existing** | User-provided | Reference images directly from `../images/` directory |
| **AI-generated** | Generated by Image_Generator | Images already in `../images/`, reference directly |
| **Placeholder** | Not yet prepared | Use dashed border placeholder |

**Reference**: `<image href="../images/xxx.png" ... preserveAspectRatio="xMidYMid slice"/>`

**Placeholder**: Dashed border `<rect stroke-dasharray="8,4" .../>` + description text

---

## 7. Font Usage

Apply corresponding fonts for different text roles based on the font plan in the Design Specification & Content Outline:

| Role | Chinese Recommended | English Recommended |
|------|--------------------|--------------------|
| Title font | Microsoft YaHei / KaiTi / SimHei | Arial / Georgia |
| Body font | Microsoft YaHei / SimSun | Calibri / Times |
| Emphasis font | SimHei | Arial Black / Consolas |
| Annotation font | Microsoft YaHei / SimSun | Arial / Times |

---

## 8. Speaker Notes Generation Framework

### Task 1. Generate Complete Speaker Notes Document

After **all SVG pages are generated and finalized**, enter the "Logic Construction Phase" and generate the complete speaker notes document in `notes/total.md`.

**Why not generate page-by-page?** Batch-writing notes allows planning transitions like a script, ensuring coherent presentation logic.

**Format**: Each page starts with `# <number>_<page_title>`, separated by `---` between pages. Each page includes: script text (2-5 sentences), `Key points: ① ② ③`, `Duration: X minutes`. Except for the first page, each page's text starts with a `[Transition]` phrase.

**Basic stage direction markers** (common to all styles):

| Marker | Purpose |
|--------|---------|
| `[Pause]` | Whitespace after key content, letting the audience absorb |
| `[Transition]` | Standalone paragraph at the start of each page's text, bridging from the previous page |

> Each style may extend with additional markers (`[Interactive]`/`[Data]`/`[Scan Room]`/`[Benchmark]` etc.), see `executor-{style}.md`.

**Requirements**:

- Notes should be conversational and flow naturally
- Highlight each page's core information and presentation key points
- Users can manually edit and override in the `notes/` directory

### Task 2. Split Into Per-Page Note Files

Automatically split `notes/total.md` into individual speaker note files in the `notes/` directory.

**File naming convention**:

- **Recommended**: Match SVG names (e.g., `01_cover.svg` → `notes/01_cover.md`)
- **Compatible**: Also supports `slide01.md` format (backward compatibility)

---

## 9. Next Steps After Completion

> **Auto-continuation**: After Visual Construction Phase (all SVG pages) and Logic Construction Phase (all notes) are complete, the Executor proceeds directly to the post-processing pipeline.

**Post-processing & Export** (see [shared-standards.md](shared-standards.md)):

```bash
# 0. Hard gate: text/layout preflight must pass first
python3 scripts/text_layout_audit.py <project_path>

# 1. Split speaker notes
python3 scripts/total_md_split.py <project_path>

# 2. SVG post-processing (auto-embed icons, images, etc.)
python3 scripts/finalize_svg.py <project_path>

# 3. Export PPTX
python3 scripts/svg_to_pptx.py <project_path> -s final
# Default: generates native shapes (.pptx) + SVG reference (_svg.pptx)
```
