import os
from typing import Optional

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    """Application settings."""

    API_VERSION: str = os.getenv("API_VERSION", "0.1.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    MONGODB_URL: str = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
    MONGODB_DB_NAME: str = os.getenv("MONGODB_DB_NAME", "fastapi_db")

    class Config:
        case_sensitive = True


settings = Settings()
