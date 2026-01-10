from app.model.entity.business import Business
from app.services import business
import asyncio

async def create_business(business: Business):
    """Create a business entity"""
    await business.create()
        
async def get_business_by_id(business_id: str) -> Business | None:
    """Gets a business entity by id"""
    business = await Business.get(business_id)
    return business


async def get_business_by_name(business_name: str, limit:int = 1, threshold_score: float = 1.0) -> list[Business]:
    """Gets a list of businesses by name"""
    
    businesses_found = []
    pipeline = [
        {
            "$search": {
                "index": "business_search_index",
                "text": {
                    "query": business_name,
                    "path": "name",
                    "fuzzy": {
                        "maxEdits": 2,
                        "prefixLength": 1,
                        "maxExpansions": 50
                    }
                }
            }
        },
        {"$limit": limit},
        {"$addFields": {"score": {"$meta": "searchScore"}}}
    ]
    
    results = await Business.aggregate(pipeline).to_list()
    
    for result in results:
        if result.get('score', 0) >= threshold_score:
            business_data = results[0].copy()
            business_data.pop('score', None)
            business_found = Business(**business_data)
            businesses_found.append(business_found)
    
    return businesses_found
    
async def get_businesses_by_list_of_names(business_names: list[str], threshold_score: float = 0.8) -> list[Business]:
    """Gets a list of businesses by list of names"""
    
    tasks = [get_business_by_name(business_name, threshold_score=threshold_score) for business_name in business_names]
    results = await asyncio.gather(*tasks)
    
    # flatten list of lists into single list
    businesses_found = [business for sublist in results for business in sublist]
    
    return businesses_found

async def create_many_businesses(businesses: list[Business]) -> list[str]:
    """Create many business entities"""
    business = await Business.insert_many(businesses)
    return business.inserted_ids

async def get_businesses_by_relevant_categories(keywords: list[str], limit: int = 20) -> list[Business]:
    """Gets a list of businesses by relevant categories"""
    should_clauses = []

    for kw in keywords:
        should_clauses.append({
            "autocomplete": {
                "query": kw,
                "path": "category_slugs",
                "fuzzy": {
                    "maxEdits": 2,
                    "prefixLength": 1
                }
            }
        })

    pipeline = [
        {
            "$search": {
                "index": "business_search_index",
                "compound": {
                    "should": should_clauses,
                    "minimumShouldMatch": 1
                }
            }
        },
        {"$limit": limit},
        {
            "$project": {
                "name": 1,
                "category_slugs": 1,
                "rating": 1,
                "address": 1,
                "siteUrl": 1,
                "phone": 1,
                "email": 1,
                "_id": 0
            }
        }
    ]
    
    businesses = await Business.aggregate(pipeline).to_list()

    return [Business(**business) for business in businesses]

async def get_count_of_businesses() -> int:
    """Gets the count of businessesn in the db"""
    return await Business.get_pymongo_collection().estimated_document_count()

     