"""
merger.py — Merge topic outputs from multiple chunks, deduplicate, and consolidate.
"""

from logger_config import get_logger

logger = get_logger(__name__)


def _normalize(name: str) -> str:
    """Lowercase and strip for comparison."""
    return name.strip().lower()


def merge_results(results: list[dict]) -> dict:
    """Merge multiple chunk results into a single unified topic tree."""
    logger.info(f"Merging results from {len(results)} chunks")

    topic_map: dict[str, dict] = {}  # normalized_name -> topic dict

    for result in results:
        for topic in result.get("topics", []):
            topic_name = topic.get("name", "").strip()
            if not topic_name:
                continue

            norm_key = _normalize(topic_name)

            if norm_key not in topic_map:
                topic_map[norm_key] = {
                    "name": topic_name,
                    "subtopics": {},
                }

            existing = topic_map[norm_key]

            for sub in topic.get("subtopics", []):
                sub_name = sub.get("name", "").strip()
                if not sub_name:
                    continue
                sub_norm = _normalize(sub_name)

                if sub_norm not in existing["subtopics"]:
                    existing["subtopics"][sub_norm] = {
                        "name": sub_name,
                        "concepts": set(),
                    }

                for concept in sub.get("concepts", []):
                    c = concept.strip()
                    if c:
                        existing["subtopics"][sub_norm]["concepts"].add(_normalize(c))
                        # Keep original casing: store original alongside
                        existing["subtopics"][sub_norm].setdefault("_originals", {})[_normalize(c)] = c

    # Convert back to list format
    merged_topics = []
    for t_data in topic_map.values():
        subtopics = []
        for s_data in t_data["subtopics"].values():
            originals = s_data.get("_originals", {})
            concepts = [originals.get(c, c) for c in sorted(s_data["concepts"])]
            subtopics.append({
                "name": s_data["name"],
                "concepts": concepts,
            })
        merged_topics.append({
            "name": t_data["name"],
            "subtopics": subtopics,
        })

    logger.info(f"Merged into {len(merged_topics)} unique topics")
    return {"topics": merged_topics}
