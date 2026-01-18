from pydantic import BaseModel, Field
from app.model.entity.business import Business

class BusinessSearchDto(BaseModel):
    results: list[Business] = Field(description="List of businesses found.")
    total_count: int = Field(description="Total number of businesses found")
    

class BusinessLogoDto(BaseModel):
    business_name: str = Field(description="Name of the original business.")
    business_url: str = Field(description="URL of the original business.")
    logo_url: str = Field(description="URL of the logo.")
    

    