from app.infrastructure import db
from app.infrastructure.repository.business_repository import create_many_businesses, get_businesses_by_list_of_names
from app.model.entity.business import Business
import logging
from beanie import BulkWriter
from agents import Runner, trace
from app.infrastructure.agents.business_agents import business_data_validation_agent
import json

from app.services import business

logger = logging.getLogger(__name__)

async def ingest_businesses_from_search(task_id: str, businesses_from_search: list[Business]):
    """
    Adds businesses found from web AI search into database
    """
    try:
        logger.info(f"Starting ingestion task {task_id} with {len(businesses_from_search)} businesses")
        
        if not businesses_from_search:
            logger.info(f"Ingestion task {task_id} completed with 0 new businesses")
            return
        
        new_businesses = []
        
        business_names: list[str] = [business.name for business in businesses_from_search]
        
        db_matches: list[Business] = await get_businesses_by_list_of_names(business_names, threshold_score=0.8)
        
        if len(db_matches) > 0:
            existing_names = {
                biz.name.lower().strip() for biz in db_matches
            }
            
            new_businesses = [
                business
                for business in businesses_from_search
                if business.name.lower().strip() not in existing_names
            ]
            
            await update_existing_businesses(businesses_from_search, db_matches)
        else:
            new_businesses = businesses_from_search
        
        if len(new_businesses) > 0:
           with trace("Business validation"):
               result = await Runner.run(business_data_validation_agent, [
                    {
                        "role": "user",
                        "content": biz.model_dump_json(),
                    }
                    for biz in new_businesses
                ])
               
        await create_many_businesses(result.final_output)
            
        
        logger.info(f"Ingestion task {task_id} completed with {len(new_businesses)} new businesses, and {len(db_matches)} updated businesses")
           
    except Exception as e:
        logger.error(f"Error during ingestion task {task_id}: {e}")
        


async def update_existing_businesses(businesses_from_search: list[Business], db_matches: list[Business]):
    """Update existing businesses from search with new tags found"""
    
    if not businesses_from_search or not db_matches:
        return

    # Index search businesses by normalized name
    search_index: dict[str, set[str]] = {}

    for biz in businesses_from_search:
        if not biz.category_slugs:
            continue

        key = biz.name.strip().lower()
        search_index.setdefault(key, set()).update(biz.category_slugs)

    if not search_index:
        return

    async with BulkWriter() as bulk:
        for db_biz in db_matches:
            key = db_biz.name.strip().lower()

            incoming_tags = search_index.get(key)
            if not incoming_tags:
                continue

            existing_tags = set(db_biz.category_slugs or [])
            merged_tags = existing_tags | incoming_tags

            # Skip DB write if nothing changes
            if merged_tags == existing_tags:
                continue

            db_biz.category_slugs = list(merged_tags)
            await db_biz.save(bulk_writer=bulk)