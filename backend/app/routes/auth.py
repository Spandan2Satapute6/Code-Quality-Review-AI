from flask import Blueprint, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

from app.models.user import User
from app.services.auth_service import AuthService

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")


@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    user, error = AuthService.register(
        data["name"],
        data["email"],
        data["password"],
    )

    if error:
        return {"message": error}, 400

    return {
        "message": "User registered successfully",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
        },
    }, 201


@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    result, error = AuthService.login(
        data["email"],
        data["password"],
    )

    if error:
        return {"message": error}, 401

    return {
        "message": "Login successful",
        "data": result,
    }, 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():

    user_id = get_jwt_identity()

    user = User.query.get(int(user_id))

    if not user:
        return {"message": "User not found"}, 404

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }, 200