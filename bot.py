import os

import discord
from discord.ext import commands

import music

token_f = open("token", "r")

token =  token_f.readline()

cogs = [music]

client = commands.Bot(command_prefix='!', intents = discord.Intents.all())

for i in range(len(cogs)):
    cogs[i].setup(client)


@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def ping(ctx):
    await ctx.send(f'IT\'S ALIVE!!!\n Your latency --> {round(client.latency*1000)}ms')

client.run(token)
