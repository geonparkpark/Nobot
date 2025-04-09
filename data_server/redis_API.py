import redis.asyncio as redis
from dotenv import load_dotenv
import os

load_dotenv()
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")

class RedisClient:
    def __init__(self):
        self.redis_client = None

    async def connect(self):
        if not self.redis_client:
            self.redis_client = await redis.from_url(f"redis://{REDIS_HOST}", port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
            print("Redis connected")
        else:
            print("Redis client already connected")

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()
            print("Redis closed")
        else:
            print("Redis not connected yet")

    async def get(self, key):
        return await self.redis_client.get(key)

    async def set(self, key, value, ex: int = 8640000):
        if key.startswith('search:'):
            await self.redis_client.set(key, value, ex=ex) # auto-delete after 100 days: 8,640,000

    async def hgetall(self, key):
        return await self.redis_client.hgetall(key)

    async def hset(self, key, mapping):
        if key.startswith('video:'):
            pipe = self.redis_client.pipeline()
            await pipe.hset(key, mapping=mapping)
            await pipe.expire(key, 21600) # auto-delete after 6 hours: 21600s
            await pipe.execute()
            # await self.redis_client.hset(key, mapping=mapping)

    async def pubsub(self):
        return self.redis_client.pubsub()