from __future__ import annotations

import json
from pathlib import Path


DEFAULT_COMPONENTS = {
    'cover': [],
    'principles': ['editorial_stat_badge'],
    'framework': ['minimal_divider_callout'],
    'architecture': ['research_data_panel'],
    'workflow': ['tech_signal_cards'],
    'capabilities': ['editorial_stat_badge', 'tech_signal_cards'],
    'use-cases': ['journey_stage_cards'],
    'ending': []
}

DEFAULT_CHARTS = {
    'cover': None,
    'principles': None,
    'framework': None,
    'architecture': None,
    'workflow': 'process_flow',
    'capabilities': None,
    'use-cases': None,
    'ending': None,
}

DEFAULT_LAYOUT_PAGE = {
    'cover': '01_cover.svg',
    'ending': '04_ending.svg'
}


def build_bindings(tasks: list[dict], template_key: str = 'anthropic') -> list[dict]:
    bindings = []
    for task in tasks:
        page_type = task['page_type']
        bindings.append({
            'page_no': task['page_no'],
            'template_key': template_key,
            'template_page': DEFAULT_LAYOUT_PAGE.get(page_type, '03_content.svg'),
            'layout_mode': task['layout_intent'],
            'components': [
                {'slot': 'primary', 'key': key, 'variant': 'default'}
                for key in DEFAULT_COMPONENTS.get(page_type, [])
            ],
            'chart': DEFAULT_CHARTS.get(page_type),
            'icons': task['icons_mode'],
            'background_assets': [],
            'constraints': {
                'body_width_px': 268 if page_type == 'principles' else 500,
                'max_body_lines': 3,
            }
        })
    return bindings


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('project_dir')
    parser.add_argument('--template', default='anthropic')
    args = parser.parse_args()

    project = Path(args.project_dir)
    tasks = json.loads((project / 'page_design_tasks.json').read_text(encoding='utf-8-sig'))
    bindings = build_bindings(tasks, template_key=args.template)
    out = project / 'resource_bindings.json'
    out.write_text(json.dumps(bindings, ensure_ascii=False, indent=2), encoding='utf-8')
    print(out)
