from fastapi import APIRouter
from app.core.config import settings
from app.api.v1.router import api_router as api_v1_router

# Main API router
router = APIRouter(prefix=settings.API_PREFIX)

# Include API version routers
router.include_router(api_v1_router, prefix="/v1")

# Health check endpoint
@router.get("/health")
async def health_check():
    """
    Health check endpoint to verify the API is working
    """
    return {"status": "ok", "version": settings.PROJECT_VERSION} 