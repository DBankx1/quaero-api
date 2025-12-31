from contextlib import asynccontextmanager
from app.infrastructure.db.mongo import init_db, close_db
from app.core.logging import init_logging
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_logging()
    await init_db()
    yield
    await close_db()