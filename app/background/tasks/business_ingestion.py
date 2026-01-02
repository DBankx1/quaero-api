from sympy import fu
from app.infrastructure.repository.business_repository import create_many_businesses, get_businesses_by_list_of_names
from app.model.entity.business import Business
import logging
from thefuzz import process, fuzz

from app.services import business

logger = logging.getLogger(__name__)

async def ingest_businesses_from_search(task_id: str, businesses_from_search: list[Business]):
    """
    Adds businesses found from web AI search into database
    """
    try:
        MATCH_THRESHOLD = 85
        
        new_businesses = []
        
        logger.info(f"Starting ingestion task {task_id} with {len(businesses_from_search)} businesses")
        
        business_names: list[str] = [business.name for business in businesses_from_search]
        
        businesses_in_db: list[Business] = await get_businesses_by_list_of_names(business_names)
        
        if len(businesses_in_db) > 0:
            for biz in businesses_from_search:
                db_biz_names = [business.name for business in businesses_in_db]
                print(db_biz_names)
                result = process.extractOne(biz.name, db_biz_names, scorer=fuzz.token_set_ratio)
                
                if result is None:
                    continue
                
                _, score, *_ = result
                print(f"{biz.name} - {_} - {score} when matching")
                
                if score < MATCH_THRESHOLD:
                    new_businesses.append(biz)
        else:
            new_businesses = businesses_from_search
        
        if len(new_businesses) > 0:        
            await create_many_businesses(new_businesses)
        
        logger.info(f"Ingestion task {task_id} completed with {len(new_businesses)} new businesses")
           
    except Exception as e:
        logger.error(f"Error during ingestion task {task_id}: {e}")
        
        