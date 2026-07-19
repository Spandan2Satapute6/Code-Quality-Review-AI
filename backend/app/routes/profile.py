from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.services.profile_service import ProfileService

profile_bp = Blueprint(
    "profile",
    __name__,
    url_prefix="/api/v1/profile",
)


@profile_bp.route("", methods=["GET"])
@jwt_required()
def get_profile():

    user_id = int(get_jwt_identity())

    profile, error = ProfileService.get_profile(user_id)

    if error:
        return {"message": error}, 404

    return profile, 200


@profile_bp.route("", methods=["PUT"])
@jwt_required()
def update_profile():

    user_id = int(get_jwt_identity())

    data = request.get_json()

    profile, error = ProfileService.update_profile(
        user_id=user_id,
        name=data["name"],
    )

    if error:
        return {"message": error}, 400

    return {
        "message": "Profile updated successfully",
        "data": profile,
    }, 200


@profile_bp.route("/password", methods=["PUT"])
@jwt_required()
def change_password():

    user_id = int(get_jwt_identity())

    data = request.get_json()

    error = ProfileService.change_password(
        user_id=user_id,
        old_password=data["old_password"],
        new_password=data["new_password"],
    )

    if error:
        return {"message": error}, 400

    return {
        "message": "Password updated successfully"
    }, 200