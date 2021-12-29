import discord
import math
import random
import asyncio
import logging
import os
import datetime
from discord.ext import commands, tasks
import re
from discord import Intents
from db import Database
from typing import Text, Tuple
from math import sqrt
from discord.utils import get
from discord_webhook import DiscordWebhook

#you shouldnt touch any of this ngl 

bot = commands.Bot(command_prefix = '>', activity=discord.Game(name="Keeping track of builds"))
TOKEN = os.getenv('BOT_TOKEN')
guild = bot.get_guild(880015752533528626)
DATABASE_URL = os.environ['DATABASE_URL']
bot.db = Database()
startupWebhook = os.getenv('STARTUP')
roleList = []

@bot.event
async def on_ready():
    bot.guild = bot.get_guild(880015752533528626)
    await bot.change_presence(status=discord.Status.online, activity=discord.Game('Keeping track of builds'))
    print("--------------------") 
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------------------')
    webhook = DiscordWebhook(url=startupWebhook, rate_limit_retry=True, content=f'-------------------- \n Logged in as \n {bot.user.name} \n {bot.user.id} \n --------------------')
    response = webhook.execute()

@bot.listen()
async def on_connect():
    await bot.db.setup()
    print("database loaded")

@bot.listen()
async def on_message(message):
    if message.author.bot:
        return 
    if str(message.channel.type) == "private":
        await message.channel.send("Hey there! I dont answer to dms yet.")
        return
    if message.author == bot.user:
        return
    user = await bot.db.get_user(message.author.id)

@bot.event
async def on_command_error(ctx, error):
    logging.error(f'Error on command {ctx.invoked_with}, {error}')
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title="Error!",
                              description=f"The command `{ctx.invoked_with}` was not found! We suggest you do `>help` to see all of the commands",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.MissingRole):
        embed = discord.Embed(title="Error!",
                              description=f"You don't have permission to execute `{ctx.invoked_with}`.",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Error!",
                              description=f"`{error}`",
                              colour=0xe73c24)
        await ctx.send(embed=embed)
        raise error

bot.run(TOKEN) #starts the nuclear reactor