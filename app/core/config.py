from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application configuration settings.
    Values are loaded from environment variables.
    """

    # Database
    DATABASE_URL: str

    # JWT Settings
    SECRET_KEY: str  # Generate with: openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15  # Short-lived JWT
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30    # Long-lived refresh token

    # Discord OAuth
    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str = "http%3A%2F%2F127.0.0.1%3A8000%2Fauth%2Fdiscord%2Fcallback" # e.g., http://localhost:8000/auth/discord/callback
    BOT_JWT: str

    # Application
    API_URL: str = "http://localhost:8000"

    # Feature specific configurations
    MIN_HABITS_REQUIRED_TO_START_CYCLE: int = 3
    

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
