from __future__ import annotations

import re
from pathlib import Path
from xml.etree import ElementTree as ET

ASCII_TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._/+:-]*")
TRANSLATE_RE = re.compile(r"translate\(([-0-9.]+)[ ,]([-0-9.]+)\)")


def tokenize_mixed_text(text: str) -> list[str]:
    text = str(text or "")
    tokens: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        m = ASCII_TOKEN_RE.match(text, i)
        if m:
            tokens.append(m.group(0))
            i = m.end()
            continue
        if ch.isspace():
            if tokens and tokens[-1] != " ":
                tokens.append(" ")
            i += 1
            continue
        if "\u4e00" <= ch <= "\u9fff":
            j = i + 1
            while j < n and "\u4e00" <= text[j] <= "\u9fff":
                j += 1
            tokens.append(text[i:j])
            i = j
            continue
        tokens.append(ch)
        i += 1
    return tokens


def token_units(token: str) -> int:
    if token == " ":
        return 1
    if ASCII_TOKEN_RE.fullmatch(token):
        return max(2, len(token))
    return len(token)


def cjk_safe_wrap(text: str, width: int, max_lines: int = 3) -> list[str]:
    tokens = tokenize_mixed_text(text.strip())
    if not tokens:
        return [""]

    lines: list[str] = []
    current: list[str] = []
    used = 0

    for token in tokens:
        units = token_units(token)
        if token == " " and not current:
            continue
        if current and used + units > width:
            lines.append("".join(current).strip())
            current = [] if token == " " else [token]
            used = 0 if token == " " else units
            continue
        current.append(token)
        used += units

    if current:
        lines.append("".join(current).strip())

    lines = [line for line in lines if line]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip("，。；,.; ") + "..."
    return lines or [""]


try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:  # pragma: no cover
    Image = None  # type: ignore[assignment]
    ImageDraw = None  # type: ignore[assignment]
    ImageFont = None  # type: ignore[assignment]


FONT_FILE_CANDIDATES = {
    'Segoe UI': [r'C:\Windows\Fonts\segoeui.ttf'],
    'Segoe UI Bold': [r'C:\Windows\Fonts\segoeuib.ttf'],
    'Arial': [r'C:\Windows\Fonts\arial.ttf'],
    'Arial Bold': [r'C:\Windows\Fonts\arialbd.ttf'],
    'Microsoft YaHei': [r'C:\Windows\Fonts\msyh.ttc', r'C:\Windows\Fonts\msyh.ttf'],
    'Microsoft YaHei Bold': [r'C:\Windows\Fonts\msyhbd.ttc', r'C:\Windows\Fonts\msyhbd.ttf'],
    'SimSun': [r'C:\Windows\Fonts\simsun.ttc'],
}


def _pick_font_file(font_family: str, font_weight: str) -> str | None:
    family = (font_family or 'Microsoft YaHei').strip().strip("'\"")
    if font_weight in ('bold', '600', '700', '800', '900') and family == 'Microsoft YaHei':
        family = 'Microsoft YaHei Bold'
    elif font_weight in ('bold', '600', '700', '800', '900') and family == 'Segoe UI':
        family = 'Segoe UI Bold'
    elif font_weight in ('bold', '600', '700', '800', '900') and family == 'Arial':
        family = 'Arial Bold'
    for candidate in FONT_FILE_CANDIDATES.get(family, []) + FONT_FILE_CANDIDATES.get('Microsoft YaHei', []):
        if Path(candidate).exists():
            return candidate
    return None


def measure_text_width_px(text: str, font_size: float, font_family: str = 'Microsoft YaHei', font_weight: str = '400') -> float:
    text = str(text or '')
    if not text:
        return 0.0
    if Image and ImageDraw and ImageFont:
        font_path = _pick_font_file(font_family, font_weight)
        if font_path:
            try:
                font = ImageFont.truetype(font_path, size=max(1, int(round(font_size))))
                dummy = Image.new('RGB', (4, 4), 'white')
                draw = ImageDraw.Draw(dummy)
                left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
                return float(right - left)
            except Exception:
                pass
    width = 0.0
    for token in tokenize_mixed_text(text):
        if token == ' ':
            width += font_size * 0.32
        elif ASCII_TOKEN_RE.fullmatch(token):
            width += len(token) * font_size * 0.56
        else:
            width += len(token) * font_size * 0.96
    if font_weight in ('bold', '600', '700', '800', '900'):
        width *= 1.03
    return width


