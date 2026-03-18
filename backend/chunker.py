"""
chunker.py — Split text into token-bounded chunks (~500–800 tokens).
"""

import tiktoken
from logger_config import get_logger

logger = get_logger(__name__)

ENCODING = tiktoken.get_encoding("cl100k_base")
MIN_TOKENS = 500
MAX_TOKENS = 800


def chunk_text(text: str) -> list[str]:
    """Split text into chunks of approximately 500–800 tokens."""
    paragraphs = text.split("\n\n")
    chunks: list[str] = []
    current_chunk: list[str] = []
    current_tokens = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
        para_tokens = len(ENCODING.encode(para))

        # If a single paragraph exceeds MAX_TOKENS, split it by sentences
        if para_tokens > MAX_TOKENS:
            if current_chunk:
                chunks.append("\n\n".join(current_chunk))
                current_chunk = []
                current_tokens = 0
            _split_large_paragraph(para, chunks)
            continue

        if current_tokens + para_tokens > MAX_TOKENS and current_chunk:
            chunks.append("\n\n".join(current_chunk))
            current_chunk = []
            current_tokens = 0

        current_chunk.append(para)
        current_tokens += para_tokens

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    logger.info(f"Split text into {len(chunks)} chunks")
    for i, c in enumerate(chunks):
        t = len(ENCODING.encode(c))
        logger.info(f"  Chunk {i + 1}: {t} tokens")

    return chunks


def _split_large_paragraph(para: str, chunks: list[str]):
    """Split an oversized paragraph into sentence-based chunks."""
    import re

    sentences = re.split(r"(?<=[.!?])\s+", para)
    buf: list[str] = []
    buf_tokens = 0

    for sent in sentences:
        sent_tokens = len(ENCODING.encode(sent))
        if buf_tokens + sent_tokens > MAX_TOKENS and buf:
            chunks.append(" ".join(buf))
            buf = []
            buf_tokens = 0
        buf.append(sent)
        buf_tokens += sent_tokens

    if buf:
        chunks.append(" ".join(buf))
