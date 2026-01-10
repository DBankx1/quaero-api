from urllib import response
from fastapi import APIRouter, BackgroundTasks, Query
from app.infrastructure.repository.business_repository import get_businesses_by_relevant_categories, get_count_of_businesses
from app.model.dto.business_search_dto import BusinessSearchDto
from app.model.entity.business import Business
from app.services.business.search import search_businesses

router = APIRouter(tags=["businesses"], prefix="/businesses")

# TODO: add caching and pagination
@router.get("/search", response_model=BusinessSearchDto)
async def search(s: str, background_tasks: BackgroundTasks):
    result = await search_businesses(s, background_tasks)
    return result


@router.get("/search/categories", response_model=list[Business])
async def search_businesses_by_categories(
    category: list[str] = Query(..., description="List of category slugs to search for businesses"),
    limit: int = Query(20, ge=1, le=500)):
    return await get_businesses_by_relevant_categories(category, limit)

@router.get("/count", response_model=int)
async def get_indexed_businesses_count():
    return await get_count_of_businesses()