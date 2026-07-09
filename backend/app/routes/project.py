from flask import Blueprint, request

from app.services.project_service import ProjectService

project_bp = Blueprint(
    "project",
    __name__,
    url_prefix="/api/v1/projects"
)


@project_bp.route("/upload", methods=["POST"])
def upload_project():

    file = request.files.get("file")

    result, error = ProjectService.upload_project(file)

    if error:
        return {"message": error}, 400

    return {
        "message": "Project uploaded successfully",
        "data": result
    }, 200