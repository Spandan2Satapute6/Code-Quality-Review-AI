from flask import Blueprint, request
from flask_jwt_extended import (
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


# ============================
# Forgot Password
# ============================

@auth_bp.route("/forgot-password", methods=["POST"])
def forgot_password():

    data = request.get_json()

    token, error = AuthService.forgot_password(
        data["email"]
    )

    if error:
        return {"message": error}, 404

    return {
        "message": "Reset token generated",
        "reset_token": token,
    }, 200


# ============================
# Reset Password
# ============================

@auth_bp.route("/reset-password", methods=["POST"])
def reset_password():

    data = request.get_json()

    error = AuthService.reset_password(
        data["token"],
        data["password"],
    )

    if error:
        return {"message": error}, 400

    return {
        "message": "Password reset successful"
    }, 200 



