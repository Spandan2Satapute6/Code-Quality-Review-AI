from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from app.services.code_review_service import CodeReviewService

code_bp = Blueprint(
    "code",
    __name__,
    url_prefix="/api/v1/code",
)


@code_bp.route("/review", methods=["POST"])
@jwt_required()
def review_code():

    data = request.get_json()

    if not data:
        return {
            "message": "Request body is required"
        }, 400

    code = data.get("code", "").strip()
    language = data.get("language", "python")

    if not code:
        return {
            "message": "Code is required"
        }, 400

    try:
        report = CodeReviewService.review_code(
            code=code,
            language=language,
        )

        return {
            "message": "Code reviewed successfully",
            "data": report,
        }, 200

    except Exception as e:
        return {
            "message": str(e)
        }, 500