from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
import os


class Settings(BaseSettings):
    AUTH0_DOMAIN: Optional[str] = None
    AUTH0_API_AUDIENCE: Optional[str] = None
    AUTH0_ALGORITHM: Optional[str] = None
    AUTH0_ISSUER: Optional[str] = None
    AUTH0_TOKEN: Optional[str] = None
    
    DATABASE_URL: str = "postgresql://user:password@localhost/dbname"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()