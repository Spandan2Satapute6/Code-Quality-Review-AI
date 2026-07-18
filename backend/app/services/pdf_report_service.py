from io import BytesIO
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.enums import TA_CENTER


def generate_pdf_report(review_data):
    """
    Generates a PDF report from AI review data.
    Returns a BytesIO object.
    """

    buffer = BytesIO()

    doc = SimpleDocTemplate(buffer)

    styles = getSampleStyleSheet()

    title = styles["Heading1"]
    title.alignment = TA_CENTER

    heading = styles["Heading2"]
    normal = styles["BodyText"]

    elements = []

    # Title
    elements.append(Paragraph("AI Code Review Report", title))
    elements.append(Spacer(1, 20))

    # Project Information
    project_name = review_data.get("project_name", "Unknown Project")
    score = review_data.get("overall_score", "N/A")
    summary = review_data.get("summary", "No summary available.")

    elements.append(Paragraph("<b>Project Information</b>", heading))
    elements.append(Paragraph(f"<b>Project:</b> {project_name}", normal))
    elements.append(Paragraph(f"<b>Overall Score:</b> {score}", normal))
    elements.append(Spacer(1, 12))

    # AI Summary
    elements.append(Paragraph("<b>AI Summary</b>", heading))
    elements.append(Paragraph(summary, normal))
    elements.append(Spacer(1, 20))

    # File Reviews
    reviews = review_data.get("review", [])

    elements.append(Paragraph("<b>File Reviews</b>", heading))
    elements.append(Spacer(1, 10))

    for file in reviews:

        filename = file.get("filename", "Unknown")
        severity = file.get("severity", "N/A")
        file_score = file.get("score", "N/A")
        review = file.get("review", "")

        elements.append(
            Paragraph(f"<b>{filename}</b>", styles["Heading3"])
        )

        elements.append(
            Paragraph(f"Score: {file_score}", normal)
        )

        elements.append(
            Paragraph(f"Severity: {severity}", normal)
        )

        elements.append(
            Paragraph(review, normal)
        )

        elements.append(Spacer(1, 15))

    doc.build(elements)

    buffer.seek(0)

    return buffer