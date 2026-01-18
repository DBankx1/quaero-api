from app.model.entity.business import Business
import json


def businesses_to_json(businesses: list[Business]) -> str:
    """Convert a list of businesses to a JSON string"""
    
    business_dicts = [
        business.model_dump(exclude={'id', 'revision_id'}) for business in businesses
    ]
    
    return json.dumps(business_dicts, indent=2)