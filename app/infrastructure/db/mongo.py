from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.core.config import settings
from app.infrastructure import db
from app.infrastructure.db.seed_categories import seed_categories
from app.model.entity.business import Business
from app.model.entity.category import Category

async def collection_exists(db, collection_name: str) -> bool:
    """Check if a collection exists in the database."""
    collection_names = await db.list_collection_names()
    return collection_name in collection_names

async def init_db():
    global client
    client = AsyncMongoClient(settings.MONGODB_CONNECTION)
    await init_beanie(database=client[settings.MONGODB_CORE_COLLECTION], document_models=[Business, Category])
    
    # Figure out how to seed categories once on startup of application 
    #await seed_categories()
    
async def close_db():
    if client:
        await client.close()