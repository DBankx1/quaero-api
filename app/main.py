from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.lifespan import lifespan

app = FastAPI(
    title="Quaero",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
    )

app.include_router(api_router, prefix=settings.API_V1_STR)