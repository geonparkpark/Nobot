import os
import redis
from ytsearch import search_id_yt
from ytdownload import get_yturl
import requests

def is_yt_link(query):
    return query.startswith("http") and "youtube.com" in query

def search_id_server(query):
    r = redis.Redis(host='localhost', port=6379, db=0)
    v_id = r.get(query)
    r.close()
    return v_id

def search_link_server(v_id):
    r = redis.Redis(host='localhost', port=6379, db=0)
    link = r.get(v_id)
    r.close()
    return link

def insert_search_id(key, v_id):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(key, v_id)
    r.close()

def insert_id_link(v_id, link):
    r = redis.Redis(host='localhost', port=6379, db=0)
    r.set(v_id, link)
    r.close()

def get_v_id(query):
    if is_yt_link(query):
        v_id = query.split('watch?v=')[-1].split('?')[0]
    else:
        key_db = ''.join(sorted(query.split()))
        v_id = search_id_server(key_db)
        if v_id:
            v_id = v_id.decode('utf-8')
        else:
            v_id = search_id_yt(query)
            insert_search_id(key_db, v_id)

    return v_id

def get_url(v_id):
    url = search_link_server(v_id)
    if url:
        url = url.decode('utf-8')
    else:
        url = get_yturl(v_id)
        insert_id_link(v_id, url)

    return url

def search_url(query):
    v_id = get_v_id(query)
    url = get_url(v_id)

        # url 만료되었으면 갱신
    response = requests.head(url)
    if response.status_code != 200:
        url = get_yturl(v_id)
        insert_id_link(v_id, url)

    return url