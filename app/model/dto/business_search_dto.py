from pydantic import BaseModel, Field
from app.model.entity.business import Business

class BusinessSearchDto(BaseModel):
    results: list[Business] = Field(description="List of businesses found.")
    total_count: int = Field(description="Total number of businesses found")
    

class BusinessSearchValidation(BaseModel):
    search_result_index: int
    business_name: str = Field(description="Name of the business from search")
    status: str = Field(description="new|duplicate|needs_review")
    duplicate_of_id: str | None = Field(description="database_id or null")
    match_confidence: float = Field(description="0.0 - 1.0 confidence of match", max_digits=1, decimal_places=1)
    match_reason: list[str] = Field(description="array of reasons why it matched")
    recommended_action: str = Field(description="insert|skip|manual_review|update_existing")
    data_quality_score: float = Field(description="0.0 - 1.0 score of data quality", max_digits=1, decimal_places=1)
    data_quality_issues: list[str] = Field(description="array of data quality issues or empty array if no issues")

class BusinessSearchValidationSummary(BaseModel):
    total_processed: int
    new_businesses: int
    duplicates: int
    needs_review: int
   
class BusinessSearchValidationResultDto(BaseModel):
    validation_results: list[BusinessSearchValidation]
    summary: BusinessSearchValidationSummary 
    

    