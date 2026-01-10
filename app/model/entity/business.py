from typing import Annotated
from pydantic import BaseModel, Field
from beanie import Document, Indexed

class BusinessAddress(BaseModel):
    street: str | None = Field(description="Street address of the business.")
    city: str | None = Field(description="City of the business.")
    state: str | None = Field(description="State of the business.")
    post_code: str | None = Field(description="Zip code of the business.")
    country: str = Field(description="Country of the business.")

class Business(Document):
    name: Annotated[str, Indexed()] = Field(description="Name of the business found.") 
    address: BusinessAddress = Field(description="Address of the business found. This field is required and every business should have an address")
    logo: str | None = Field(description="Logo URL of the business found.", default=None)
    description: str | None = Field(description="Description of the business and its function", default=None)
    siteUrl: str | None = Field(description="Website of the business found.", default=None)
    phone: str | None = Field(description="Phone number of the business found.", default=None)
    email: str | None = Field(description="Email of the business found.", default=None)
    rating: float | None = Field(description="Rating of the business based on testimonials and reviews you can find. The rating should be between 0.0 and 5.0", default=0.0)
    is_online_shop: bool = Field(description="Whether the business is an online shop or not", default=False)
    category_slugs: Annotated[list[str], Indexed()] = Field(description="The slugs of the categories that the business belongs to", default_factory=list)
    
    class Settings:
        name = "businesses"