from motor.motor_asyncio import AsyncIOMotorClient
from ..core.config import settings

class MongoDB:
    client: AsyncIOMotorClient = None
    db = None
    
    @classmethod
    def get_db(cls):
        return cls.db
    
    @classmethod
    async def connect_to_mongodb(cls):
        cls.client = AsyncIOMotorClient(settings.MONGODB_URL)
        cls.db = cls.client[settings.MONGODB_DB_NAME]
    
    @classmethod
    async def close_mongodb_connection(cls):
        if cls.client:
            cls.client.close()

mongodb = MongoDB()