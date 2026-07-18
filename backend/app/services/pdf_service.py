from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
)
from reportlab.lib.units import inch


class PDFService:

    @staticmethod
    def generate_report(report):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        dashboard = report.get("dashboard", {})
        summary = report.get("project_summary", {})

        elements.append(
            Paragraph(
                "<b>AI Code Review Report</b>",
                styles["Title"],
            )
        )

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(
            Paragraph(
                f"<b>Project :</b> {report.get('project_name','')}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"<b>Overall Score :</b> {dashboard.get('overall_score',0)}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"<b>Average Score :</b> {dashboard.get('average_score',0)}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"<b>Security Issues :</b> {dashboard.get('security_issues',0)}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"<b>Maintainability Issues :</b> {dashboard.get('maintainability_issues',0)}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(
                f"<b>Performance Issues :</b> {dashboard.get('performance_issues',0)}",
                styles["Normal"],
            )
        )

        elements.append(Spacer(1, 0.3 * inch))

        elements.append(
            Paragraph(
                "<b>AI Project Summary</b>",
                styles["Heading2"],
            )
        )

        elements.append(
            Paragraph(
                summary.get("overall_summary", ""),
                styles["BodyText"],
            )
        )

        doc.build(elements)

        pdf = buffer.getvalue()

        buffer.close()

        return pdf