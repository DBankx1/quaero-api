from typing import Literal, Optional

from fastapi import APIRouter, Query

from app.infrastructure.repository.category_repository import get_categories, get_categories_by_keywords
from app.model.dto.category_dto import CategoryResponseDto
from app.model.entity.category import Category

router = APIRouter(tags=["categories"], prefix="/categories")

@router.get("/", response_model=list[CategoryResponseDto])
async def list_categories(
    level: Optional[Literal["primary", "secondary", "tertiary"]] = None,
    limit: Optional[int] = Query(None, ge=1, le=500),
    offset: Optional[int] = Query(None, ge=0),
):
    
    return await get_categories(limit, offset, level)


@router.get("/keywords", response_model=list[CategoryResponseDto])
async def list_categories_by_keywords(
    keywords: str = Query(..., description="Comma-separated list of keywords to search for categories"),
    limit: int = Query(20, ge=1, le=500),
):
    keywords_list = [keyword.strip() for keyword in keywords.split(",")]
    return await get_categories_by_keywords(keywords_list, limit=limit)

