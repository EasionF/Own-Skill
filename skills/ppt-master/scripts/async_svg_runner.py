#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, encoding='utf-8', errors='replace')


def _manifest(generator: Path) -> list[str]:
    result = _run([sys.executable, str(generator), '--manifest'], generator.parent)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or 'manifest failed')
    data = json.loads(result.stdout)
    if not isinstance(data, list):
        raise RuntimeError('manifest must be a json list')
    return [str(item) for item in data]


def _render_one(generator: Path, page_id: str) -> dict[str, str | int]:
    started = time.time()
    result = _run([sys.executable, str(generator), '--page', page_id], generator.parent)
    return {
        'page': page_id,
        'returncode': result.returncode,
        'stdout': result.stdout,
        'stderr': result.stderr,
        'elapsed_ms': int((time.time() - started) * 1000),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Run page-level SVG generation in parallel without changing the ppt-master export pipeline.')
    parser.add_argument('generator')
    parser.add_argument('--workers', type=int, default=4)
    parser.add_argument('--pages', nargs='*')
    args = parser.parse_args()

    generator = Path(args.generator).resolve()
    if not generator.exists():
        print(f'[ERROR] generator not found: {generator}', file=sys.stderr)
        return 2

    pages = args.pages or _manifest(generator)
    if not pages:
        print('[ERROR] no pages returned by manifest', file=sys.stderr)
        return 2

    failures = []
    with ThreadPoolExecutor(max_workers=max(1, args.workers)) as executor:
        futures = {executor.submit(_render_one, generator, page): page for page in pages}
        for future in as_completed(futures):
            result = future.result()
            print(f"[PAGE] {result['page']} returncode={result['returncode']} elapsed_ms={result['elapsed_ms']}")
            if result['returncode'] != 0:
                failures.append(result)

    if failures:
        print('[ERROR] async generation failed for pages:', file=sys.stderr)
        for item in failures:
            print(f"  - {item['page']}", file=sys.stderr)
            if item['stderr']:
                print(item['stderr'], file=sys.stderr)
        return 1

    print(f'[OK] async generation complete: {len(pages)} pages')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
