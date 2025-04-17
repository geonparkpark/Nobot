import time
import yt_dlp
import asyncio

ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': '-',
    'extract_flat': True,
    'noplaylist': True,
    'skip_download': True,
    'force_generic_extractor': False,
    'extractor_args': {
        'youtube': {
            'skip': ['dash', 'translated_subs'],
            'player_client': ['tv']
            }
        },

    # 'http_headers': {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 11.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36',
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'Referer': 'https://www.youtube.com/',
    #     'Sec-Fetch-Mode': 'navigate'
    # },

    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (SmartTV; Linux; Tizen 6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
        'X-YouTube-Client-Name': '85',
        'X-YouTube-Client-Version': '7.20250409.08.00',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7'
    },

    #   for Android client
    # 'http_headers': {
    #     'User-Agent': 'com.google.android.youtube/18.12.37 (Linux; U; Android 12; en_US)',
    #     'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
    #     'X-YouTube-Client-Name': '21',
    #     'X-YouTube-Client-Version': '20.11.41'
    # },

    'verbose': True,
    'quiet': False,

    "no_cache_dir": True,
    "rm-cache-dir": True,
    }

async def search_id_yt(query):
    start_time = time.time()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        link = f'ytsearch1:{query} "auto-generated"'
        info = ydl.extract_info(link, download=False)
        print(info)

    elapsed = time.time() - start_time
    print(f'유튜브 id 검색: {elapsed:.6f}초 소요')

    url = info['entries'][0]['url'] if 'entries' in info else info['url']
    return url.split('watch?v=')[-1].split('?')[0]

async def get_streamingdata(v_id):
    start_time = time.time()

    with (yt_dlp.YoutubeDL(ydl_opts) as ydl):
        url = f'https://www.youtube.com/watch?v={v_id}'
        info = ydl.extract_info(url, download=False)
        data = {'artist': info.get('channel', 'Various Artists'),
                'title': info.get('title'),
                'url': info.get('url'),
                'thumbnail': info.get('thumbnail'),
                } if info else []

    elapsed = time.time() - start_time
    print(f'유튜브 스트리밍 url 추출: {elapsed:.6f}초 소요')

    return data

# v_id = asyncio.run(search_id_yt('sik k lov3'))
v_id = '7mjg-7ibaQA'
data = asyncio.run(get_streamingdata(v_id))
print(data)