# app/core/app_config.py
from pydantic import BaseSettings

class AppConfig(BaseSettings):
    PROJECT_NAME: str = "ChameleonVPN"
    DEBUG: bool = False  # Disabled by default; enable via env for development
    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

config = AppConfig()
