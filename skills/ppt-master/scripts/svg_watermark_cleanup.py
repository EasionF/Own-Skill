#!/usr/bin/env python3
"""
PPT Master - SVG 水印清理辅助工具

默认清理 SVG 幻灯片里重复出现的示例水印和页脚文字。
它会在 SVG 后处理和 SVG 转 PPTX 之前运行，确保最终输出默认不带仓库水印。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree as ET

WATERMARK_PATTERNS = (
    re.compile(r"github\.com/hugohe3/ppt-master", re.IGNORECASE),
    re.compile(r"^https://github\.com/hugohe3/ppt-master/?$", re.IGNORECASE),
    re.compile(r"MIT License", re.IGNORECASE),
    re.compile(r"Made with ❤️", re.IGNORECASE),
    re.compile(r"^PPT Master -\s+"),
)

FOOTER_Y_THRESHOLD = 640.0
FOOTER_LINE_MIN_WIDTH = 800.0
FOOTER_LINE_MAX_THICKNESS = 2.5


def _strip_ns(tag: str) -> str:
    return tag.rsplit("}", 1)[-1] if "}" in tag else tag


def _float_attr(elem: ET.Element, name: str) -> Optional[float]:
    raw = elem.get(name)
    if raw is None:
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _normalized_text(elem: ET.Element) -> str:
    text = "".join(elem.itertext()).strip()
    return re.sub(r"\s+", " ", text)


def _should_strip_text(elem: ET.Element) -> bool:
    if _strip_ns(elem.tag) != "text":
        return False

    text = _normalized_text(elem)
    if not text:
        return False

    if any(pattern.search(text) for pattern in WATERMARK_PATTERNS):
        return True

    y = _float_attr(elem, "y")
    if y is not None and y >= FOOTER_Y_THRESHOLD:
        if re.fullmatch(r"\d{1,2}\s*/\s*\d{1,2}", text):
            return True

    return False


def _should_strip_line(elem: ET.Element) -> bool:
    if _strip_ns(elem.tag) != "line":
        return False

    x1 = _float_attr(elem, "x1")
    x2 = _float_attr(elem, "x2")
    y1 = _float_attr(elem, "y1")
    y2 = _float_attr(elem, "y2")

    if None in (x1, x2, y1, y2):
        return False

    if abs(y1 - y2) > FOOTER_LINE_MAX_THICKNESS:
        return False

    if max(y1, y2) < FOOTER_Y_THRESHOLD:
        return False

    if (x2 - x1) < FOOTER_LINE_MIN_WIDTH:
        return False

    return True


def cleanup_svg_watermarks(svg_file: Path, verbose: bool = False) -> int:
    """从单个 SVG 中移除默认仓库水印和页脚节点。"""
    try:
        tree = ET.parse(str(svg_file))
        root = tree.getroot()
    except Exception:
        return 0

    removed = 0
    parents = list(root.iter())
    for parent in parents:
        children = list(parent)
        for child in children:
            if _should_strip_text(child) or _should_strip_line(child):
                parent.remove(child)
                removed += 1

    if removed > 0:
        tree.write(str(svg_file), encoding="unicode", xml_declaration=False)
        if verbose:
            print(f"   [OK] {svg_file.name}: removed {removed} watermark node(s)")

    return removed
