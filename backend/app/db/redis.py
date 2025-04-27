import redis.asyncio as redis
from ..core.config import settings

class RedisClient:
    def __init__(self):
        self.redis = None
    
    async def connect_to_redis(self):
        self.redis = await redis.from_url(
            f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}",
            password=settings.REDIS_PASSWORD or None,
            encoding="utf-8",
            decode_responses=True
        )
        print("Connected to Redis")
    
    async def close_redis_connection(self):
        if self.redis:
            await self.redis.close()
            print("Closed Redis connection")
    
    async def get_cache(self, key):
        return await self.redis.get(key)
    
    async def set_cache(self, key, value, ttl=3600):
        await self.redis.set(key, value, ex=ttl)

redis_client = RedisClient()
