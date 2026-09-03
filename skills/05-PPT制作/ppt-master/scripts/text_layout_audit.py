#!/usr/bin/env python3
"""
PPT Master - SVG 文本版式预检工具

用途：
    在进入 finalize_svg / svg_to_pptx 之前，先扫描 svg_output/ 里的 SVG，
    估算每个 <text> 的实际占位，并和它所在的容器矩形做碰撞判断。

设计目标：
    1. 发现"文本太长，已经超出卡片/容器"的问题。
    2. 在导出前直接把问题页、问题文本、问题容器报出来。
    3. 尽量把"修成品"前移到"修源文件"。

说明：
    这是一个启发式检查，不是像浏览器一样 100% 精确渲染。
    但对当前这种"固定 SVG 模板 + 文本填充"的工作流足够实用。
"""

from __future__ import annotations

import argparse
import re
import sys
from functools import lru_cache
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple
from xml.etree import ElementTree as ET

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover - fallback path for minimal environments
    Image = None  # type: ignore[assignment]
    ImageDraw = None  # type: ignore[assignment]
    ImageFont = None  # type: ignore[assignment]


SVG_NS = "http://www.w3.org/2000/svg"
MIN_CONTAINER_PADDING_RATIO = 0.10
MIN_CONTAINER_PADDING_PX = 16.0
MIN_TEXT_GAP = 10.0
MIN_LINE_GAP = 6.0

FONT_FILE_CANDIDATES = {
    "Segoe UI": [r"C:\Windows\Fonts\segoeui.ttf"],
    "Segoe UI Bold": [r"C:\Windows\Fonts\segoeuib.ttf"],
    "Arial": [r"C:\Windows\Fonts\arial.ttf"],
    "Arial Bold": [r"C:\Windows\Fonts\arialbd.ttf"],
    "Microsoft YaHei": [r"C:\Windows\Fonts\msyh.ttc"],
    "Microsoft YaHei Bold": [r"C:\Windows\Fonts\msyhbd.ttc"],
    "Microsoft JhengHei": [r"C:\Windows\Fonts\msjh.ttc"],
    "Microsoft JhengHei Bold": [r"C:\Windows\Fonts\msjhbd.ttc"],
    "SimSun": [r"C:\Windows\Fonts\simsun.ttc"],
    "SimSun Bold": [r"C:\Windows\Fonts\simsun.ttc"],
    "Aptos": [r"C:\Windows\Fonts\segoeui.ttf"],
    "Aptos Bold": [r"C:\Windows\Fonts\segoeuib.ttf"],
}

FONT_FAMILY_ALIAS = {
    "Helvetica Neue": "Arial",
    "Helvetica": "Arial",
    "Aptos": "Segoe UI",
    "Calibri": "Segoe UI",
    "Candara": "Segoe UI",
    "Arial": "Arial",
    "Segoe UI": "Segoe UI",
    "Microsoft YaHei": "Microsoft YaHei",
    "Microsoft JhengHei": "Microsoft JhengHei",
    "SimSun": "SimSun",
}


# Windows 终端默认代码页容易把中文/项目符号打崩，先统一切到 UTF-8。
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def _f(value: Optional[str], default: float = 0.0) -> float:
    """
    把字符串属性转成浮点数，失败时回退默认值。
    
    参数:
        value: 字符串值
        default: 默认浮点值
        
    返回:
        转换后的浮点数
    """
    if value is None:
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _normalize_text(text: str) -> str:
    """
    把文本里的多余空白合并掉。
    
    参数:
        text: 原始文本
        
    返回:
        标准化后的文本
    """
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def estimate_text_width(text: str, font_size: float, font_weight: str = "400") -> float:
    """
    按字符类型估算文本宽度，和 svg_to_shapes.py 的口径保持一致。
    
    参数:
        text: 要估算的文本
        font_size: 字体大小
        font_weight: 字体粗细
        
    返回:
        估算的文本宽度
    """
    width = 0.0
    for ch in text:
        if "\u4e00" <= ch <= "\u9fff":
            width += font_size
        elif ch == " ":
            width += font_size * 0.3
        elif ch in "mMwWOQ":
            width += font_size * 0.75
        elif ch in "iIlj1!|":
            width += font_size * 0.3
        else:
            width += font_size * 0.55
    if font_weight in ("bold", "600", "700", "800", "900"):
        width *= 1.05
    return width


