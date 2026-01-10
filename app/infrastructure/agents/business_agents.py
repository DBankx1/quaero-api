from agents import Agent, WebSearchTool, handoff, function_tool
from app.core.config import settings
from app.infrastructure.repository.category_repository import get_categories_by_keywords
from app.model.dto.business_search_dto import BusinessSearchDto
from app.infrastructure.agents.prompts import business_searcher_agent_instructions, business_data_validator_instructions
from app.infrastructure.repository.business_repository import create_many_businesses, get_businesses_by_list_of_names
from app.model.entity.business import Business

# TOOLS -----------------------------------------------------------------------
@function_tool
async def create_businesses(businesses: list[Business]):
    await create_many_businesses(businesses)
    
@function_tool
async def get_businesses_by_names(business_names: list[str]) -> list[Business]:
    return await get_businesses_by_list_of_names(business_names)

@function_tool
async def get_relevant_categories(keywords: list[str]):
    return await get_categories_by_keywords(keywords, 30)

business_searcher_agent = Agent(
    name="Business Searcher",
    instructions=business_searcher_agent_instructions,
    model=settings.APP_DEFAULT_MODEL,
    tools=[WebSearchTool(search_context_size="high"), get_relevant_categories],
    output_type=BusinessSearchDto
)


business_data_validation_agent = Agent(
    name="Business Data Validator",
    instructions=business_data_validator_instructions,
    model=settings.APP_DEFAULT_MODEL,
    tools=[WebSearchTool(search_context_size="high"), get_relevant_categories],
    output_type=list[Business]
)