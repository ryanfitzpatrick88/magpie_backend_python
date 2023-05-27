import os
from typing import List
from pydantic import BaseSettings, AnyHttpUrl
from datetime import timedelta
from dotenv import load_dotenv

class Settings(BaseSettings):
    load_dotenv("../.env.local")

    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Magpie")
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.0.1")

    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    ALLOWED_ORIGINS: List[str] = os.getenv("ALLOWED_ORIGINS", ["*"])

    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///../database/app.db")

    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 1))  # Set the expiration time in minutes
    ACCESS_TOKEN_EXPIRE_TIMEDELTA: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # Create a timedelta object

    REFRESH_TOKEN_EXPIRE_HOURS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_HOURS", 8))
    REFRESH_TOKEN_EXPIRE_TIMEDELTA: timedelta = timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)

    SECRET_KEY: str = os.getenv("SECRET_KEY", "i-have-approximate-knowledge-of-many-things")  # Set your secret key here
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")  # Set your algorithm here

    REFRESH_SECRET_KEY: str = os.getenv("REFRESH_SECRET_KEY", "i-also-have-approximate-knowledge-of-many-things")

    class Config:
        case_sensitive = True


settings = Settings()
