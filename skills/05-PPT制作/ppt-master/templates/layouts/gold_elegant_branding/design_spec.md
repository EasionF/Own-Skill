# gold_elegant_branding - Gold Elegant Branding Design Specification

> Suitable for luxury branding kits, fashion lookbooks, editorial profiles, and premium creative proposals.

---

## I. Template Overview

| Property | Description |
| --- | --- |
| **Template Name** | gold_elegant_branding |
| **Use Cases** | Branding kits, fashion decks, premium lookbooks, editorial identity systems |
| **Design Tone** | Elegant, editorial, luxurious, minimal |
| **Theme Mode** | Warm gold cover + white editorial inner pages |

---

## II. Canvas Specification

| Property | Value |
| --- | --- |
| **Format** | Standard 16:9 |
| **Dimensions** | 1280 × 720 px |
| **viewBox** | `0 0 1280 720` |
| **Safe Margins** | 60px left/right, 50px top/bottom |
| **Content Area** | x: 80-1200, y: 110-650 |

---

## III. Color Scheme

| Role | Value | Usage |
| --- | --- | --- |
| **Mustard Gold** | `#D9A92E` | Cover background, numbering, key accents |
| **Warm Beige** | `#E8D7BD` | Image panels, subtle backgrounds |
| **Ink Black** | `#1F1A17` | Headlines, decorative rules |
| **Soft White** | `#FBFAF8` | Content-page background |
| **Warm Gray** | `#8E8578` | Secondary editorial notes |

---

## IV. Typography System

- **Primary Serif**: `Georgia, Times New Roman, serif`
- **Secondary Sans**: `Arial, Microsoft YaHei, sans-serif`
- Cover H1: 84-112px italic serif
- Content H2: 34-48px serif
- Body: 18-20px sans/serif mix
- Caption: 14-16px

---

## V. Page Structure

- Cover uses a centered arched image window and oversized editorial title.
- TOC and chapter pages combine serif hierarchy with fine rules and image blocks.
- Content pages keep a clean left title system, optional right image slot, and flexible central content area.
- Ending page echoes the cover with a warm gold background and centered serif closing message.

---

## VI. Page Types

1. `01_cover.svg` — Warm gold editorial cover with image arch and oversized title.
2. `02_toc.svg` — Large serif TOC with numeric index and bottom image panel.
3. `02_chapter.svg` — Editorial chapter divider with chapter number and image rail.
4. `03_content.svg` — White content page with logo slot, left-aligned title, divider line, optional image block, flexible content area.
5. `04_ending.svg` — Minimal closing page with thank-you message and contact line.

---

## VII. Layout Modes (Recommended)

- Editorial split image/text
- Statement + image
- Three-column brand principle cards
- Quote page with side note
- Minimal comparison board

---

## VIII. Spacing Specification

- Use generous whitespace; avoid dense dashboards.
- Keep at least 32px vertical spacing between title and subtitle blocks.
- Fine rules should be 2-4px; accents should remain restrained.

---

## IX. SVG Technical Constraints

Follow the global `ppt-master` SVG compatibility rules. Use only inline styles and standard shapes.

---

## X. Placeholder Specification

Use standard placeholders: `{{TITLE}}` `{{SUBTITLE}}` `{{DATE}}` `{{AUTHOR}}` `{{PAGE_TITLE}}` `{{CONTENT_AREA}}` `{{CHAPTER_NUM}}` `{{CHAPTER_TITLE}}` `{{PAGE_NUM}}` `{{CLOSING_MESSAGE}}`.

---

## XI. Usage Guide (Recommended)

Best for image-led brand storytelling, luxury service decks, and premium launch materials.
