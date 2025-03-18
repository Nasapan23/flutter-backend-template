from fastapi import APIRouter
from app.api.v1.endpoints import users, auth, ai

# API v1 router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"]) 