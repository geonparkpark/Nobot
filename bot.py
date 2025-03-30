import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
from search import search_music_data

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
    await ctx.message.delete()

    if not ctx.author.voice:
        await ctx.send("음성 채널을 먼저 들어가야죠 ㅋㅋ")

    else:
        if not ctx.voice_client:
            channel = ctx.author.voice.channel
            await channel.connect()
            elapsed = time.time() - start_time
            print(f'음성 채널 접속: {elapsed:.6f}초 소요')

        start_time = time.time()
        data = search_music_data(query)
        elapsed = time.time() - start_time
        print(f'음원 Search total: {elapsed:.6f}초 소요')

        start_time = time.time()
        audio = discord.FFmpegPCMAudio(data['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 3',
                                       options='-vn', executable=ffmpeg_path)
        elapsed = time.time() - start_time
        print(f'음원 FFmpeg 변환: {elapsed:.6f}초 소요')

        ctx.voice_client.play(audio)

        embed = discord.Embed(
            title=f'😈 PLAY',
            description=f"{data['title']}\n{data['artist']}",
            color=discord.Color.lighter_grey()
        )
        embed.set_thumbnail(url=data['thumbnail'])
        # 재생곡 정보 출력
        await ctx.send(embed=embed)

@bot.command(name='stop', aliases=['정지'])
async def stop(ctx):
    if ctx.voice_client:
        await ctx.message.delete()
        await ctx.voice_client.disconnect()

        embed = discord.Embed(
            title=f'👿 STOP',
            color=discord.Color.lighter_grey()
        )  # 재생곡 정보 출력
        await ctx.send(embed=embed)
    else:
        await ctx.send("❌ 현재 음성 채널에 있지 않습니다.")

@bot.command(name='pause', aliases=['일시정지'])
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.message.delete()

        embed = discord.Embed(
            title=f'PAUSED',
            color=discord.Color.lighter_grey()
        )
        await ctx.send(embed=embed)

    else:
        await ctx.send("❌ 현재 재생 중인 음악이 없습니다.")

@bot.command(name='resume', aliases=['재개'])
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.message.delete()

        embed = discord.Embed(
            title=f'RESUMED',
            color=discord.Color.lighter_grey()
        )
        await ctx.send(embed=embed)

    else:
        await ctx.send("❌ 일시정지된 음악이 없습니다.")

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
