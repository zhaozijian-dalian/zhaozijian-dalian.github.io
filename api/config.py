from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_SERVER: str = "localhost"
    DATABASE_NAME: str = "infection_control"
    DATABASE_USER: str = "sa"
    DATABASE_PASSWORD: str = "your_password"
    
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    
    API_PREFIX: str = "/api"
    
    class Config:
        env_file = ".env"

settings = Settings()

DATABASE_URL = f"mssql+pymssql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_SERVER}/{settings.DATABASE_NAME}"
