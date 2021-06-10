import discord
import os
from discord import FFmpegPCMAudio
from discord.utils import get
import youtube_dl

from discord.ext import commands

client = commands.Bot(command_prefix = '!')

token = open("token.txt", "r").read()

@client.event
async def on_ready():
    print('> bot ready')

@client.command()
async def ping(ctx):
    await ctx.send(f'IT\'S ALIVE!!!\n Your latency --> {round(client.latency*1000)}ms')

@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

@client.command(pass_context=True)
async def leave(ctx):
    guild = ctx.message.guild
    voice_client = guild.voice_client
    if voice_client:
        await voice_client.disconnect()
    else:
        print('error')

@client.command(pass_context=True)
async def play(ctx, req: str):
    await ctx.send('Загружаю композицию')
    song_check = os.path.isfile('song.mp3')
    try:
        if song_check:
            os.remove('song.mp3')
    except PermissionError:
        await ctx.send('НЕТ')
        return
    voice_client = ctx.message.guild.voice_client
    ytdl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ytdl_opts) as ydl:
        ydl.download([f'ytsearch: {req}'])
    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            videoname = file.title()
            os.rename(file, 'song.mp3')

    voice_client.play(discord.FFmpegPCMAudio('song.mp3'))
    await ctx.send('Играет: ' + videoname)
    voice_client.is_playing()

#    if voice_client:
#        player = await voice_client.create_ytdl_player(url, ytdl_options={'default_search': 'auto'})
#        player.start()
#    else:
#        print('error')


client.run(token)
