from pydantic import BaseModel
from typing import Optional

class CategoryResponseDto(BaseModel):
    slug: str
    name: str
    level: str
    primary: str
    secondary: Optional[str]
    parent_slug: Optional[str]

    class Config:
        from_attributes = True