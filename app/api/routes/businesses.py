from fastapi import APIRouter, BackgroundTasks
from app.model.dto.business_search_dto import BusinessSearchDto
from app.services.business.search import search_businesses

router = APIRouter(tags=["businesses"])

# TODO: add caching and pagination
@router.get("/search", response_model=BusinessSearchDto)
async def search(s: str, background_tasks: BackgroundTasks):
    result = await search_businesses(s, background_tasks)
    return result