def _font_key(font_family: str, font_weight: str) -> str:
    """Resolve a SVG font-family to a local Windows font key."""
    family = (font_family or "").split(",")[0].strip().strip("'\"")
    family = FONT_FAMILY_ALIAS.get(family, family)
    bold = font_weight in ("bold", "600", "700", "800", "900")
    if bold:
        bold_key = f"{family} Bold"
        if bold_key in FONT_FILE_CANDIDATES:
            return bold_key
    return family if family in FONT_FILE_CANDIDATES else "Segoe UI Bold" if bold else "Segoe UI"


@lru_cache(maxsize=128)
def _load_font(font_key: str, font_size: int):
    """Load a local font for bbox measurement."""
    if ImageFont is None:
        return None
    for font_path in FONT_FILE_CANDIDATES.get(font_key, []):
        path = Path(font_path)
        if path.exists():
            try:
                return ImageFont.truetype(str(path), max(int(font_size), 1))
            except OSError:
                continue
    fallback_path = Path(r"C:\Windows\Fonts\segoeui.ttf")
    try:
        return ImageFont.truetype(str(fallback_path), max(int(font_size), 1))
    except OSError:
        return None


def _measure_line_bbox(text: str, font_family: str, font_size: float, font_weight: str, anchor: str) -> Optional[Tuple[float, float, float, float]]:
    """Measure a single text line using actual font metrics when available."""
    if ImageDraw is None or Image is None:
        return None

    font_key = _font_key(font_family, font_weight)
    font = _load_font(font_key, round(font_size))
    if font is None:
        return None

    canvas = Image.new("RGB", (4, 4), "white")
    draw = ImageDraw.Draw(canvas)
    anchor_map = {"start": "ls", "middle": "ms", "end": "rs"}
    pil_anchor = anchor_map.get(anchor, "ls")
    try:
        left, top, right, bottom = draw.textbbox((0, 0), text, font=font, anchor=pil_anchor)
        return float(left), float(top), float(right), float(bottom)
    except Exception:
        # Fallback to font metrics if textbbox is unavailable for some reason.
        bbox = font.getbbox(text)
        return float(bbox[0]), float(bbox[1]), float(bbox[2]), float(bbox[3])


@dataclass
class RectBox:
    """页面里的候选容器矩形。"""

    x: float
    y: float
    w: float
    h: float
    stroke: str = ""
    fill: str = ""
    opacity: float = 1.0

    @property
    def right(self) -> float:
        """矩形右边界的 X 坐标"""
        return self.x + self.w

    @property
    def bottom(self) -> float:
        """矩形底边界的 Y 坐标"""
        return self.y + self.h

    def contains(self, left: float, top: float, right: float, bottom: float, padding: float = 0.0) -> bool:
        """
        判断一个文本包围盒是否完全落在容器内部。
        
        参数:
            left: 文本包围盒左边界的 X 坐标
            top: 文本包围盒顶边界的 Y 坐标
            right: 文本包围盒右边界的 X 坐标
            bottom: 文本包围盒底边界的 Y 坐标
            padding: 内边距
            
        返回:
            如果文本包围盒完全在容器内则返回 True，否则返回 False
        """
        return (
            left >= self.x + padding
            and top >= self.y + padding
            and right <= self.right - padding
            and bottom <= self.bottom - padding
        )


@dataclass
class TextIssue:
    """单个文本问题。"""

    file: Path
    text: str
    x: float
    y: float
    estimated_w: float
    estimated_h: float
    container: Optional[RectBox]
    reason: str


@dataclass
class TextBox:
    """用于做文本块之间的碰撞检测。"""

    file: Path
    text: str
    group: str
    left: float
    top: float
    right: float
    bottom: float
    container: Optional[RectBox]


