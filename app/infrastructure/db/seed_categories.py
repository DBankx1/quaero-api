import json
import logging

from app.model.entity.category import Category


logger = logging.getLogger(__name__)

async def seed_categories():
    """Seed categories in database"""
    try:
        logger.info("Seeding categories.......")
        with open("data/processed/categories.json", "r") as f:
            categories = json.load(f)
            
        for cat in categories:
            exists = await Category.find_one(Category.slug == cat["slug"])
            
            if not exists:
                await Category(**cat).insert()
                
        logger.info(f"Seeded {len(categories)} categories")
    except Exception as e:
        logger.error(f"Error seeding categories: {e}")