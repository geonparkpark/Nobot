import redis.asyncio as redis

class RedisClient:
    def __init__(self, redis_url="redis://localhost"):
        self.redis_url = redis_url
        self.redis_client = None

    async def connect(self):
        if not self.redis_client:
            self.redis_client = await redis.from_url(self.redis_url, port=6379, db=0, decode_responses=True)
            print("Redis 연결 성공")
        else:
            print("Redis 클라이언트가 이미 연결됨")

    async def close(self):
        if self.redis_client:
            await self.redis_client.close()
            print("Redis 연결 종료")
        else:
            print("Redis 클라이언트가 연결되지 않음")

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