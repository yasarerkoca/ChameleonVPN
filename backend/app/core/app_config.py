# app/core/app_config.py
from pydantic import BaseSettings

class AppConfig(BaseSettings):
    PROJECT_NAME: str = "ChameleonVPN"
    DEBUG: bool = True
    VERSION: str = "1.0.0"

    class Config:
        env_file = ".env"

config = AppConfig()
