from redis_API import RedisClient
from ytsearch import get_streamingdata
import asyncio

redis_client = RedisClient()

async def event_listener():
    await redis_client.connect()
    pubsub = await redis_client.pubsub()

    await pubsub.psubscribe("__keyevent@0__:expired")  # DB 0

    print("Listening for expired events...")

    async for message in pubsub.listen():
        if message and message["type"] == "pmessage":
            try:
                v_id = message["data"].split(':')[-1]
                data = await get_streamingdata(v_id)
                await redis_client.hset(f'video:{v_id}', data)
            except Exception as e:
                print(f'error with {e}')
                print(f'message: {message}')

asyncio.run(event_listener())