"""
llm_engine.py — Call Groq LLM to extract topics/subtopics/concepts from syllabus chunks.
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

SYSTEM_PROMPT = """You are an expert academic curriculum analyst. Given a chunk of syllabus text, extract and organize the content into a structured hierarchy of topics, subtopics, and concepts.

Rules:
1. Identify distinct TOPICS (broad subject areas).
2. Under each topic, list SUBTOPICS (specific areas within the topic).
3. Under each subtopic, list CONCEPTS (individual terms, theories, methods, or ideas).
4. Maintain a clean hierarchy — no duplicates within the same chunk.
5. If text is unclear, infer the best reasonable structure.

You MUST respond with ONLY valid JSON in this exact format, no extra text:
{
  "topics": [
    {
      "name": "Topic Name",
      "subtopics": [
        {
          "name": "Subtopic Name",
          "concepts": ["Concept 1", "Concept 2"]
        }
      ]
    }
  ]
}"""

USER_PROMPT_TEMPLATE = """Analyze the following syllabus text and extract topics, subtopics, and concepts in the required JSON format.

--- SYLLABUS TEXT ---
{chunk}
--- END ---"""


async def extract_topics(chunk: str, chunk_index: int = 0) -> dict:
    """Send a chunk to Groq LLM and return structured JSON."""
    api_key = _get_api_key()
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Add it to backend/.env file."
        )

    client = AsyncGroq(api_key=api_key)
    user_prompt = USER_PROMPT_TEMPLATE.format(chunk=chunk)

    logger.info(f"[Chunk {chunk_index}] Sending to LLM ({len(chunk)} chars)")
    logger.info(f"[Chunk {chunk_index}] Prompt:\n{user_prompt[:200]}...")

    for attempt in range(3):
        try:
            response = await client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_tokens=4096,
                response_format={"type": "json_object"},
            )

            content = response.choices[0].message.content.strip()
            logger.info(f"[Chunk {chunk_index}] Raw LLM response (attempt {attempt + 1}):\n{content[:300]}...")

            parsed = json.loads(content)

            # Validate structure
            if "topics" not in parsed:
                raise ValueError("Missing 'topics' key in response")

            for topic in parsed["topics"]:
                if "name" not in topic or "subtopics" not in topic:
                    raise ValueError("Invalid topic structure")
                for sub in topic["subtopics"]:
                    if "name" not in sub or "concepts" not in sub:
                        raise ValueError("Invalid subtopic structure")

            logger.info(
                f"[Chunk {chunk_index}] Extracted {len(parsed['topics'])} topics"
            )
            return parsed

        except json.JSONDecodeError as e:
            logger.warning(f"[Chunk {chunk_index}] JSON parse error (attempt {attempt + 1}): {e}")
            if attempt == 2:
                logger.error(f"[Chunk {chunk_index}] Failed after 3 attempts")
                return {"topics": []}
        except Exception as e:
            logger.warning(f"[Chunk {chunk_index}] Error (attempt {attempt + 1}): {e}")
            if attempt == 2:
                logger.error(f"[Chunk {chunk_index}] Failed after 3 attempts: {e}")
                return {"topics": []}

    return {"topics": []}
