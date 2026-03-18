"""
parser.py — Extract text from PDF and TXT files.
"""

import io
from logger_config import get_logger

logger = get_logger(__name__)


def parse_file(file_bytes: bytes, filename: str) -> str:
    """Extract text from an uploaded file (PDF or TXT)."""
    ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    logger.info(f"Parsing file: {filename} (type: {ext}, size: {len(file_bytes)} bytes)")

    if ext == "pdf":
        return _parse_pdf(file_bytes)
    elif ext == "txt":
        return file_bytes.decode("utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type: .{ext}. Only PDF and TXT are supported.")


def parse_text(raw_text: str) -> str:
    """Passthrough for raw text input."""
    logger.info(f"Received raw text input ({len(raw_text)} chars)")
    return raw_text


def _parse_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF using pdfplumber."""
    import pdfplumber

    text_parts = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages):
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)
                logger.info(f"  Page {i + 1}: extracted {len(page_text)} chars")
    full_text = "\n\n".join(text_parts)
    logger.info(f"PDF parsing complete: {len(full_text)} total chars from {len(text_parts)} pages")
    return full_text
