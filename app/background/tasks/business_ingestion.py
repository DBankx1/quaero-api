from sympy import fu
from app.infrastructure import db
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
        else:
            new_businesses = businesses_from_search
        
        if len(new_businesses) > 0:        
            await create_many_businesses(new_businesses)
        
        logger.info(f"Ingestion task {task_id} completed with {len(new_businesses)} new businesses")
           
    except Exception as e:
        logger.error(f"Error during ingestion task {task_id}: {e}")
        
        