"""
pdf_export.py — Generate a branded, styled PDF from structured topic data using ReportLab.
"""

import io
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable,
    KeepTogether,
)
from logger_config import get_logger

logger = get_logger(__name__)

LOGO_PATH = os.path.join(os.path.dirname(__file__), "logo.jpeg")

BRAND_PRIMARY = HexColor("#6366F1")
BRAND_DARK = HexColor("#0a0a0f")
BRAND_ACCENT = HexColor("#818CF8")
BRAND_LIGHT_BG = HexColor("#EEF0FF")
BRAND_GRAY = HexColor("#64748b")
BRAND_BORDER = HexColor("#C7D2FE")
BRAND_WHITE = HexColor("#FFFFFF")
BRAND_CONCEPT_BG = HexColor("#F5F3FF")
BRAND_TEXT = HexColor("#1e293b")
BRAND_SUBTLE = HexColor("#94a3b8")

PAGE_W, PAGE_H = A4


def _draw_header_footer(canvas, doc):
    canvas.saveState()

    canvas.setStrokeColor(BRAND_PRIMARY)
    canvas.setLineWidth(2)
    canvas.line(doc.leftMargin, PAGE_H - 52, PAGE_W - doc.rightMargin, PAGE_H - 52)

    logo_path = os.path.normpath(LOGO_PATH)
    if os.path.exists(logo_path):
        canvas.drawImage(
            logo_path,
            doc.leftMargin,
            PAGE_H - 47,
            width=90,
            height=28,
            preserveAspectRatio=True,
            mask="auto",
        )
    else:
        canvas.setFont("Helvetica-Bold", 11)
        canvas.setFillColor(BRAND_PRIMARY)
        canvas.drawString(doc.leftMargin, PAGE_H - 44, "StructGem")

    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(BRAND_GRAY)
    canvas.drawRightString(
        PAGE_W - doc.rightMargin, PAGE_H - 44, "Smart Syllabus Topic Segregator"
    )

    canvas.setStrokeColor(BRAND_BORDER)
    canvas.setLineWidth(0.5)
    canvas.line(doc.leftMargin, 40, PAGE_W - doc.rightMargin, 40)

    canvas.setFont("Helvetica", 7.5)
    canvas.setFillColor(BRAND_GRAY)
    canvas.drawString(
        doc.leftMargin,
        28,
        f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
    )
    canvas.drawRightString(PAGE_W - doc.rightMargin, 28, f"Page {doc.page}")

    canvas.restoreState()


def _build_styles():
    styles = getSampleStyleSheet()

    return {
        "title": ParagraphStyle(
            "ReportTitle",
            parent=styles["Title"],
            fontSize=26,
            leading=32,
            textColor=BRAND_DARK,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "ReportSubtitle",
            parent=styles["Normal"],
            fontSize=11,
            textColor=BRAND_GRAY,
            spaceAfter=24,
            fontName="Helvetica",
        ),
        "topic": ParagraphStyle(
            "TopicStyle",
            parent=styles["Heading2"],
            fontSize=14,
            leading=18,
            textColor=BRAND_WHITE,
            fontName="Helvetica-Bold",
            leftIndent=4,
        ),
        "subtopic": ParagraphStyle(
            "SubtopicStyle",
            parent=styles["Heading3"],
            fontSize=12,
            leading=16,
            textColor=BRAND_PRIMARY,
            spaceBefore=10,
            spaceAfter=6,
            leftIndent=8,
            fontName="Helvetica-Bold",
        ),
        "concept": ParagraphStyle(
            "ConceptStyle",
            parent=styles["Normal"],
            fontSize=10,
            leading=14,
            textColor=BRAND_TEXT,
            leftIndent=24,
            spaceBefore=2,
            spaceAfter=2,
            fontName="Helvetica",
        ),
        "summary_label": ParagraphStyle(
            "SummaryLabel",
            parent=styles["Normal"],
            fontSize=9,
            textColor=BRAND_GRAY,
            fontName="Helvetica",
        ),
        "summary_value": ParagraphStyle(
            "SummaryValue",
            parent=styles["Normal"],
            fontSize=14,
            textColor=BRAND_DARK,
            fontName="Helvetica-Bold",
        ),
    }