@dataclass
class LineBox:
    """用于做文本与线条的碰撞检测。"""

    file: Path
    left: float
    top: float
    right: float
    bottom: float
    stroke_width: float


def _parse_svg(svg_path: Path) -> Tuple[ET.Element, float, float]:
    """
    解析 SVG 文件
    
    参数:
        svg_path: SVG 文件路径
        
    返回:
        (根元素, 宽度, 高度)
    """
    tree = ET.parse(svg_path)
    root = tree.getroot()
    width = _f(root.get("width"), 1280.0)
    height = _f(root.get("height"), 720.0)
    return root, width, height


def _parse_rect(elem: ET.Element) -> Optional[RectBox]:
    """
    把 <rect> 解析成候选容器。
    
    参数:
        elem: SVG 矩形元素
        
    返回:
        解析后的矩形容器，如果无效则返回 None
    """
    x = _f(elem.get("x"))
    y = _f(elem.get("y"))
    w = _f(elem.get("width"))
    h = _f(elem.get("height"))
    if w <= 0 or h <= 0:
        return None
    # 过滤掉几乎铺满整个页面的背景块，避免误判成文本容器。
    if w >= 1200 and h >= 650 and x <= 10 and y <= 10:
        return None
    return RectBox(
        x=x,
        y=y,
        w=w,
        h=h,
        stroke=elem.get("stroke", ""),
        fill=elem.get("fill", ""),
        opacity=_f(elem.get("opacity"), 1.0),
    )


def _is_visible_container_rect(rect: RectBox) -> bool:
    """
    判断矩形是否应被视为文本容器。

    除了带描边的卡片，也要识别封面/结尾里那种
    “只有填充、没有描边”的信息面板，否则这类面板会绕过审计。
    """
    if rect.stroke and rect.stroke not in ("none", "transparent"):
        return True
    if rect.fill and rect.fill not in ("none", "transparent") and rect.opacity > 0:
        return True
    return False


def _parse_line(elem: ET.Element) -> Optional[LineBox]:
    """
    把 <line> 解析成候选碰撞线段。
    """
    x1 = _f(elem.get("x1"))
    y1 = _f(elem.get("y1"))
    x2 = _f(elem.get("x2"))
    y2 = _f(elem.get("y2"))
    sw = max(_f(elem.get("stroke-width"), 1.0), 1.0)
    left = min(x1, x2) - sw / 2.0
    right = max(x1, x2) + sw / 2.0
    top = min(y1, y2) - sw / 2.0
    bottom = max(y1, y2) + sw / 2.0
    return LineBox(file=Path(), left=left, top=top, right=right, bottom=bottom, stroke_width=sw)


def _collect_text_runs(elem: ET.Element) -> List[dict]:
    """
    从 <text> / <tspan> 中收集扁平文本段。
    
    参数:
        elem: SVG 文本元素
        
    返回:
        文本段列表
    """
    runs: List[dict] = []

    parent_text = _normalize_text(elem.text or "")
    if parent_text:
        runs.append({
            "text": parent_text,
            "font_size": _f(elem.get("font-size"), 16.0),
            "font_weight": elem.get("font-weight", "400"),
            "text_anchor": elem.get("text-anchor", "start"),
        })

    for child in elem:
        if child.tag.replace(f"{{{SVG_NS}}}", "") != "tspan":
            continue
        child_text = _normalize_text("".join(child.itertext()))
        if not child_text:
            continue
        runs.append({
            "text": child_text,
            "font_size": _f(child.get("font-size"), _f(elem.get("font-size"), 16.0)),
            "font_weight": child.get("font-weight", elem.get("font-weight", "400")),
            "text_anchor": child.get("text-anchor", elem.get("text-anchor", "start")),
        })

    return runs


