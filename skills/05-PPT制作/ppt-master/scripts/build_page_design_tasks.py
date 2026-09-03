from __future__ import annotations

import json
from pathlib import Path


PAGE_TYPE_RULES = {
    "封面": ("cover", "hero"),
    "结尾": ("ending", "closing"),
    "团队定位": ("principles", "three-column-cards"),
    "战略判断": ("framework", "two-by-two-modules"),
    "能力架构": ("architecture", "layered-system"),
    "产品亮点": ("workflow", "stage-flow"),
    "能力拆解": ("capabilities", "two-by-two-cards"),
    "场景表达": ("use-cases", "scenario-cards"),
}


def build_page_tasks(outline: dict, design_spec_text: str) -> list[dict]:
    tasks = []
    design_style = ''
    for line in design_spec_text.splitlines():
        if line.strip().startswith('| Design Style |'):
            parts = [part.strip() for part in line.split('|') if part.strip()]
            if len(parts) >= 2:
                design_style = parts[1]
                break

    for page in outline.get('pages', []):
        intent = page.get('intent', '')
        page_type, layout_intent = PAGE_TYPE_RULES.get(intent, ('content', 'single-panel'))
        tasks.append({
            'page_no': page['page_no'],
            'title': page.get('title', ''),
            'intent': intent,
            'purpose': page.get('core', ''),
            'page_type': page_type,
            'layout_intent': layout_intent,
            'density': 'medium' if len(page.get('evidence', [])) <= 4 else 'high',
            'visual_priority': 'headline-first' if page_type in {'principles', 'capabilities', 'workflow'} else 'framework-first',
            'content_mode': 'statement-plus-supports',
            'charts_required': page_type in {'workflow'} and 'chart' in page.get('core', '').lower(),
            'images_required': False,
            'icons_mode': 'light' if page_type in {'principles', 'capabilities'} else 'none',
            'design_style': design_style,
            'notes': page.get('focus', '') or ''
        })
    return tasks


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('project_dir')
    args = parser.parse_args()

    project = Path(args.project_dir)
    outline = json.loads((project / 'outline.json').read_text(encoding='utf-8-sig'))
    design_spec = (project / 'design_spec.md').read_text(encoding='utf-8-sig')
    tasks = build_page_tasks(outline, design_spec)
    out = project / 'page_design_tasks.json'
    out.write_text(json.dumps(tasks, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)
