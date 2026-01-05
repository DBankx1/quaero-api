from fastapi import APIRouter

from app.api.routes import businesses, categories

api_router = APIRouter()
api_router.include_router(businesses.router)
api_router.include_router(categories.router)
