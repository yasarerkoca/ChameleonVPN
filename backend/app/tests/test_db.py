import pytest
import asyncio
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from fastapi_limiter import FastAPILimiter
import redis.asyncio as aioredis
import os

from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config.database import Base, get_db

DATABASE_URL = os.environ["DATABASE_URL"]
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def _startup_limiter():
    redis_url = os.getenv("REDIS_URL", "redis://redis:6379")
    redis = await aioredis.from_url(redis_url, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
    yield

@pytest.fixture(scope="function")
async def client(_startup_limiter):
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as ac:
            yield ac