def _collect_text_lines(elem: ET.Element) -> List[dict]:
    """
    Collect text lines with baseline offsets and style data from <text>/<tspan>.

    Each line dict contains text, font_size, font_weight, font_family, text_anchor,
    and dy (cumulative baseline offset from the parent text baseline).
    """
    lines: List[dict] = []
    parent_font_size = _f(elem.get("font-size"), 16.0)
    parent_font_weight = elem.get("font-weight", "400")
    parent_font_family = elem.get("font-family", "")
    parent_anchor = elem.get("text-anchor", "start")
    current_dy = 0.0

    parent_text = _normalize_text(elem.text or "")
    if parent_text:
        lines.append(
            {
                "text": parent_text,
                "font_size": parent_font_size,
                "font_weight": parent_font_weight,
                "font_family": parent_font_family,
                "text_anchor": parent_anchor,
                "dy": current_dy,
            }
        )

    for child in elem:
        if child.tag.replace(f"{{{SVG_NS}}}", "") != "tspan":
            continue
        child_text = _normalize_text("".join(child.itertext()))
        if not child_text:
            continue
        dy = _f(child.get("dy"), 0.0)
        current_dy += dy
        lines.append(
            {
                "text": child_text,
                "font_size": _f(child.get("font-size"), parent_font_size),
                "font_weight": child.get("font-weight", parent_font_weight),
                "font_family": child.get("font-family", parent_font_family),
                "text_anchor": child.get("text-anchor", parent_anchor),
                "dy": current_dy,
            }
        )

    return lines


def _estimate_text_box(elem: ET.Element) -> Optional[Tuple[float, float, float, float, str]]:
    """
    估算一个 <text> 的文本包围盒。
    
    参数:
        elem: SVG 文本元素
        
    返回:
        (X坐标, Y坐标, 宽度, 高度, 文本内容)，如果无法估算则返回 None
    """
    lines = _collect_text_lines(elem)
    if not lines:
        return None

    text = " ".join(line["text"] for line in lines).strip()
    if not text:
        return None

    x = _f(elem.get("x"))
    y = _f(elem.get("y"))
    anchor = elem.get("text-anchor", "start")
    abs_left = float("inf")
    abs_top = float("inf")
    abs_right = float("-inf")
    abs_bottom = float("-inf")

    for line in lines:
        bbox = _measure_line_bbox(
            line["text"],
            line["font_family"],
            line["font_size"],
            line["font_weight"],
            line["text_anchor"] or anchor,
        )
        if bbox is None:
            font_size = line["font_size"]
            font_weight = "700" if line["font_weight"] in ("bold", "600", "700", "800", "900") else "400"
            estimated_w = estimate_text_width(line["text"], font_size, font_weight)
            bbox = (
                -estimated_w / 2 if anchor == "middle" else -estimated_w if anchor == "end" else 0.0,
                -font_size * 0.76,
                estimated_w / 2 if anchor == "middle" else estimated_w,
                font_size * 0.60,
            )

        line_x = x
        line_y = y + line["dy"]
        left = line_x + bbox[0]
        top = line_y + bbox[1]
        right = line_x + bbox[2]
        bottom = line_y + bbox[3]
        abs_left = min(abs_left, left)
        abs_top = min(abs_top, top)
        abs_right = max(abs_right, right)
        abs_bottom = max(abs_bottom, bottom)

    if abs_left == float("inf"):
        return None

    return abs_left, abs_top, abs_right - abs_left, abs_bottom - abs_top, text


