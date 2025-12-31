from app.model.entity.business import Business
from agents import function_tool

@function_tool 
async def create_business(business: Business):
    """Create a business entity"""
    await business.create()
        
async def get_business_by_id(business_id: str) -> Business | None:
    """Gets a business entity by id"""
    business = await Business.get(business_id)
    return business

@function_tool
async def get_businesses_by_name(business_name: str) -> list[Business]:
    """Gets a list of businesses by name"""
    regex_pattern = f".*{business_name}.*"
    businesses = await Business.find({"name": {"$regex": regex_pattern, "$options": "i"}}).to_list()
    return businesses
    
@function_tool
async def get_businesses_by_list_of_names(business_names: list[str]) -> list[Business]:
    """Gets a list of businesses by list of names"""
    regex_filters = [{"name": {"$regex": sub, "$options": "i"}} for sub in business_names]
    cursor = Business.find({"$or": regex_filters})
    return await cursor.to_list()

@function_tool
async def create_many_businesses(businesses: list[Business]):
    """Create many business entities"""
    await Business.insert_many(businesses)