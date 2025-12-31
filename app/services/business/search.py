from http.client import INTERNAL_SERVER_ERROR
import logging
import re
import uuid
from agents import Runner, trace
from app.infrastructure.agents.business_agents import business_searcher_agent, business_ingestion_agent
from app.model.dto.business_search_dto import BusinessSearchDto
from fastapi import BackgroundTasks, HTTPException
import json


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
        background_tasks.add_task(_start_business_ingestion_background, background_task_id, result.final_output)
        
        return businesses
    except Exception as e:
        logger.error(f"searching businesses with query: {query} failed with error: {e}")
        raise e
    

# Private Functions ----------------------------------------------------------

async def _start_business_ingestion_background(background_task_id: str, business_search_result: BusinessSearchDto):
    """
    From search result, start ingestion of businesses into db
    """
    try:
        logger.info(f"starting ingestion of businesses with background task id: {background_task_id}")
        with trace("Business ingestion"):
            result = await Runner.run(business_ingestion_agent, business_search_result.model_dump_json())
            return result.final_output
    except Exception as e:
        logger.error(f"ingesting businesses failed with error: {e}")
        raise HTTPException(status_code=INTERNAL_SERVER_ERROR, detail=str(e))
        