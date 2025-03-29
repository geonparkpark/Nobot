import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
from search import search_url

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
print(f'token: {TOKEN}')

intents = discord.Intents.default()
intents.message_content = True  # 메시지 읽기 권한 활성화
ffmpeg_path = os.path.join(os.path.dirname(__file__), 'venv', 'ffmpeg', 'bin', 'ffmpeg.exe') # ffmpeg 바이너리 경로지정

bot = commands.Bot(intents=intents, command_prefix='/')

# 음성 채널에 연결하고 음악을 재생하는 명령어
@bot.command(name="play", aliases=["재생"])
async def play(ctx, *, query):
    start_time = time.time()
    ctx.message.delete()

    if not ctx.author.voice:
        await ctx.send("음성 채널을 먼저 들어가야죠 ㅋㅋ")

    else:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
            elapsed = time.time() - start_time
            print(f'음성 채널 접속: {elapsed:.6f}초 소요')

            start_time = time.time()
            url = search_url(query)
            elapsed = time.time() - start_time
            print(f'음원 Search total: {elapsed:.6f}초 소요')

            start_time = time.time()
            audio = discord.FFmpegPCMAudio(url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 3',
                                           options='-vn', executable=ffmpeg_path)
            elapsed = time.time() - start_time
            print(f'음원 FFmpeg 변환: {elapsed:.6f}초 소요')

            ctx.voice_client.play(audio)

            # 재생곡 정보 출력
        await ctx.send(f'play {query} by {ctx.author}')

@bot.command()
async def test_audio(ctx):
    if not ctx.voice_client:
        channel = ctx.author.voice.channel
        await channel.connect()

    song = discord.FFmpegPCMAudio("Bryan Chase  - GREENLIGHT(SNIPPET).mp3", executable=ffmpeg_path)
    source = discord.PCMVolumeTransformer(song)
    ctx.voice_client.play(source, after=lambda e: print(f'Player error: {e}') if e else None)
    await ctx.send("테스트 음성 재생 중...")

@bot.command()
async def is_playing(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        await ctx.send("현재 음악이 재생 중입니다.")
    else:
        await ctx.send("음악이 재생되고 있지 않습니다.")

# 봇 준비 완료 이벤트
@bot.event
async def on_ready():
    print(f"✅ {bot.user} 로 로그인 완료!")

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error occurred in event {event}: {args} {kwargs}")

# 핑 명령어 추가
@bot.command()
async def ping(ctx):
    await ctx.send("ㅋ")

bot.run(TOKEN)
