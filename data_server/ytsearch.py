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

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        link = f'ytsearch1:{query} "auto-generated"'
        info = ydl.extract_info(link, download=False)

    url = info['entries'][0]['url'] if 'entries' in info else info['url']
    return url.split('watch?v=')[-1].split('?')[0]

async def get_streamingdata(v_id):

    with (yt_dlp.YoutubeDL(ydl_opts) as ydl):
        url = f'https://www.youtube.com/watch?v={v_id}'
        info = ydl.extract_info(url, download=False)
        data = {'artist': info['channel'],
                'title': info['fulltitle'],
                'url': info['url'],
                'thumbnail': info['thumbnails'][0]['url'],
                } if info else []

    return data