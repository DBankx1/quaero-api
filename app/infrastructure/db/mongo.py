from beanie import init_beanie
from pymongo import AsyncMongoClient
from app.core.config import settings
from app.model.entity.business import Business


async def init_db():
    global client
    client = AsyncMongoClient(settings.MONGODB_CONNECTION)
    await init_beanie(database=client[settings.MONGODB_CORE_COLLECTION], document_models=[Business])
    
async def close_db():
    if client:
        await client.close()