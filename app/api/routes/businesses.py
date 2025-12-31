from typing import List
from fastapi import APIRouter

router = APIRouter(tags=["businesses"])

@router.get("/")
async def search(search: str) -> List:
    return []