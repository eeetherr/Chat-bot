from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    REDIS_URL: str = os.getenv("REDIS_URL")
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    CELERY_BROKER_URL: str = os.getenv("CELERY_BROKER_URL")
    class Config:
        env_file = ".env"

settings = Settings()
