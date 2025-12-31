from fastapi import FastAPI

from app.api.main import api_router
from app.core.config import settings
from app.core.logging import init_logging

init_logging()

app = FastAPI(
    title="Quaero",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
    )

app.include_router(api_router, prefix=settings.API_V1_STR)