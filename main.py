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

bot = commands.Bot(command_prefix = '!', activity=discord.Game(name="Keeping track of builds"))
TOKEN = os.getenv('BOT_TOKEN')
guild = bot.get_guild(880015752533528626)
DATABASE_URL = os.environ['DATABASE_URL']
bot.db = Database()
startupWebhook = os.getenv('STARTUP')
roleList = []
versionIdList = []
plembed = discord.Embed(title=f"Only people with Bot operator can give me orders", description="You cant control me you mere mortal", color=randomColor())

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

def randomColor():
    return str(hex(random.randint(0,16777215))) 

@bot.listen()
async def on_message(message):
    if message.author.bot:
        return 
    if str(message.channel.type) == "private":
        await message.channel.send("Hey there! I dont answer to dms yet.")
        return
    if message.author == bot.user:
        return

@bot.command()
async def getdownload(ctx, versionID):
    role = discord.utils.get(ctx.guild.roles, name="Bot operator")
    if role not in ctx.author.roles:
        return
    else:
        versionList = await bot.db.get_all_versions()
        for x in versionList:
            versionIdList.append(x["versionid"])
        if versionID not in versionIdList:
            embed = discord.Embed(title=f"Version {versionID} not found", description="Please check the spelling, here are all the currently available versions:", color=randomColor())
            for x in versionIdList:
                embed.add_field(name=x[versionID], value="--------",inline=False)
            await ctx.send(embed = embed)
        else:
            x = await bot.db.get_version_link(versionID)
            embed = discord.Embed(title=f"download link for {versionID}", description=x["versiondownload"], color=randomColor())
            await ctx.send(embed=embed)

@bot.command()
async def createbuild(ctx, versionID, downloadLink):
    role = discord.utils.get(ctx.guild.roles, name="Bot operator")
    if role not in ctx.author.roles:
        return
    else:
        if "https://api.onedrive.com/v1.0/shares/" in downloadLink:
            versionList = await bot.db.get_all_versions()
            for x in versionList:
                versionIdList.append(x["versionid"])
            if versionID not in versionIdList:
                await bot.db.create_version_link(versionID, downloadLink)
                embed = discord.Embed(title=f"Database entry created for {versionID}", description=f"Successfully created database entry for {versionID} with the download link: {downloadLink}", color=randomColor())
            else:
                x = await bot.db.get_version_link(versionID)
                downloadmoment = x["versiondownload"]
                embed = discord.Embed(title=f"Version {versionID} already exists", description=f"Version {versionID} already exists with the link {downloadmoment} \n if this is the incorrect link update it using !updatelink", color=randomColor())
        else:
            embed = discord.Embed(title=f"Wrong link", description=f"The link {downloadLink} is not a valid direct download link", color=randomColor())    
        await ctx.send(embed=embed)

@bot.command()
async def updatelink(ctx, versionID, downloadLink):
    role = discord.utils.get(ctx.guild.roles, name="Bot operator")
    if role not in ctx.author.roles:
        return
    else:
        await bot.db.update_version_link(downloadLink, versionID)
        embed = discord.Embed(title=f"download link for {versionID} successfully updated", color=randomColor())
        await ctx.send(embed=embed)

@bot.command()
async def versions(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Bot operator")
    if role not in ctx.author.roles:
        return
    else:
        versionList = await bot.db.get_all_versions()
        embed = discord.Embed(title="Every available build:", color=randomColor())
        for x in versionList:
            currID = x["versionid"]
            embed.add_field(name=f"{currID}", value="--------",inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def convertLink(ctx, link):
    driveLink = link.replace("https://1drv.ms/u/","https://api.onedrive.com/v1.0/shares/")
    DdLink = driveLink[:-9] + "/root/content"
    embed = discord.Embed(title=f"direct download link for {link} successfully created", description=f"Direct download link: {DdLink}" ,color=randomColor())
    await ctx.send(embed = embed) 

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