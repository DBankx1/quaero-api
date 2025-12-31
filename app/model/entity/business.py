from pydantic import BaseModel, Field
from beanie import Document

class BusinessAddress(BaseModel):
    street: str | None = Field(description="Street address of the business.")
    city: str | None = Field(description="City of the business.")
    state: str | None = Field(description="State of the business.")
    post_code: str | None = Field(description="Zip code of the business.")
    country: str = Field(description="Country of the business.")

class Business(Document):
    name: str = Field(description="Name of the business found.")
    address: BusinessAddress = Field(description="Address of the business found. This field is required and every business should have an address")
    siteUrl: str | None = Field(description="Website of the business found.", default=None)
    phone: str | None = Field(description="Phone number of the business found.", default=None)
    email: str | None = Field(description="Email of the business found.", default=None)
    rating: int | None = Field(description="Rating of the business based on testimonials and reviews you can find. The rating should be between 0 and 5", default=0)
    
    class Settings:
        name = "businesses"