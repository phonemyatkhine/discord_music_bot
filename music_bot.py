from os import name
import discord
import keyboard
import random
import youtube_dl 
from discord.ext import commands, tasks
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import time
import urllib.request
import re

bot = commands.Bot(command_prefix="-")
bot.queue = {}
bot.queue_marker = 0


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    channel = discord.utils.get(bot.get_all_channels(), name='general')
    # await channel.send("Pls apologize to mod @WYK")
    # guild = discord.utils.get(bot.get_guild(), id = "415188177020518411")
    check_queue.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)

@tasks.loop(seconds = 10.0)
async def check_queue():
    channel = discord.utils.get(bot.get_all_channels(), name='general')
    if(len(bot.queue) > 1 and bot.queue_marker < len(bot.queue)) :
        for voice_client in bot.voice_clients:
            if not (voice_client.is_playing()):
                await start_playing(voice_client, bot.queue_marker,channel)
    else:
        return
    # if(commands.Context.voice_client.is_playing()):
    #     await channel.send("Playing")
    # await channel.send("Looping")

@bot.command()
async def play(ctx, *,args):
    message = youtube_search(args)
    if(ctx.voice_client):
        pass
    else :
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

    if(len(bot.queue) == 0):
        bot.queue[0] = message
        async with ctx.typing():
            await start_playing(ctx.voice_client, bot.queue_marker, ctx.channel)
    else :
        bot.queue[len(bot.queue)] = message
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message, download=False)
            URL = info['formats'][0]['url']
        embed = discord.Embed(
            color = discord.Color.blue(),
            description = "Added " + info['title'] + " to Queue"
        )
        await ctx.channel.send(embed = embed)

@bot.command()
async def p(ctx, *, args):
    message = youtube_search(args)
    if(ctx.voice_client):
        pass
    else :
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()

    if(len(bot.queue) == 0):
        bot.queue[0] = message
        async with ctx.typing():
            await start_playing(ctx.voice_client, bot.queue_marker, ctx.channel)
    else :
        bot.queue[len(bot.queue)] = message
        ydl_opts = {'format': 'bestaudio'}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(message, download=False)
            URL = info['formats'][0]['url']
        embed = discord.Embed(
            color = discord.Color.blue(),
            description = "Added " + info['title'] + " to Queue"
        )
        await ctx.channel.send(embed = embed)

async def start_playing(voice_client, queue_marker, channel):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(bot.queue[queue_marker], download=False)
        URL = info['formats'][0]['url']
    voice_client.play(discord.FFmpegPCMAudio(URL,  **FFMPEG_OPTIONS))
    bot.queue_marker += 1
    embed = discord.Embed(
        title = "Playing",
        color = discord.Color.blue(),
        description = info['title']
    )
    embed.set_thumbnail(url=info['thumbnails'][0]['url'])
    await channel.send(embed=embed)
    
def youtube_search(message):
    search_keyword = ""
    split_message = message.split()
    for word in split_message:
        search_keyword = search_keyword + "+" + word 
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + search_keyword)
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    return ("https://www.youtube.com/watch?v=" + video_ids[0])

@bot.command()
async def clear(ctx):
    bot.queue = {}
    bot.queue_marker = 0
    await ctx.channel.send("Cleared Queue")

@bot.command(brief="Plays a single video, from a youtube URL")
async def rickroll(ctx):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
        URL = info['formats'][0]['url']
    if(ctx.voice_client):
        voice_channel = await ctx.voice_client.connect(reconnect = false, timeout = false)
    else :
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()
    print(URL)
    await voice_channel.play(discord.FFmpegPCMAudio(URL,  **FFMPEG_OPTIONS))
    await ctx.channel.send("Never gonna give u up")

@bot.command()
async def leave(ctx):
    if not (ctx.guild.voice_client.channel == ctx.author.voice.channel) :
        return await ctx.channel.send('You need to be in a voice channel to use this command')
    else :    
        if (ctx.voice_client): # If the bot is in a voice channel
            await ctx.guild.voice_client.disconnect() # Leave the channel
        else: # But if it isn't
            await ctx.send("I'm not in a voice channel, use the join command to make me join")

# @bot.command()
# async def queue(ctx):
#     queue = bot.queue
    

# @bot.command()
# async def q(ctx):

bot.run("amtoken")
