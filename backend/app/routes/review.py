from flask import Blueprint
from flask_jwt_extended import jwt_required

from app.services.review_history_service import ReviewHistoryService

review_bp = Blueprint(
    "review",
    __name__,
    url_prefix="/api/v1/reviews",
)


@review_bp.route("", methods=["GET"])
@jwt_required()
def get_reviews():

    reviews = ReviewHistoryService.get_all_reviews()

    return {
        "message": "Reviews fetched successfully",
        "data": reviews,
    }, 200


@review_bp.route("/<int:review_id>", methods=["GET"])
@jwt_required()
def get_review(review_id):

    review = ReviewHistoryService.get_review(review_id)

    if review is None:
        return {
            "message": "Review not found"
        }, 404

    return {
        "message": "Review fetched successfully",
        "data": review,
    }, 200


@review_bp.route("/<int:review_id>", methods=["DELETE"])
@jwt_required()
def delete_review(review_id):

    deleted = ReviewHistoryService.delete_review(review_id)

    if not deleted:
        return {
            "message": "Review not found"
        }, 404

    return {
        "message": "Review deleted successfully"
    }, 200