def audit_svg(svg_path: Path) -> List[TextIssue]:
    """
    扫描单个 SVG，找出可能越界的文本。
    
    参数:
        svg_path: SVG 文件路径
        
    返回:
        发现的问题列表
    """
    root, page_w, page_h = _parse_svg(svg_path)
    issues: List[TextIssue] = []
    rects: List[RectBox] = []
    text_boxes: List[TextBox] = []
    line_boxes: List[LineBox] = []

    # 以文档顺序扫描：遇到 <rect> 记为候选容器，遇到 <text> 就拿最近的容器做判断。
    for elem in root.iter():
        tag = elem.tag.replace(f"{{{SVG_NS}}}", "")
        if tag == "rect":
            rect = _parse_rect(elem)
            if rect is not None:
                rects.append(rect)
            continue

        if tag == "line":
            line = _parse_line(elem)
            if line is not None:
                line.file = svg_path
                line_boxes.append(line)
            continue

        if tag != "text":
            continue

        estimated = _estimate_text_box(elem)
        if estimated is None:
            continue

        anchor_x = _f(elem.get("x"))
        anchor_y = _f(elem.get("y"))
        # 页脚区域默认不做强校验，避免把页码、版权、页脚说明误判为内容超框。
        if anchor_y >= 640:
            continue

        box_x, box_y, box_w, box_h, text = estimated
        left = box_x
        top = box_y
        right = box_x + box_w
        bottom = box_y + box_h

        # 找到最近的、且 anchor 点落在其中的矩形容器。
        container: Optional[RectBox] = None
        for rect in reversed(rects):
            if not _is_visible_container_rect(rect):
                continue
            if rect.x <= anchor_x <= rect.right and rect.y <= anchor_y <= rect.bottom:
                container = rect
                break

        # 优先检查容器边界；如果没有容器，再退化成页面边界。
        if container is not None:
            padding = max(MIN_CONTAINER_PADDING_PX, min(container.w, container.h) * MIN_CONTAINER_PADDING_RATIO)
            if not container.contains(left, top, right, bottom, padding=padding):
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=text,
                        x=anchor_x,
                        y=anchor_y,
                        estimated_w=box_w,
                        estimated_h=box_h,
                        container=container,
                        reason="文本超出容器边界",
                    )
                )
        else:
            if left < 0 or top < 0 or right > page_w or bottom > page_h:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=text,
                        x=anchor_x,
                        y=anchor_y,
                        estimated_w=box_w,
                        estimated_h=box_h,
                        container=None,
                        reason="文本超出页面边界",
                    )
                )

        text_boxes.append(
            TextBox(
                file=svg_path,
                text=text,
                group=elem.get("data-group", ""),
                left=left,
                top=top,
                right=right,
                bottom=bottom,
                container=container,
            )
        )

    # 再做一次文本块之间的碰撞检测，防止两个文本框彼此压住。
    # 这里的门槛要尽量保守，只抓明显重叠，不把紧邻排版误判成错误。
    overlap_padding = 2.0
    for i in range(len(text_boxes)):
        a = text_boxes[i]
        for j in range(i + 1, len(text_boxes)):
            b = text_boxes[j]
            if a.file != b.file:
                continue
            if a.group and a.group == b.group:
                continue
            x_overlap = min(a.right, b.right) - max(a.left, b.left)
            y_overlap = min(a.bottom, b.bottom) - max(a.top, b.top)
            if x_overlap > overlap_padding and y_overlap > overlap_padding:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=b.text,
                        x=(b.left + b.right) / 2,
                        y=(b.top + b.bottom) / 2,
                        estimated_w=b.right - b.left,
                        estimated_h=b.bottom - b.top,
                        container=b.container,
                        reason=f"文本块与 '{a.text[:30]}' 重叠",
                    )
                )
                continue

            # 不一定要真的压住，只要在同一阅读方向上贴得太近，也算布局风险。
            vertical_gap = max(a.top, b.top) - min(a.bottom, b.bottom)
            horizontal_gap = max(a.left, b.left) - min(a.right, b.right)
            same_column = x_overlap > 20
            same_row = y_overlap > 20
            if same_column and 0 <= vertical_gap < MIN_TEXT_GAP:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=b.text,
                        x=(b.left + b.right) / 2,
                        y=(b.top + b.bottom) / 2,
                        estimated_w=b.right - b.left,
                        estimated_h=b.bottom - b.top,
                        container=b.container,
                        reason=f"文本间距过小：与 '{a.text[:30]}' 的垂直间距仅 {vertical_gap:.1f}px",
                    )
                )
            if same_row and 0 <= horizontal_gap < MIN_TEXT_GAP:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=b.text,
                        x=(b.left + b.right) / 2,
                        y=(b.top + b.bottom) / 2,
                        estimated_w=b.right - b.left,
                        estimated_h=b.bottom - b.top,
                        container=b.container,
                        reason=f"文本间距过小：与 '{a.text[:30]}' 的水平间距仅 {horizontal_gap:.1f}px",
                    )
                )

    # 线条与文本的碰撞检测，避免下划线、分隔线、装饰线压到文字上。
    line_padding = MIN_LINE_GAP
    for line in line_boxes:
        for box in text_boxes:
            if line.file != box.file:
                continue
            x_overlap = min(line.right, box.right) - max(line.left, box.left)
            y_overlap = min(line.bottom, box.bottom) - max(line.top, box.top)
            if x_overlap > line_padding and y_overlap > line_padding:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=box.text,
                        x=(box.left + box.right) / 2,
                        y=(box.top + box.bottom) / 2,
                        estimated_w=box.right - box.left,
                        estimated_h=box.bottom - box.top,
                        container=box.container,
                        reason="文本与线条重叠",
                    )
                )
                continue

            # 线条不穿字，但也不能贴得太近，尤其是标题下划线和分隔线。
            line_vertical_gap = max(box.top, line.top) - min(box.bottom, line.bottom)
            line_horizontal_gap = max(box.left, line.left) - min(box.right, line.right)
            if x_overlap > 20 and 0 <= line_vertical_gap < line_padding:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=box.text,
                        x=(box.left + box.right) / 2,
                        y=(box.top + box.bottom) / 2,
                        estimated_w=box.right - box.left,
                        estimated_h=box.bottom - box.top,
                        container=box.container,
                        reason=f"文本与线条间距过小：仅 {line_vertical_gap:.1f}px",
                    )
                )
            if y_overlap > 20 and 0 <= line_horizontal_gap < line_padding:
                issues.append(
                    TextIssue(
                        file=svg_path,
                        text=box.text,
                        x=(box.left + box.right) / 2,
                        y=(box.top + box.bottom) / 2,
                        estimated_w=box.right - box.left,
                        estimated_h=box.bottom - box.top,
                        container=box.container,
                        reason=f"文本与线条间距过小：仅 {line_horizontal_gap:.1f}px",
                    )
                )

    return issues