def cjk_wrap_to_px(text: str, max_width_px: float, font_size: float, font_family: str = 'Microsoft YaHei', font_weight: str = '400', max_lines: int = 3) -> list[str]:
    text = str(text or '').strip()
    if not text:
        return ['']
    if measure_text_width_px(text, font_size, font_family, font_weight) <= max_width_px:
        return [text]

    tokens = tokenize_mixed_text(text)
    lines: list[str] = []
    current: list[str] = []

    def current_text(next_token: str | None = None) -> str:
        parts = current.copy()
        if next_token is not None:
            parts.append(next_token)
        return ''.join(parts).strip()

    for token in tokens:
        if token == ' ' and not current:
            continue
        trial = current_text(token)
        if current and measure_text_width_px(trial, font_size, font_family, font_weight) > max_width_px:
            lines.append(''.join(current).strip())
            current = [] if token == ' ' else [token]
            continue
        current.append(token)

    if current:
        lines.append(''.join(current).strip())

    lines = [line for line in lines if line]
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and measure_text_width_px(last + '...', font_size, font_family, font_weight) > max_width_px:
            last = last[:-1].rstrip('，。；,.; ')
        lines[-1] = (last.rstrip('，。；,.; ') or last) + '...'
    return lines or ['']


def _format_number(num: float) -> str:
    return str(int(num)) if float(num).is_integer() else str(round(num, 2))


def _shift_points(points: str, dx: float, dy: float) -> str:
    vals = re.findall(r"[-+]?[0-9]*\.?[0-9]+", points)
    nums = [float(v) for v in vals]
    parts = []
    for i in range(0, len(nums), 2):
        if i + 1 < len(nums):
            parts.append(f"{_format_number(nums[i] + dx)},{_format_number(nums[i + 1] + dy)}")
    return " ".join(parts)


def _apply_translate(elem: ET.Element, dx: float, dy: float) -> None:
    for attr in ("x", "x1", "x2", "cx"):
        if elem.get(attr) is not None:
            elem.set(attr, _format_number(float(elem.get(attr)) + dx))
    for attr in ("y", "y1", "y2", "cy"):
        if elem.get(attr) is not None:
            elem.set(attr, _format_number(float(elem.get(attr)) + dy))
    if elem.get("points"):
        elem.set("points", _shift_points(elem.get("points"), dx, dy))


def _apply_translate_recursive(elem: ET.Element, dx: float, dy: float) -> None:
    _apply_translate(elem, dx, dy)
    for child in list(elem):
        _apply_translate_recursive(child, dx, dy)


def flatten_translate_groups(svg_path: str | Path) -> bool:
    svg_path = Path(svg_path)
    tree = ET.parse(svg_path)
    root = tree.getroot()
    changed = False

    while True:
        pass_changed = False
        for parent in root.iter():
            children = list(parent)
            for child in children:
                tr = child.get("transform", "")
                m = TRANSLATE_RE.fullmatch(tr)
                if not (child.tag.endswith("g") and m):
                    continue
                dx = float(m.group(1))
                dy = float(m.group(2))
                insert_at = list(parent).index(child)
                parent.remove(child)
                moved = list(child)
                for offset, grand in enumerate(moved):
                    _apply_translate_recursive(grand, dx, dy)
                    parent.insert(insert_at + offset, grand)
                pass_changed = True
                changed = True
                break
            if pass_changed:
                break
        if not pass_changed:
            break

    if changed:
        tree.write(svg_path, encoding="utf-8", xml_declaration=True)
    return changed
