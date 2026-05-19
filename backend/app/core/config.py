from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App
    APP_NAME: str = "MindPath Career Mentor API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "postgresql://postgres:password@localhost:5432/mindpath_db"

    # CORS
    ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "https://mindpathmentor.com",
    ]

    # WhatsApp
    WHATSAPP_NUMBER: str = "919666889722"

    # Admin
    ADMIN_SECRET_KEY: str = "change-this-in-production"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
