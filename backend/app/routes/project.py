from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)

from app.services.project_service import ProjectService

project_bp = Blueprint(
    "project",
    __name__,
    url_prefix="/api/v1/projects",
)


@project_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload_project():

    user_id = int(get_jwt_identity())

    file = request.files.get("file")

    result, error = ProjectService.upload_project(
        file=file,
        user_id=user_id,
    )

    if error:
        return {
            "message": error
        }, 400

    return {
        "message": "Project uploaded successfully",
        "data": result,
    }, 200