import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import time
from search import search_music_data, setup_redis, close_redis
import asyncio

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")
print(f'token: {TOKEN}')

intents = discord.Intents.default()
intents.message_content = True  # 메시지 읽기 권한 활성화
curr_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
ffmpeg_path = os.path.join(curr_dir, 'venv', 'ffmpeg', 'bin', 'ffmpeg.exe') # ffmpeg 바이너리 경로지정

bot = commands.Bot(intents=intents, command_prefix='/')

song_queue = {}

def get_queue(guild_id):
    if guild_id not in song_queue:
        song_queue[guild_id] = []
    return song_queue[guild_id]

@bot.command(name="play", aliases=["재생", 'p'])
async def play(ctx, *, query):
    start_time = time.time()
    await ctx.message.delete()

    if not ctx.author.voice:
        await ctx.send("음성 채널을 먼저 들어가야죠 ㅋㅋ")

    if not ctx.voice_client:
        channel = ctx.author.voice.channel
        await channel.connect()
        elapsed = time.time() - start_time
        print(f'음성 채널 접속: {elapsed:.6f}초 소요')

    start_time = time.time()
    data = await asyncio.create_task(search_music_data(query))
    elapsed = time.time() - start_time
    print(f'음원 Search total: {elapsed:.6f}초 소요')

    url = 'https://www.youtube.com/watch?v=' + data['id']
    title = '😈 ADDED TO PLAYLIST' if ctx.voice_client.is_playing() else '😈 PLAY'
    embed = discord.Embed(
        title=title,
        description=f"[{data['title']}]({url})\n\n{data['artist']}",
        color=discord.Color.lighter_grey()
    )
    embed.set_thumbnail(url=data['thumbnail'])
    await ctx.send(embed=embed)

    queue = get_queue(ctx.guild.id)
    queue.append(data)

    if not ctx.voice_client.is_playing():
        await play_next(ctx, ctx.voice_client)

async def play_next(ctx, voice_client):
    queue = get_queue(ctx.guild.id)
    if queue:
        data = queue.pop(0)
        url = data['url']

        start_time = time.time()
        audio = discord.FFmpegPCMAudio(url, before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 3',
                                   options='-vn', executable=ffmpeg_path)
        elapsed = time.time() - start_time
        print(f'음원 FFmpeg 변환: {elapsed:.6f}초 소요')

        voice_client.play(audio, after=lambda e: asyncio.run_coroutine_threadsafe(play_next(ctx, voice_client), bot.loop))

    else:
        await voice_client.disconnect()

@bot.command(name='skip', aliases=['s', '스킵'])
async def skip(ctx):
    await ctx.message.delete()
    voice_client = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice_client and voice_client.is_playing():
        voice_client.stop()

@bot.command(name='queue', aliases=['playlist', 'list', '목록', '재생목록', '큐', 'q'])
async def queue(ctx):
    queue = get_queue(ctx.guild.id)
    if queue:
        list = []
        for data in queue:
            list.append(f"[{data['title']}]({data['url']})")
        plist = '\n'.join(list)
        embed = discord.Embed(
            title='PLAYLIST',
            description=plist,
            color=discord.Color.lighter_grey()
        )
        await ctx.send(embed=embed)
    else:
        await ctx.send("EMPTY PLAYLIST")

@bot.command(name='stop', aliases=['정지', 'kick'])
async def stop(ctx):
    if ctx.voice_client:
        await ctx.message.delete()
        await ctx.voice_client.disconnect()

        embed = discord.Embed(
            title=f'👿 STOP',
            color=discord.Color.lighter_grey()
        )
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

@bot.event
async def on_ready():
    await setup_redis()
    print(f'{bot.user} is connected to Discord!')

@bot.event
async def on_close():
    await close_redis()

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error occurred in event {event}: {args} {kwargs}")

# 핑 명령어 추가
@bot.command()
async def ping(ctx):
    await ctx.send("ㅋ")



bot.run(TOKEN)
