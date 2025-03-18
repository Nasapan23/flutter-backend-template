from typing import List
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Flutter Backend API"
    PROJECT_DESCRIPTION: str = "Backend API for Flutter applications with AI capabilities"
    PROJECT_VERSION: str = "0.1.0"
    API_PREFIX: str = "/api"
    
    # Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecretkey")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Vite default
        "http://localhost:8000",  # Frontend
        "http://localhost:5173",  # Another Vite default
        "capacitor://localhost",  # Mobile app
        "http://localhost"
    ]
    
    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")
    
    # AI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    DEFAULT_LLM_MODEL: str = "gpt-3.5-turbo"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", case_sensitive=True)


# Create global settings instance
settings = Settings() 