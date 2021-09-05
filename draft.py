from os import name
import discord
import keyboard
import random
import youtube_dl 
from discord.ext import commands
from discord import FFmpegPCMAudio, PCMVolumeTransformer
import time

bot = commands.Bot(command_prefix="-")
bot.queue = {}

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    channel = discord.utils.get(bot.get_all_channels(), name='general')
    # await channel.send("Pls apologize to mod @WYK")
    # guild = discord.utils.get(bot.get_guild(), id = "415188177020518411")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await bot.process_commands(message)


@bot.command()
async def play(ctx, message):
    
    if(ctx.voice_client):
        pass
    else :
        channel = ctx.author.voice.channel
        voice_channel = await channel.connect()
    await play_with_queue(ctx, message)
   

async def play_with_queue(ctx, message):
    if not ctx.voice_client.is_playing():
        await start_playing(ctx.voice_client, message, ctx.channel)
    else :
        return
    # #if q = 0 start counter    
    # if(len(bot.queue) == 0):
    #     bot.queue = message
    # #if q != 0 increment counter
    # else :
    #     bot.queue[len(bot.queue)] = message
    #     await ctx.channel.send("Added "+ message +" to Queue")
    # # await ctx.channel.send("https://youtu.be/77zsaWA2I44")

async def start_playing(voice_client, message, channel):
    ydl_opts = {'format': 'bestaudio'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5','options': '-vn'}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(message, download=False)
        URL = info['formats'][0]['url']
    voice_client.play(discord.FFmpegPCMAudio(URL,  **FFMPEG_OPTIONS))
    await channel.send("Playing " + message)

def check_queue(message):
    if message in bot.queue:
        return
    else:
        bot.queue[len(bot.queue)] = message


@bot.command()
async def clear(ctx):
    bot.queue = {}
    await ctx.channel.send("Cleared Queue")

@bot.command()
async def queue(ctx):
    await ctx.channel.send(bot.queue)

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
async def p(ctx, message):
    channel = ctx.author.voice.channel
    await channel.connect()

@bot.command()
async def leave(ctx):
    if (ctx.voice_client): # If the bot is in a voice channel
        await ctx.guild.voice_client.disconnect() # Leave the channel
    else: # But if it isn't
        await ctx.send("I'm not in a voice channel, use the join command to make me join")

bot.run("amtoken")
