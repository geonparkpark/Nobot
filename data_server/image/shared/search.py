from redis_API import RedisClient
from ytsearch import search_id_yt, get_streamingdata

redis_client = RedisClient()

    # ** lifespan 이벤트에서만 사용 **
async def setup_redis():
    await redis_client.connect()

def is_yt_link(query):
    return query.startswith("http") and "youtube.com" in query

async def push_data(v_id):
    data = await get_streamingdata(v_id)
    await redis_client.hset(f'video:{v_id}', data)

    return data

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
    if not data:
        data = await push_data(v_id)

    return data

async def search_music_data(query):
    v_id = await get_v_id(query)
    data = await get_data(v_id)
    data['id'] = v_id

    return data