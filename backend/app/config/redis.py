import redis.asyncio as aioredis
from .base import settings
from typing import Optional

REDIS_URL = settings.REDIS_URL
redis: Optional[aioredis.Redis] = None

async def init_redis_connection():
    global redis
    redis = await aioredis.from_url(REDIS_URL, encoding="utf-8", decode_responses=True)

async def close_redis_connection():
    global redis
    if redis:
        await redis.close()
