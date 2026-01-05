
from typing import Literal, Optional
from app.model.entity.category import Category


async def get_categories(limit:int | None, offset: int | None, level: Optional[Literal["primary", "secondary", "tertiary"]] = None):
    query = Category.find()

    if level:
        query = query.find(Category.level == level)

    if offset is not None:
        query = query.skip(offset)

    if limit is not None:
        query = query.limit(limit)

    return await query.to_list()

async def get_categories_by_keywords(keywords: list[str], limit: int = 20):
    should_clauses = []

    for keyword in keywords:
        should_clauses.append({
            "text": {
                "query": keyword,
                "path": ["name", "slug", "primary", "secondary"],
                "fuzzy": {
                    "maxEdits": 2,
                    "prefixLength": 1,
                    "maxExpansions": 50
                }
            }
        })

    pipeline = [
        {
            "$search": {
                "index": "categories_index",
                "compound": {
                    "should": should_clauses,
                    "minimumShouldMatch": 1
                }
            }
        },
        { "$limit": limit },
        {
            "$project": {
                "slug": 1,
                "name": 1,
                "level": 1,
                "primary": 1,
                "secondary": 1,
                "parent_slug": 1,
                "_id": 0
            }
        }
    ]
    
    return await Category.aggregate(pipeline).to_list()
    