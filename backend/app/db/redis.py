import redis.asyncio as redis
from ..core.config import settings

class RedisClient:
    def __init__(self):
        self.redis = None
    
    @classmethod
    async def connect_to_redis(cls):
        cls.redis = await redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            password=settings.REDIS_PASSWORD or None,
            encoding="utf-8",
            decode_responses=True
        )
    
    @classmethod
    async def close_redis_connection(cls):
        if cls.redis:
            await cls.redis.close()

redis_client = RedisClient()
