import redis.asyncio as redis
import os
import random

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")
REDIS_DB = os.getenv("REDIS_DB")
print(REDIS_HOST)
print(REDIS_PORT)
print(REDIS_DB)

# auto-delete after d days
d = 100
ex_id = 60 * 60 * 24 * d

# auto-delete after min hx hours max hy hours
hx, hy = 6, 24
ex_url_min = 60 * 60 * hx
ex_url_max = 60 * 60 * hy

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

        # 서버에 검색어 -> id 매핑 삽입
    async def set(self, key, value):
        if key.startswith('search:'):
            await self.redis_client.set(key, value, ex=ex_id)

    async def hgetall(self, key):
        return await self.redis_client.hgetall(key)

        # 서버에 id -> metadata 삽입
    async def hset(self, key, mapping):
        if key.startswith('video:'):
            ex_url = random.randint(ex_url_min, ex_url_max)
            pipe = self.redis_client.pipeline()
            await pipe.hset(key, mapping=mapping)
            await pipe.expire(key, ex_url)
            await pipe.execute()

    async def pubsub(self):
        return self.redis_client.pubsub()