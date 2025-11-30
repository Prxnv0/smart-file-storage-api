from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", summary="Health check")
async def health_check() -> dict:
    """Simple health check endpoint for uptime monitoring."""
    return {"status": "ok"}
