import redis
from ytsearch import search_id_yt, get_streamingdata
import requests

def is_yt_link(query):
    return query.startswith("http") and "youtube.com" in query

def search_id_server(query):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    v_id = r.get(query)
    r.close()
    return v_id

def search_data_server(v_id):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    data = r.hgetall(v_id)
    r.close()
    return data

def insert_search_id(key, v_id):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.set(key, v_id)
    r.close()

def insert_id_data(v_id, data):
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    r.hset(v_id, mapping=data)
    r.close()

def get_v_id(query):
    if is_yt_link(query):
        v_id = query.split('watch?v=')[-1].split('?')[0]
    else:
        key_db = ''.join(sorted(query.split()))
        v_id = search_id_server(key_db)
        if not v_id:
            v_id = search_id_yt(query)
            insert_search_id(key_db, v_id)

    return v_id

def get_data(v_id):
    data = search_data_server(v_id)
    if data:
        url = data['url']

            # streaming url 만료되었을 경우 새로 갱신
        response = requests.head(url)
        if response.status_code != 200:
            data = get_streamingdata(v_id)
            insert_id_data(v_id, data)

    else:
        data = get_streamingdata(v_id)
        insert_id_data(v_id, data)

    return data

def search_music_data(query):
    v_id = get_v_id(query)
    data = get_data(v_id)

    return data