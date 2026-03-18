"""
pdf_export.py — Generate a styled PDF from structured topic data using ReportLab.
"""

import io
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    HRFlowable,
)
from logger_config import get_logger

logger = get_logger(__name__)


def generate_pdf(topics: list, title: str = "Syllabus Topic Structure") -> bytes:
    """Generate a styled PDF from structured topic data. Returns PDF bytes."""
    logger.info(f"Generating PDF for {len(topics)} topics")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=HexColor("#1a1a2e"),
        spaceAfter=20,
    )
    topic_style = ParagraphStyle(
        "TopicStyle",
        parent=styles["Heading2"],
        fontSize=16,
        textColor=HexColor("#16213e"),
        spaceBefore=16,
        spaceAfter=8,
        leftIndent=0,
    )
    subtopic_style = ParagraphStyle(
        "SubtopicStyle",
        parent=styles["Heading3"],
        fontSize=13,
        textColor=HexColor("#0f3460"),
        spaceBefore=10,
        spaceAfter=4,
        leftIndent=20,
    )
    concept_style = ParagraphStyle(
        "ConceptStyle",
        parent=styles["Normal"],
        fontSize=11,
        textColor=HexColor("#333333"),
        leftIndent=40,
        spaceBefore=2,
        spaceAfter=2,
    )

    elements = []
    elements.append(Paragraph(title, title_style))
    elements.append(HRFlowable(width="100%", thickness=1, color=HexColor("#cccccc")))
    elements.append(Spacer(1, 12))

    for i, topic in enumerate(topics):
        topic_name = topic.get("name", f"Topic {i + 1}")
        elements.append(Paragraph(f"{i + 1}. {topic_name}", topic_style))

        subtopics = topic.get("subtopics", [])
        for j, subtopic in enumerate(subtopics):
            sub_name = subtopic.get("name", f"Subtopic {j + 1}")
            elements.append(
                Paragraph(f"{i + 1}.{j + 1} {sub_name}", subtopic_style)
            )

            concepts = subtopic.get("concepts", [])
            for concept in concepts:
                c = concept if isinstance(concept, str) else str(concept)
                elements.append(Paragraph(f"\u2022 {c}", concept_style))

        elements.append(Spacer(1, 8))

    doc.build(elements)
    pdf_bytes = buffer.getvalue()
    logger.info(f"PDF generated: {len(pdf_bytes)} bytes")
    return pdf_bytes
