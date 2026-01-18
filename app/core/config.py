from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    
    API_V1_STR: str = "/api/v1"
    
    OPENAI_API_KEY: str
    
    
    MONGODB_CONNECTION: str
    
    APP_DEFAULT_MODEL: str
    
    MONGODB_CORE_COLLECTION: str
    
    BRAND_FETCH_CLIENT_ID: str
    
    
settings = Settings()  # type: ignore

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY