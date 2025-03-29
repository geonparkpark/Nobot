import yt_dlp as youtube_dl
import time

ydl_opts = {
            'format': 'bestaudio/best',
            #'postprocessors': [{
            #    'key': 'FFmpegExtractAudio',
            #    'preferredcodec': 'mp3',
            #    'preferredquality': '192',
            #}],
            'outtmpl': '-', #'downloads/%(id)s.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }

def get_yturl(v_id):
    start_time = time.time()
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        url = f'https://www.youtube.com/watch?v={v_id}'
        info = ydl.extract_info(url, download=False)
        url = info['url'] if info else ''
    elapsed = time.time() - start_time
    print(f'yt_dlp 추출: {elapsed:.6f}초 소요')
    return url