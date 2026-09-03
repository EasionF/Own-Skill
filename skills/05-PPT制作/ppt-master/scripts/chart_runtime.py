from __future__ import annotations

import math


def esc(text: str) -> str:
    return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def fmt_b(value: float) -> str:
    return f"${value:.1f}B"


def note(title: str, bullets: list[str], source: str) -> str:
    return "\n".join([f"# {title}", "", "## Key points", *[f"- {b}" for b in bullets], "", "## Source", f"- {source}", ""])


def nice_ticks(max_value: float, count: int = 5) -> list[float]:
    if max_value <= 0:
        return [0]
    raw = max_value / count
    mag = 10 ** math.floor(math.log10(raw))
    candidate = None
    for step in [1, 2, 2.5, 5, 10]:
        candidate = step * mag
        if candidate >= raw:
            break
    top = math.ceil(max_value / candidate) * candidate
    return [i * candidate for i in range(int(top / candidate) + 1)]
