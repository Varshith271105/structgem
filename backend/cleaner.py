"""
cleaner.py — Text preprocessing: remove noise, normalize formatting.
"""

import re
from logger_config import get_logger

logger = get_logger(__name__)


def clean_text(raw_text: str) -> str:
    """Clean and normalize syllabus text."""
    logger.info(f"Cleaning text ({len(raw_text)} chars)")
    text = raw_text

    # Remove common page headers/footers patterns
    text = re.sub(r"(?i)page\s*\d+\s*(of\s*\d+)?", "", text)
    text = re.sub(r"(?i)^\s*(confidential|draft|internal)\s*$", "", text, flags=re.MULTILINE)

    # Remove standalone page numbers
    text = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", text)

    # Normalize bullet characters to a single dash
    text = re.sub(r"(?m)^\s*[•●○▪▸►◆→➤➢✓✔☐☑]\s*", "- ", text)
    text = re.sub(r"(?m)^\s*\d+[\.\)]\s+", "- ", text)

    # Normalize whitespace
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = text.strip()

    logger.info(f"Cleaned text: {len(text)} chars")
    return text
