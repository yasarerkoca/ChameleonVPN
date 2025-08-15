# app.events.shutdown_events.py

from fastapi import FastAPI
from app.config.redis import close_redis_connection
from app.logs.logger import shutdown_logger

def register_shutdown_events(app: FastAPI):
    @app.on_event("shutdown")
    async def on_shutdown():
        await close_redis_connection()
        shutdown_logger()
        print("🛑 Uygulama kapatılıyor.")
