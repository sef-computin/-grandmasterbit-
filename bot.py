import os
import asyncio

import discord
from discord.ext import commands

import music
import soundboard

token_f = open("token", "r")

token =  token_f.readline()

cogs = [music]

client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

for i in range(len(cogs)):
    #await client.load_extension("music")
    asyncio.run(cogs[i].setup(client))

#async def load_cogs():
#    await client.load_extension(music)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def ping(ctx):
    await ctx.send(f'Я живой!!\n А у вот пинг:  {round(client.latency*1000)}ms')

#async def main(token):
#    await load_cogs()
#    await client.start(token)
#    #async with client:
#    #    await load_cogs()
#    #    await client.start(token)

#asyncio.run(main(token))
#asyncio.run(load_cogs())
client.run(token)