def _build_summary_table(topics, styles):
    total_subtopics = sum(len(t.get("subtopics", [])) for t in topics)
    total_concepts = sum(
        sum(len(st.get("concepts", [])) for st in t.get("subtopics", []))
        for t in topics
    )

    cells = [
        [
            Paragraph("TOPICS", styles["summary_label"]),
            Paragraph("SUBTOPICS", styles["summary_label"]),
            Paragraph("CONCEPTS", styles["summary_label"]),
        ],
        [
            Paragraph(str(len(topics)), styles["summary_value"]),
            Paragraph(str(total_subtopics), styles["summary_value"]),
            Paragraph(str(total_concepts), styles["summary_value"]),
        ],
    ]

    col_w = (PAGE_W - 100) / 3
    table = Table(cells, colWidths=[col_w] * 3, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BRAND_LIGHT_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, BRAND_BORDER),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, BRAND_BORDER),
                ("TOPPADDING", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 2),
                ("TOPPADDING", (0, 1), (-1, 1), 2),
                ("BOTTOMPADDING", (0, 1), (-1, 1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ]
        )
    )
    return table


def _build_topic_banner(index, name):
    banner_data = [
        [
            Paragraph(
                f"<b>{index + 1}.</b>&nbsp;&nbsp;{name}",
                ParagraphStyle(
                    "BannerText",
                    fontSize=14,
                    leading=18,
                    textColor=white,
                    fontName="Helvetica-Bold",
                    leftIndent=4,
                ),
            )
        ]
    ]
    banner_w = PAGE_W - 100
    banner = Table(banner_data, colWidths=[banner_w], hAlign="LEFT")
    banner.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), BRAND_PRIMARY),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                ("LEFTPADDING", (0, 0), (-1, -1), 16),
                ("ROUNDEDCORNERS", [6, 6, 6, 6]),
            ]
        )
    )
    return banner


def _build_subtopic_section(topic_idx, sub_idx, subtopic, styles):
    elements = []
    sub_name = subtopic.get("name", f"Subtopic {sub_idx + 1}")
    elements.append(
        Paragraph(
            f"{topic_idx + 1}.{sub_idx + 1}&nbsp;&nbsp;{sub_name}",
            styles["subtopic"],
        )
    )

    concepts = subtopic.get("concepts", [])
    if concepts:
        concept_rows = []
        for concept in concepts:
            c = concept if isinstance(concept, str) else str(concept)
            concept_rows.append(
                [
                    Paragraph(
                        f'<font color="#6366F1">\u2022</font>&nbsp;&nbsp;{c}',
                        styles["concept"],
                    )
                ]
            )

        concept_w = PAGE_W - 130
        concept_table = Table(concept_rows, colWidths=[concept_w], hAlign="LEFT")
        concept_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, -1), BRAND_CONCEPT_BG),
                    ("TOPPADDING", (0, 0), (-1, -1), 4),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                    ("LEFTPADDING", (0, 0), (-1, -1), 16),
                    ("ROUNDEDCORNERS", [4, 4, 4, 4]),
                    ("BOX", (0, 0), (-1, -1), 0.3, BRAND_BORDER),
                ]
            )
        )
        elements.append(concept_table)

    return elements


def generate_pdf(topics: list, title: str = "Syllabus Topic Structure") -> bytes:
    """Generate a branded, styled PDF from structured topic data. Returns PDF bytes."""
    logger.info(f"Generating PDF for {len(topics)} topics")

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=50,
        leftMargin=50,
        topMargin=65,
        bottomMargin=55,
    )

    styles = _build_styles()
    elements = []

    elements.append(Spacer(1, 8))
    elements.append(Paragraph(title, styles["title"]))

    ts_str = datetime.now().strftime("%B %d, %Y")
    elements.append(
        Paragraph(f"Generated on {ts_str}", styles["subtitle"])
    )

    elements.append(_build_summary_table(topics, styles))
    elements.append(Spacer(1, 20))

    elements.append(
        HRFlowable(width="100%", thickness=0.5, color=BRAND_BORDER, spaceAfter=12)
    )

    for i, topic in enumerate(topics):
        topic_name = topic.get("name", f"Topic {i + 1}")

        topic_elements = []
        topic_elements.append(_build_topic_banner(i, topic_name))
        topic_elements.append(Spacer(1, 4))

        subtopics = topic.get("subtopics", [])
        for j, subtopic in enumerate(subtopics):
            sub_els = _build_subtopic_section(i, j, subtopic, styles)
            topic_elements.extend(sub_els)
            topic_elements.append(Spacer(1, 6))

        topic_elements.append(Spacer(1, 10))

        if len(subtopics) <= 3:
            elements.append(KeepTogether(topic_elements))
        else:
            elements.extend(topic_elements)

    doc.build(
        elements,
        onFirstPage=_draw_header_footer,
        onLaterPages=_draw_header_footer,
    )
    pdf_bytes = buffer.getvalue()
    logger.info(f"PDF generated: {len(pdf_bytes)} bytes")
    return pdf_bytes
