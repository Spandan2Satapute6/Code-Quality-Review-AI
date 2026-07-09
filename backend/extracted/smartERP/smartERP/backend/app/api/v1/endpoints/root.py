"""Root endpoint for basic service discovery."""

from fastapi import APIRouter


router = APIRouter(tags=["System"])


@router.get("/", summary="Root endpoint")
def root() -> dict[str, str]:
    """Return a lightweight welcome payload for the API root."""

    return {
        "message": "SmartERP API is running",
        "docs": "/docs",
        "health": "/health",
    }