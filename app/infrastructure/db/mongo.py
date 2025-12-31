from pymongo import MongoClient
from app.core.config import settings

mongo_client = MongoClient(settings.MONGODB_CONNECTION)