from beanie import Document, Indexed
from typing import Annotated, Optional, Literal
from pydantic import Field

CategoryLevel = Literal["primary", "secondary", "tertiary"]

class Category(Document):
    slug: Annotated[str, Indexed(str, unique=True)]
    name: str

    level: CategoryLevel

    primary: str
    secondary: Optional[str] = None

    parent_slug: Optional[str] = None

    class Settings:
        name = "categories"
        indexes = [
            "slug",
            "primary",
            "secondary",
            "level"
        ]
