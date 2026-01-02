import logging
import uuid
from agents import Runner, trace
from app.background.tasks.business_ingestion import ingest_businesses_from_search
from app.infrastructure.agents.business_agents import business_searcher_agent
from app.model.dto.business_search_dto import BusinessSearchDto
from fastapi import BackgroundTasks

logger = logging.getLogger(__name__)

async def search_businesses(query: str, background_tasks: BackgroundTasks) -> BusinessSearchDto:
    """
    search for businesses based on given query
    """
    
    try:
        with trace("Business search"):
            result = await Runner.run(business_searcher_agent, query)
            businesses = result.final_output
            
        background_task_id = str(uuid.uuid4())
        background_tasks.add_task(ingest_businesses_from_search, background_task_id, businesses.results)
        
        return businesses
    except Exception as e:
        logger.error(f"searching businesses with query: {query} failed with error: {e}")
        raise e
    