from ytsearch import search_id_yt, get_streamingdata
from redis_API import RedisClient
import aiohttp

redis_client = RedisClient()

async def setup_redis():
    await redis_client.connect()

async def close_redis():
    await redis_client.close()

def is_yt_link(query):
    return query.startswith("http") and "youtube.com" in query

async def is_valid_url(url):
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as response:
            return response.status == 200

async def get_v_id(query):
    if is_yt_link(query):
        v_id = query.split('watch?v=')[-1].split('?')[0]
    else:
        key_db = ''.join(sorted(query.split()))
        v_id = await redis_client.get(f'search:{key_db}')
        if not v_id:
            v_id = await search_id_yt(query)
            await redis_client.set(f'search:{key_db}', v_id)

    return v_id

async def get_data(v_id):
    data = await redis_client.hgetall(f'video:{v_id}')
    if data:
        url = data['url']

            # streaming url 만료되었을 경우 새로 갱신
        if not await is_valid_url(url):
            data = await get_streamingdata(v_id)
            await redis_client.hset(f'video:{v_id}', data)

    else:
        data = await get_streamingdata(v_id)
        await redis_client.hset(f'video:{v_id}', data)

    return data

async def search_music_data(query):
    v_id = await get_v_id(query)
    data = await get_data(v_id)
    data['id'] = v_id

    return data