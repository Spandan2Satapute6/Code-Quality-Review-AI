from flask import Blueprint, send_file
from flask_jwt_extended import jwt_required
from io import BytesIO

from app.models.review import Review
from app.services.pdf_service import PDFService

report_bp = Blueprint(
    "report",
    __name__,
    url_prefix="/api/v1/report",
)


@report_bp.route("/<int:review_id>/pdf", methods=["GET"])
@jwt_required()
def download_pdf(review_id):

    review = Review.query.get(review_id)

    if review is None:
        return {
            "message": "Review not found"
        }, 404

    pdf = PDFService.generate_report(
        review.report_json
    )

    return send_file(
        BytesIO(pdf),
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"review_{review_id}.pdf",
    )