#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path


def build_markdown(data: dict) -> str:
    lines = []
    lines.append(f"# {data.get('topic') or data.get('project_name') or 'PPT Outline'}")
    if data.get('brief'):
        lines.append('')
        lines.append(f"> Brief: {data['brief']}")
    meta = []
    for label, key in (("Audience", "audience"), ("Scenario", "scenario"), ("Page Count", "page_count")):
        value = data.get(key)
        if value:
            meta.append(f"- **{label}**: {value}")
    if meta:
        lines.append('')
        lines.extend(meta)
    for page in data.get('pages', []):
        lines.append('')
        lines.append(f"## Slide {int(page.get('page_no', 0) or 0):02d}: {page.get('title', '')}")
        if page.get('subtitle'):
            lines.append(f"- **Subtitle**: {page['subtitle']}")
        if page.get('intent'):
            lines.append(f"- **Intent**: {page['intent']}")
        if page.get('core'):
            lines.append(f"- **Core Message**: {page['core']}")
        if page.get('focus'):
            lines.append(f"- **Focus**: {page['focus']}")
        evidence = [str(item).strip() for item in page.get('evidence', []) if str(item).strip()]
        if evidence:
            lines.append('- **Evidence Points**:')
            for item in evidence:
                lines.append(f"  - {item}")
    lines.append('')
    return '\n'.join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description='Convert outline.json to markdown source for ppt-master.')
    parser.add_argument('outline')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()

    outline_path = Path(args.outline).resolve()
    data = json.loads(outline_path.read_text(encoding='utf-8'))
    output = Path(args.output).resolve() if args.output else outline_path.with_suffix('.md')
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_markdown(data), encoding='utf-8')
    print(output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
