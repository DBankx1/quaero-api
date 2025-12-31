from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore"
    )
    
    API_V1_STR: str = "/api/v1"
    
    OPENAI_API_KEY: str
    
    MONGODB_CONNECTION: str
    
    
settings = Settings()  # type: ignore