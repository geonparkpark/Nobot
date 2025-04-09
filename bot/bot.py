import time
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
import wavelink
from request import search_data, get_new_data

load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

LAVALINK_URL = os.getenv("LAVALINK_URL", "ws://localhost:2333")
LAVALINK_PASSWORD = os.getenv("LAVALINK_PASSWORD", "youshallnotpass")

intents = discord.Intents.default()
intents.message_content = True  # 메시지 읽기 권한 활성화

bot = commands.Bot(intents=intents, command_prefix='/')

song_queue = {}

def get_queue(guild_id):
    if guild_id not in song_queue:
        song_queue[guild_id] = asyncio.Queue()
    return song_queue[guild_id]

@bot.command(name="play", aliases=["재생", 'p'])
async def play(ctx, *, query):
    await ctx.message.delete()
    unexpected = False

    if not ctx.author.voice:
        await ctx.send("음성 채널을 먼저 들어가야죠 ㅋㅋ")
        return

        # 음성 채널 접속 및 라바링크 player 객체 연결
    channel = ctx.author.voice.channel
    player: wavelink.Player = ctx.voice_client or await channel.connect(cls=wavelink.Player)

        # 데이터 서버에서 query에 대한 데이터 가져오기
    try:
        data = await asyncio.create_task(search_data(query))
    except Exception as e:
        print(f'server error:\n{e}')
        title = '서버 응답 오류'
        description = '잠시 후에 시도해 주세요..'
        embed = discord.Embed(title=title, description=description, color=discord.Color.lighter_grey())
        await ctx.send(embed=embed)
        return

    url = data['url']
    for i in range(2): # url 만료 시 한 번만 url 발급 시도
        try:
            track = await wavelink.Playable.search(url)
            break
        except Exception as e:
            url = await asyncio.create_task(get_new_data(data['id']))
            print(f"lavalink error {data['id']}: {e}")
            track = None
            unexpected = True
            time.sleep(5)
            continue

    if not track:
        unexpected = True

    if unexpected:
        title = '예기치 못한 오류'
        description = '검색어를 다시 확인하거나\n잠시 후에 시도해 주세요..'
        embed = discord.Embed(title=title, description=description, color=discord.Color.lighter_grey())
        await ctx.send(embed=embed)
        return

    track = track[0]

        # 재생목록
    queue = get_queue(ctx.guild.id)

        # 채널에 출력할 임베드 생성
    url_yt = 'https://www.youtube.com/watch?v=' + data['id']
    title = '😈 ADDED TO PLAYLIST' if player.is_playing() else '😈 PLAY'
    description = f"[{data['title']}]({url_yt})\n\n{data['artist']}"

    if not player.is_playing() and not player.is_paused() and not player.current:
        await player.play(track)
    else:
        q = {'track': track, 'title': data['title'], 'url': url_yt}
        await queue.put(q)

        # 채널에 임베드 출력
    embed = discord.Embed(title=title, description=description, color=discord.Color.lighter_grey())
    embed.set_thumbnail(url=data['thumbnail'])
    await ctx.send(embed=embed)

@bot.event
async def on_wavelink_track_end(player: wavelink.Player, track, reason):
    queue = get_queue(player.guild.id)

    if queue.empty():
        await player.disconnect()
    else:
        next_track_data = await queue.get()
        next_track = next_track_data['track']
        await player.play(next_track)

@bot.command(name='skip', aliases=['s', '스킵'])
async def skip(ctx):
    await ctx.message.delete()
    player: wavelink.Player = ctx.voice_client
    if player and player.is_playing():
        await player.stop()

@bot.command(name='queue', aliases=['playlist', 'list', '목록', '재생목록', '큐', 'q'])
async def queue(ctx):
    queue = get_queue(ctx.guild.id)
    if queue:
        list = []
        for q in queue._queue:
            list.append(f"[{q['title']}]({q['url']})")
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
        await ctx.send("를고 읻는 7H 업네요..")

@bot.command(name='pause', aliases=['일시정지'])
async def pause(ctx):
    player: wavelink.Player = wavelink.Pool.get_node().get_player(ctx.guild.id)
    if player and player.is_playing():
        await player.pause(True)
        await ctx.message.delete()

        embed = discord.Embed(
            title=f'PAUSED',
            color=discord.Color.lighter_grey()
        )
        await ctx.send(embed=embed)

@bot.command(name='resume', aliases=['재개'])
async def resume(ctx):
    player: wavelink.Player = wavelink.Pool.get_node().get_player(ctx.guild.id)
    if player and player.is_paused():
        await player.pause(False)
        await ctx.message.delete()

        embed = discord.Embed(
            title=f'RESUMED',
            color=discord.Color.lighter_grey()
        )
        await ctx.send(embed=embed)

@bot.event
async def on_error(event, *args, **kwargs):
    print(f"Error occurred in event {event}: {args} {kwargs}")

# 핑 명령어 추가
@bot.command()
async def ping(ctx):
    await ctx.send("ㅋ")

@bot.event
async def on_connect():
    nodes = [wavelink.Node(uri=LAVALINK_URL, password=LAVALINK_PASSWORD)]
    await wavelink.Pool.connect(nodes=nodes, client=bot)
    print("Lavalink connected!")



bot.run(TOKEN)
