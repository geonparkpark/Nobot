from ytsearch import search_id_yt, get_streamingdata
from redis_API import RedisClient
import aiohttp
import io

redis_client = RedisClient()

async def setup_redis():
    await redis_client.connect()

async def close_redis():
    await redis_client.close()

def is_yt_link(query):
    return query.startswith("http") and "youtube.com" in query

    # 사용하지 않음
# async def is_valid_url(url):
#     async with aiohttp.ClientSession() as session:
#         async with session.head(url) as response:
#             return response.status == 200

async def audio_stream(url: str) -> io.BytesIO | None:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return None
                raw_data = await response.read()
                return io.BytesIO(raw_data)

    except Exception as e:
        print(f"[get_audio_stream_if_valid] 에러: {e}")
        return None

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
        data = await get_streamingdata(v_id)
        await redis_client.hset(f'video:{v_id}', data)

    return data

async def search_music_data(query):
    v_id = await get_v_id(query)
    data = await get_data(v_id)

    # audio = await audio_stream(data['url'])
    # data['audio'] = audio
    # data.pop('url')
    data['id'] = v_id

    return data