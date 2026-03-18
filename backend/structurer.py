"""
structurer.py — Logically order topics from basic→advanced, foundational→applied.
Uses LLM to determine ordering when available, falls back to heuristic.
"""

import json
import os
from groq import AsyncGroq
from logger_config import get_logger

logger = get_logger(__name__)


def _get_api_key():
    """Get Groq API key from environment (loaded from .env by main.py)."""
    return os.environ.get("GROQ_API_KEY", "")


MODEL = "llama-3.3-70b-versatile"

ORDERING_PROMPT = """You are given a list of academic topics extracted from a syllabus. 
Reorder them from most foundational/basic to most advanced/applied.
Also reorder the subtopics within each topic from basic to advanced.

Return the reordered structure as valid JSON in EXACTLY this format:
{{
  "topics": [
    {{
      "name": "Topic Name",
      "subtopics": [
        {{
          "name": "Subtopic Name",
          "concepts": ["Concept 1", "Concept 2"]
        }}
      ]
    }}
  ]
}}

Input topics:
{topics_json}"""


async def structure_topics(merged: dict) -> dict:
    """Reorder topics from basic→advanced using LLM."""
    topics = merged.get("topics", [])
    if len(topics) <= 1:
        return merged

    logger.info(f"Structuring {len(topics)} topics (basic → advanced)")

    # Try LLM-based ordering
    api_key = _get_api_key()
    if api_key:
        try:
            return await _llm_order(merged, api_key)
        except Exception as e:
            logger.warning(f"LLM ordering failed, using heuristic: {e}")

    # Fallback: heuristic ordering (alphabetical with 'Introduction' first)
    return _heuristic_order(merged)


async def _llm_order(merged: dict, api_key: str) -> dict:
    """Use LLM to reorder topics."""
    client = AsyncGroq(api_key=api_key)
    topics_json = json.dumps(merged, indent=2)

    prompt = ORDERING_PROMPT.format(topics_json=topics_json)
    logger.info("Sending ordering request to LLM")

    response = await client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=4096,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content.strip()
    result = json.loads(content)

    if "topics" in result:
        logger.info("LLM ordering successful")
        return result

    return merged


def _heuristic_order(merged: dict) -> dict:
    """Simple heuristic: put intro/basics first, sort rest alphabetically."""
    topics = merged.get("topics", [])

    intro_keywords = {"introduction", "basics", "fundamentals", "overview", "foundation"}

    intro_topics = []
    other_topics = []

    for t in topics:
        name_lower = t["name"].lower()
        if any(kw in name_lower for kw in intro_keywords):
            intro_topics.append(t)
        else:
            other_topics.append(t)

    intro_topics.sort(key=lambda x: x["name"].lower())
    other_topics.sort(key=lambda x: x["name"].lower())

    return {"topics": intro_topics + other_topics}
