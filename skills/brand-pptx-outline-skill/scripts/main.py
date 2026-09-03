#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from typing import Any

from openai import OpenAI


MODEL_DEFAULT = os.getenv("BRAND_PPT_MODEL", "qwen-plus")
BASE_URL = os.getenv("QWEN_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")

ROLE_PLAN = [
    ("cover", "建立品牌主题与开场判断"),
    ("mission", "说明品牌使命如何定义长期边界"),
    ("brand_dna", "拆解品牌核心主张与识别秩序"),
    ("product", "说明产品语言如何承接品牌价值"),
    ("experience", "说明体验系统如何降低理解成本"),
    ("ecosystem", "说明协同关系如何形成品牌护城河"),
    ("software", "说明数字化与服务如何延长价值兑现"),
    ("manufacturing", "说明组织与兑现能力如何支撑品牌承诺"),
    ("innovation", "说明创新如何持续转化为品牌资产"),
    ("closing", "收束成一句可复述的品牌判断"),
]


def load_client(api_key: str | None) -> OpenAI:
    key = (api_key or os.getenv("QWEN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or "").strip()
    if not key:
        raise RuntimeError("missing QWEN_API_KEY or DASHSCOPE_API_KEY")
    return OpenAI(api_key=key, base_url=BASE_URL)


def extract_json(text: str) -> Any:
    cleaned = text.strip()
    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.I)
        cleaned = re.sub(r"\s*```$", "", cleaned)
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start < 0 or end < 0 or end <= start:
        raise ValueError(f"no JSON object found: {text[:200]}")
    return json.loads(cleaned[start : end + 1])


def call_qwen_json(prompt: str, api_key: str | None, model: str) -> Any:
    client = load_client(api_key)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "你是品牌类PPT大纲策划。只输出严格 JSON。"
                    "不要输出 markdown、解释、代码块或任何额外文字。"
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.35,
        max_tokens=5000,
    )
    return extract_json(resp.choices[0].message.content or "")


def build_prompt(topic: str, count: int, audience: str, purpose: str, tone: str, focus: str) -> str:
    role_list = " / ".join(role for role, _ in ROLE_PLAN[:count])
    return f"""
请为下面的品牌类 PPT 生成结构化 outline.json。
主题：{topic}
页数：{count}
受众：{audience or "品牌 / 战略 / 市场 / 管理层"}
用途：{purpose or "品牌战略 / 品牌发布 / 品牌解读"}
语气：{tone or "清晰、克制、系统化"}
侧重点：{focus or "品牌主张、识别秩序、产品语言、体验系统、长期兑现"}

要求：
1. 这是品牌类专项 PPT 大纲，不是咨询报告，不是完整正文。
2. 只输出叙事大纲和内容边界，不要输出组件、版式、布局、配色、样式、字体、图标、页面设计建议。
3. 每页只保留一个主判断，必须有 intent / core / focus / key_message / evidence。
4. evidence 是内容线索或论据，不是完整段落。
5. 不要输出任何容量参数、版式参数或视觉参数。
6. 使用以下角色并按顺序输出：{role_list}
7. 输出必须是合法 JSON，对象结构如下：
{{
  "title": "...",
  "topic": "...",
  "brand": "...",
  "scenario": "...",
  "audience": "...",
  "purpose": "...",
  "tone": "...",
  "page_count": {count},
  "pages": [
    {{
      "page_no": 1,
      "role": "cover",
      "intent": "...",
      "core": "...",
      "focus": "...",
      "key_message": "...",
      "evidence": ["...", "..."]
    }}
  ]
}}
""".strip()


def normalize_outline(
    raw: dict[str, Any],
    topic: str,
    count: int,
    audience: str,
    purpose: str,
    tone: str,
    focus: str,
) -> dict[str, Any]:
    pages = raw.get("pages") or []
    normalized_pages: list[dict[str, Any]] = []
    for idx, (role, default_intent) in enumerate(ROLE_PLAN[:count], start=1):
        source = pages[idx - 1] if idx - 1 < len(pages) and isinstance(pages[idx - 1], dict) else {}
        normalized_pages.append(
            {
                "page_no": idx,
                "role": source.get("role") or role,
                "title": source.get("title") or "",
                "subtitle": source.get("subtitle") or "",
                "intent": source.get("intent") or default_intent,
                "core": source.get("core") or source.get("key_message") or "",
                "focus": source.get("focus") or focus or "",
                "key_message": source.get("key_message") or source.get("core") or "",
                "evidence": source.get("evidence") or [],
            }
        )

    return {
        "title": raw.get("title") or f"{topic} 品牌解读",
        "topic": raw.get("topic") or topic,
        "brand": raw.get("brand") or raw.get("topic") or topic,
        "scenario": raw.get("scenario") or "品牌战略 / 品牌表达 / 品牌发布",
        "audience": raw.get("audience") or audience or "品牌 / 战略 / 市场 / 管理层",
        "purpose": raw.get("purpose") or purpose or "品牌战略 / 品牌发布 / 品牌解读",
        "tone": raw.get("tone") or tone or "清晰、克制、系统化",
        "page_count": len(normalized_pages),
        "pages": normalized_pages,
    }


