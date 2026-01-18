from typing import Optional
from agents import Agent, WebSearchTool, handoff, function_tool
from app.core.config import settings
from app.infrastructure.repository.category_repository import get_categories_by_keywords
from app.model.dto.business_search_dto import BusinessLogoDto, BusinessSearchDto
from app.infrastructure.agents.prompts import business_searcher_agent_instructions, business_data_validator_instructions
from app.infrastructure.repository.business_repository import create_many_businesses, get_businesses_by_list_of_names
from app.model.entity.business import Business
from app.utils.brand_logo_builder import BrandLogoBuilder

# TOOLS -----------------------------------------------------------------------
@function_tool
async def create_businesses(businesses: list[Business]):
    await create_many_businesses(businesses)
    
@function_tool
async def get_businesses_by_names(business_names: list[str]) -> list[Business]:
    return await get_businesses_by_list_of_names(business_names)

@function_tool
async def get_relevant_categories(keywords: list[str]):
    """Get the relevant categories for a business based on the keywords provided"""
    return await get_categories_by_keywords(keywords, 30)

@function_tool
async def get_businesses_logos(business_urls: list[str]) -> dict[str, Optional[str]]:
    """Get the logo URL for a business from its website link"""
    builder = BrandLogoBuilder(settings.BRAND_FETCH_CLIENT_ID)
    return builder.build_logo_urls_batch(business_urls)


business_searcher_agent = Agent(
    name="Business Searcher",
    instructions=business_searcher_agent_instructions,
    model=settings.APP_DEFAULT_MODEL,
    tools=[get_relevant_categories, WebSearchTool(search_context_size="high"), get_businesses_logos],
    output_type=BusinessSearchDto
)


business_data_validation_agent = Agent(
    name="Business Data Validator",
    instructions=business_data_validator_instructions,
    model=settings.APP_DEFAULT_MODEL,
    tools=[WebSearchTool(search_context_size="high")],
    output_type=list[Business]
)
