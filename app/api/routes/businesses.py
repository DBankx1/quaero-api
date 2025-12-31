from typing import List
from fastapi import APIRouter, BackgroundTasks

from app.model.dto.business_search_dto import BusinessSearchDto
from app.services.business.search import search_businesses

router = APIRouter(tags=["businesses"])

@router.get("/search")
async def search(s: str, background_tasks: BackgroundTasks) -> BusinessSearchDto:
    result = await search_businesses(s, background_tasks)
    return result