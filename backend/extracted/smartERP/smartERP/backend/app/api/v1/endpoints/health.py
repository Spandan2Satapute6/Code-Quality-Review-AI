"""Health endpoint for service monitoring."""

from fastapi import APIRouter


router = APIRouter(tags=["Health"])


@router.get("/health", summary="Health check")
def health_check() -> dict[str, str]:
    """Return a simple service status response for monitoring tools."""

    return {"status": "ok"}