import time
import yt_dlp

ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': '-',
            'extract_flat': True,
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
            # "nocheckcertificate": True,
            "no_cache_dir": True,
            "rm-cache-dir": True,
            }

async def search_id_yt(query):
    start_time = time.time()

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        link = f'ytsearch1:{query} "auto-generated"'
        info = ydl.extract_info(link, download=False)

    elapsed = time.time() - start_time
    print(f'유튜브 id 검색: {elapsed:.6f}초 소요')

    url = info['entries'][0]['url'] if 'entries' in info else info['url']
    return url.split('watch?v=')[-1].split('?')[0]

async def get_streamingdata(v_id):
    start_time = time.time()

    with (yt_dlp.YoutubeDL(ydl_opts) as ydl):
        url = f'https://www.youtube.com/watch?v={v_id}'
        info = ydl.extract_info(url, download=False)
        data = {'artist': info['channel'],
                'title': info['fulltitle'],
                'url': info['url'],
                'thumbnail': info['thumbnails'][0]['url'],
                } if info else []

    elapsed = time.time() - start_time
    print(f'유튜브 스트리밍 url 추출: {elapsed:.6f}초 소요')

    return data