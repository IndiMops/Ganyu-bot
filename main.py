# -*- coding: utf-8 -*-
import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os
import logging
from time import strftime
from time import gmtime
import sqlite3
import random
from ganyu import *
from importlib import reload

bot = commands.Bot(commands.when_mentioned_or('.'), intents = discord.Intents.all())
bot.remove_command('help')
discord.utils.setup_logging(level = logging.INFO, root = False)

data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()
config = LoadJson("config.json")# load config

@bot.event
async def on_ready():
    print(f'{config["bot_name"]} підключився до Discord.')
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as error:
        print(error)
        
    data = sqlite3.connect('data.sqlite')#connect to BD
    cur = data.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS stats_bot (
        'guilds' INT,
        'users' INT,
        'channels' INT,
        'commands' INT
        )""")
    data.commit()
    bot.loop.create_task(ch_pr())

@bot.event
async def on_guild_join(guild):
    print(f'Bot joined the guild: {guild.name} (id: {guild.id})')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as error:
        print(error)

async def up_db():
        """Оновлює статистику бота кожні 30 секунд
        """
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        guilds = bot.guilds
        users = len(bot.users)
        global channels
        channels = 0
        cur.execute(f'SELECT * FROM stats_bot')
        if cur.fetchone() == None:
            for guild in guilds:
                channels += len(guild.text_channels) + len(guild.voice_channels) + len(guild.stage_channels)
                cur.execute(f"INSERT INTO stats_bot VALUES ({int(len(guilds))}, {int(users)}, {int(channels)}, 0)")
        else:
            for guild in bot.guilds:
                channels += len(guild.text_channels) + len(guild.voice_channels) + len(guild.stage_channels)
                cur.execute(f'UPDATE stats_bot SET guilds = {int(len(guilds))}, users = {int(users)}, channels = {int(channels)}, commands = {StBcommands}')
        data.commit()
        await asyncio.sleep(60)
    


async def ch_pr():
    await bot.wait_until_ready()
    
    statuses = [GetMsg("bot_first_status").format(config['bot_prefix'], config['bot_version']), GetMsg("bot_second_status").format(len(bot.users))]
    while not bot.is_closed():
        status = random.choice(statuses)
        if status == statuses[0]:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game(status))
        else:
            await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = status))
        # print(GetMsg("debug_status")).format(config["bot_name"], status)
        await asyncio.sleep(30)
        
        bot.loop.create_task(up_db())


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = int(error.retry_after)
        cool = 0
        if cooldown < 60:
            cool = strftime(GetMsg("cooldown_duration_seconds"), gmtime(cooldown))
        elif 60 < cooldown < 3600:
            cool = strftime(GetMsg("cooldown_duration_minutes"), gmtime(cooldown))
        elif 3600 < cooldown < 86400:
            cool = strftime(GetMsg("cooldown_duration_hours"), gmtime(cooldown))
        elif 86400 < cooldown < 604800 or cooldown > 604800:
            cool = strftime(GetMsg("cooldown_duration_days"), gmtime(cooldown))
                    
        embed = discord.Embed(
            title = GetMsg("error_general_title"),
            description = GetMsg("error_cooldown_desc").format(cool),
            color = StrToColor(config['color_error'])
        )
        await ctx.reply(embed=embed)
        print(error)
    
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title = GetMsg("error_general_title"),
            description = GetMsg("error_command_not_found_desc").format(config["bot_prefix"]),
            color = StrToColor(config['color_error'])
        )
        
        await ctx.reply(embed = embed)
        print(error)

@bot.event
async def on_command_completion(ctx):
    for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
    cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
    data.commit()
    #print(f'\nВиконалась команда\nВсього виконано: {StBcommands + 1}\n')# Output of how many commands were executed in the bot

async def load_extensions():
    """Load cogs for main file
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load_extensions()
    await bot.start(config["bot_token"])

if __name__ == '__main__':
    asyncio.run(main())