def main() -> int:
    """主函数"""
    parser = argparse.ArgumentParser(
        description="PPT Master - SVG 文本版式预检",
    )
    parser.add_argument("project_path", help="项目目录")
    parser.add_argument("-q", "--quiet", action="store_true", help="只输出错误，不输出提示")
    args = parser.parse_args()

    project_path = Path(args.project_path)
    svg_dir = project_path / "svg_output"
    if not svg_dir.exists():
        print(f"[ERROR] 未找到 svg_output：{svg_dir}")
        return 2

    svg_files = sorted(svg_dir.glob("*.svg"))
    if not svg_files:
        print("[WARN] svg_output 里没有 SVG 文件")
        return 0

    all_issues: List[TextIssue] = []
    for svg_file in svg_files:
        issues = audit_svg(svg_file)
        all_issues.extend(issues)

    if not all_issues:
        if not args.quiet:
            print(f"[OK] 文本预检通过：{len(svg_files)} 个 SVG 未发现明显出框")
        return 0

    print(f"[ERROR] 文本预检发现 {len(all_issues)} 个潜在出框问题：")
    for item in all_issues:
        container_desc = "页面边界"
        if item.container is not None:
            c = item.container
            container_desc = f"容器({c.x:.0f},{c.y:.0f},{c.w:.0f},{c.h:.0f})"
        snippet = item.text if len(item.text) <= 60 else item.text[:57] + "..."
        print(
            f"  - {item.file.name}: {snippet} | "
            f"估算框={item.estimated_w:.0f}×{item.estimated_h:.0f} | "
            f"{container_desc} | {item.reason}"
        )

    print("\n建议：先改 svg_output 里的原始文本，必要时手动断行或缩短句子，再重新 finalize。")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
