import os
import time
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

load_dotenv()
YTAPI_KEY = os.getenv("YTAPI_KEY")
print(f'YTAPI_KEY: {YTAPI_KEY}')

YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'
yt = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=YTAPI_KEY)

#query = 'The Weeknd - Open Hearts (Single Version) (Audio)'
def search_id_yt(query):
    start_time = time.time()
    query = query.replace(' ', '+')
    search_response = yt.search()\
                        .list(q=query,
                              part='snippet',
                              maxResults=1)\
                        .execute()
    elapsed = time.time() - start_time
    print(f'yt_api Search: {elapsed:.6f}초 소요')
    return search_response['items'][0]['id']['videoId'] if search_response else None

#search_id_yt(query)