async def run(inputs: dict, context=None):
    topic = str(inputs.get("topic", "")).strip()
    if not topic:
        return {
            "status": "failed",
            "summary": "missing topic",
            "outputs": {},
            "artifacts": [],
            "error": {"message": "topic is required"},
        }

    count = int(inputs.get("count", 10) or 10)
    audience = str(inputs.get("audience", "") or "")
    purpose = str(inputs.get("purpose", "") or "")
    tone = str(inputs.get("tone", "") or "")
    focus = str(inputs.get("focus", "") or "")
    model = str(inputs.get("model", MODEL_DEFAULT) or MODEL_DEFAULT)
    api_key = str(inputs.get("api_key", "") or "")
    output = str(inputs.get("output", "") or "")
    dry_run = bool(inputs.get("dry_run", False))

    try:
        # Allow local validation without a live model call.
        if dry_run:
            raw = {
                "title": f"{topic} 品牌解读",
                "topic": topic,
                "brand": topic,
                "scenario": "品牌战略 / 品牌表达 / 品牌发布",
                "audience": audience or "品牌 / 战略 / 市场 / 管理层",
                "purpose": purpose or "品牌战略 / 品牌发布 / 品牌解读",
                "tone": tone or "清晰、克制、系统化",
                "page_count": count,
                "pages": [
                    {
                        "page_no": idx,
                        "role": role,
                        "intent": default_intent,
                        "core": "",
                        "focus": focus or "",
                        "key_message": "",
                        "evidence": [],
                    }
                    for idx, (role, default_intent) in enumerate(ROLE_PLAN[:count], start=1)
                ],
            }
        else:
            prompt = build_prompt(topic, count, audience, purpose, tone, focus)
            raw = call_qwen_json(prompt, api_key, model)

        # Normalize the model output so downstream PPT tooling sees a stable schema.
        outline = normalize_outline(raw, topic, count, audience, purpose, tone, focus)
        payload = json.dumps(outline, ensure_ascii=False, indent=2)
        artifacts: list[str] = []
        if output:
            output_path = Path(output).resolve()
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(payload, encoding="utf-8")
            artifacts.append(str(output_path))
        return {
            "status": "success",
            "summary": f"generated outline for topic={topic} page_count={outline['page_count']}",
            "outputs": {"outline": outline, "payload": payload},
            "artifacts": artifacts,
            "error": None,
        }
    except Exception as exc:
        return {
            "status": "failed",
            "summary": f"outline generation failed: {exc}",
            "outputs": {},
            "artifacts": [],
            "error": {"message": str(exc)},
        }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate brand PPT outline JSON")
    parser.add_argument("--topic", "-t", required=True)
    parser.add_argument("--count", "-n", type=int, default=10)
    parser.add_argument("--audience", "-a", default="")
    parser.add_argument("--purpose", "-p", default="")
    parser.add_argument("--tone", "-g", default="")
    parser.add_argument("--focus", "-f", default="")
    parser.add_argument("--model", default=MODEL_DEFAULT)
    parser.add_argument("--api-key", default="")
    parser.add_argument("--output", "-o", default="")
    args = parser.parse_args()

    prompt = build_prompt(args.topic, args.count, args.audience, args.purpose, args.tone, args.focus)
    raw = call_qwen_json(prompt, args.api_key, args.model)
    outline = normalize_outline(raw, args.topic, args.count, args.audience, args.purpose, args.tone, args.focus)
    payload = json.dumps(outline, ensure_ascii=False, indent=2)
    if args.output:
        Path(args.output).write_text(payload, encoding="utf-8")
    else:
        print(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
