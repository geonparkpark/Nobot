import yt_dlp
import time

query = 'the weeknd open hearts single version'

ydl_opts = {
            'format': 'bestaudio/best',
            'n_threads': 8,
            'noplaylist': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': '-',
        }

# ydl_opts = {
#         'format': 'bestaudio/best',
#         'noplaylist': True,
#         'quiet': True,
# }

start_time = time.time()
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    link = query if query.startswith("http") and ".com" in query else f'ytsearch1:{query}'
    info = ydl.extract_info(link, download=False)
    #music_url = info['url']
elapsed = time.time() - start_time
print(f'유튜브 음원 url 추출: {elapsed:.6f}초 소요')

if 'entries' in info:
        print(info['entries'][0]['url'])
else:
        print(info['url'])

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     info = ydl.extract_info(url, download=False)
#
# for x in range(len(info)):
#     print(x)
#     print(info[x])