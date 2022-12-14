# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
from config import settings
import asyncio
import os
import logging
from time import strftime
from time import gmtime
import sqlite3
import random
from discord import app_commands

bot = commands.Bot(commands.when_mentioned_or('.'), intents = discord.Intents.all())
bot.remove_command('help')
discord.utils.setup_logging(level = logging.INFO, root = False)

data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()

@bot.event
async def on_ready():
    print(f'{bot.user.name} підключився до Discord.')
    
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
    

async def sync():
    """Synchronization of slash commands"""
    fmt = await bot.tree.sync()
    print(f'\033[34mInformation\033[0m: Синхронізовано {len(fmt)} слеш-команд')
    await asyncio.sleep(10)

async def ch_pr():
    await bot.wait_until_ready()
    
    statuses = [f"{settings['prefix']}help | v{settings['version']}", f"за {len(bot.users)} користувачів"]
    while not bot.is_closed():
        status = random.choice(statuses)
        if status == statuses[0]:
            await bot.change_presence(status = discord.Status.online, activity = discord.Game(status))
        else:
            await bot.change_presence(status = discord.Status.online, activity = discord.Activity(type = discord.ActivityType.watching, name = status))
        print(f'\033[33m{settings["name"]}\033[0m: Bot changed the status to \033[11m{status}\033[0m')
        await asyncio.sleep(30)
        
        bot.loop.create_task(sync())
        bot.loop.create_task(up_db())


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = int(error.retry_after)
        cool = 0
        if cooldown < 60:
            cool = strftime('%S сек.', gmtime(cooldown))
        elif 60 < cooldown < 3600:
            cool = strftime('%M хв. %S сек.', gmtime(cooldown))
        elif 3600 < cooldown < 86400:
            cool = strftime('%H год. %M хв. %S сек.', gmtime(cooldown))
        elif 86400 < cooldown < 604800 or cooldown > 604800:
            cool = strftime('%d днів %H год. %M хв. %S сек.', gmtime(cooldown))
                    
        embed = discord.Embed(
            title='Помилка!',
            description=f'Ви ще не можете використовувати цю команду!\nСпробуйте через: **{cool}**',
            color=0xff0000
        )
        await ctx.reply(embed=embed)
        print(error)
    
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(
            title='Помилка!',
            description=f'Дану комнаду не знайдено!\nСкористайтесь: `{settings["prefix"]}help`',
            color=0xff0000
        )
        
        await ctx.reply(embed=embed)
        print(error)

@bot.event
async def on_command_completion(ctx):
    for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
    cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
    data.commit()
    print(f'\nВиконалась команда\nВсього виконано: {StBcommands + 1}\n')

async def load_extensions():
    """Load cogs for main file
    """
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


async def main():
    await load_extensions()
    await bot.start(settings['token'])

if __name__ == '__main__':
    asyncio.run(main())
