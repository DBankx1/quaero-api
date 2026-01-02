from agents import Agent, WebSearchTool, handoff, function_tool
from app.core.config import settings
from app.model.dto.business_search_dto import BusinessSearchDto, BusinessSearchValidationResultDto
from app.infrastructure.agents.prompts import business_searcher_agent_instructions, business_ingestion_tool_instructions, business_validation_tool_instruction
from app.infrastructure.repository.business_repository import create_many_businesses, get_businesses_by_list_of_names
from app.model.entity.business import Business

# TOOLS -----------------------------------------------------------------------
@function_tool
async def create_businesses(businesses: list[Business]):
    await create_many_businesses(businesses)
    
@function_tool
async def get_businesses_by_names(business_names: list[str]) -> list[Business]:
    return await get_businesses_by_list_of_names(business_names)

business_searcher_agent = Agent(
    name="Business Searcher",
    instructions=business_searcher_agent_instructions,
    model=settings.APP_DEFAULT_MODEL,
    tools=[WebSearchTool(search_context_size="high")],
    output_type=BusinessSearchDto
)

business_ingestion_agent = Agent(
    name="Business Ingestion Agent",
    instructions=business_ingestion_tool_instructions,
    model=settings.APP_DEFAULT_MODEL,
    tools=[create_businesses]
)

business_validation_agent = Agent(
    name="Business Validation Agent",
    instructions=business_validation_tool_instruction,
    model=settings.APP_DEFAULT_MODEL,
    tools=[get_businesses_by_names],
    handoffs=[business_ingestion_agent],
    output_type=BusinessSearchValidationResultDto
)