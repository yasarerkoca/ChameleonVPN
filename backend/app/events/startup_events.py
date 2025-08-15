# app.events.startup_events.py

from fastapi import FastAPI
from app.logs.logger import init_logger
from app.config.database import init_db
from app.config.redis import init_redis_connection

def register_startup_events(app: FastAPI):
    @app.on_event("startup")
    async def on_startup():
        init_logger()
        init_db()
        await init_redis_connection()
        print("✅ Uygulama başlatıldı.")
