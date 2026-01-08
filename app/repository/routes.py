from app.routes.v1.admin.auth import router

from fastapi import APIRouter



# Configure the API router with version prefix
api_router = APIRouter(prefix="/v1")

# Include admin authentication routes
api_router.include_router(router)

