# 南京大学品牌模板 - 设计规范

> 适用于南京大学品牌介绍、学术发布、招生宣传、校地合作与全球连接等场景。

---

## I. Template Overview

| Property | Description |
|---|---|
| **Template Name** | `nanjing_university` |
| **Display Name** | 南京大学 |
| **Use Cases** | 品牌介绍、学术发布、招生宣传、校友与人才、国际合作 |
| **Design Tone** | 紫白极简、学术秩序、克制、稳重、可信 |
| **Theme Mode** | Light theme (white background + purple accent) |

---

## II. Canvas Specification

| Property | Value |
|---|---|
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |
| **Page Margins** | Left/Right 60px, Top 55px, Bottom 40px |
| **Safe Area** | x: 60-1220, y: 55-680 |
| **Grid Baseline** | 40px |

---

## III. Color Scheme

### Primary Colors

| Role | Value | Notes |
|---|---|---|
| **Primary Purple** | `#6C3EA0` | Main accent, title bar, key nodes |
| **Deep Purple** | `#3C245C` | Main title, emphasis text |
| **Light Purple** | `#F7F2FB` | Card background, message bar |
| **Soft Purple** | `#A07BC9` | Labels, secondary accents |
| **Background White** | `#FBF8FE` | Main page background |

### Text Colors

| Role | Value | Usage |
|---|---|---|
| **Primary Text** | `#241938` | Main titles, card titles |
| **Secondary Text** | `#6F687E` | Body content, annotations |
| **Muted Text** | `#9A92A7` | Footer, auxiliary info |

### Support Colors

| Role | Value | Usage |
|---|---|---|
| **Academic Green** | `#1FAF7A` | Talent / process / positive node |
| **Warm Gold** | `#B98A52` | Cooperation / external connection |
| **Border Line** | `#DCCFEA` | Card borders, dividers |
| **Soft Border** | `#E9E2F1` | Section lines, separators |

---

## IV. Typography System

### Font Stack

**Font Stack**: `"Source Han Serif SC", "Noto Serif SC", serif` for titles; `"Source Han Sans SC", "Noto Sans SC", sans-serif` for body.

### Font Size Hierarchy

| Level | Usage | Size | Weight |
|---|---|---:|---|
| H1 | Cover main title | 48-56px | Bold |
| H2 | Page title | 28-34px | Bold |
| H3 | Section title | 20-24px | Bold |
| H4 | Card title | 18-22px | Bold |
| P | Body content | 14-18px | Regular |
| Sub | Labels / notes | 12-13px | Regular |

---

## V. Page Structure

### General Layout

| Area | Position / Height | Description |
|---|---|---|
| **Eyebrow** | y=48 | Small uppercase label |
| **Title Area** | y=120, h=70px | Page title and subtitle |
| **Content Area** | y=210-640 | Flexible content zone |
| **Footer** | y=640-680 | Page number / source / project note |

### Decorative Logic

- Use a thin purple top line or left accent strip, not heavy frames.
- Card borders should be light and low-contrast.
- Keep page rhythm calm and avoid dense ornament.

---

## VI. Page Types

### 1. Cover Page

- White background with subtle purple accent blocks
- Left-aligned main title
- Right-side information rail
- Project code / date / institution area

### 2. Table of Contents / Chapter List

- Clean vertical chapter list or two-column list
- Number + title + short description
- Low decoration, strong alignment

### 3. Chapter Page

- Full purple background or deep purple panel
- Centered chapter number, title, and one-line description
- Used for major section transitions

### 4. Content Page

- White background
- Top eyebrow + page title + subtitle
- One key message bar
- Flexible card / matrix / timeline / split layout

### 5. Ending Page

- Closing statement centered
- Three supporting pillars or contact area
- Clear ending and stable tone

---

## VII. Layout Modes (Recommended)

| Mode | Use Cases |
|---|---|
| **Left-right split** | Brand judgments, evidence vs. explanation |
| **Three-card row** | Core judgments, touchpoints, features |
| **Two-by-two matrix** | Academic structure, multi-dimension views |
| **Timeline / node chain** | Heritage, process, touchpoint flow |
| **Centered closing** | Ending and summary page |

---

## VIII. Spacing Specification

| Element | Value |
|---|---|
| Page margins | 60px |
| Title-to-content gap | 24-36px |
| Card gap | 20-24px |
| Internal padding | 18-28px |
| Line height | 1.35-1.55 |
| Node-to-label gap | 14-20px |

---

## IX. SVG Technical Constraints

### Mandatory Rules

1. `viewBox` must be `0 0 1280 720`
2. Use `<rect>` for backgrounds and container boxes
3. Use `<text>` / `<tspan>` for text, never `<foreignObject>`
4. Use HEX + opacity attributes, not `rgba()`
5. Do not use `<style>`, `class`, `clipPath`, `mask`, `textPath`, animation, or script
6. Prefer inline styles and explicit coordinates
7. Any text box must stay fully inside its container
8. Multiple text blocks in the same container must not visually overlap

---

## X. Placeholder Specification

| Placeholder | Purpose |
|---|---|
| `{{TITLE}}` | Main title |
| `{{SUBTITLE}}` | Subtitle |
| `{{AUTHOR}}` | Presenter / institution |
| `{{DATE}}` | Date |
| `{{PROJECT_CODE}}` | Project code |
| `{{PAGE_TITLE}}` | Page title |
| `{{SECTION_NUM}}` | Chapter / section number |
| `{{SECTION_NAME}}` | Section name |
| `{{KEY_MESSAGE}}` | Key message |
| `{{CONTENT_AREA}}` | Content area placeholder |
| `{{PAGE_NUM}}` | Page number |
| `{{THANK_YOU}}` | Closing statement |
| `{{TAGLINE}}` | Tagline |
| `{{CONTACT_NAME}}` | Contact name |
| `{{CONTACT_TITLE}}` | Contact title |
| `{{CONTACT_EMAIL}}` | Contact email |
| `{{CONTACT_PHONE}}` | Contact phone |
| `{{COPYRIGHT}}` | Copyright |

---

## XI. Usage Guide

1. Copy this template into a project's `templates/` directory, or select it from the template library by name.
2. Use the template name `nanjing_university` when matching a university-brand scenario.
3. Keep all content short, disciplined, and hierarchy-first.
4. Run text preflight before final export.
