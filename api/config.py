from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 改用 SQLite 数据库，无需外部数据库
    DATABASE_URL: str = "sqlite:///./hospital_infection.db"
    JWT_SECRET_KEY: str = "your-secret-key-change-in-production-for-demo"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 480
    API_PREFIX: str = "/api"
    class Config:
        env_file = ".env"

settings = Settings()
