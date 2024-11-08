import asyncio
import json
import discord
import os

from discord.ext import commands, tasks
from ganyu_utils import *
from ganyu_utils import Database
from dotenv import load_dotenv
from discord import app_commands
from random import random
from typing import List

load_dotenv()
config = LoadJson("config.json")
logger = setup_logging()
db = Database(
    host = os.getenv("MYSQL_HOST"),
    user = os.getenv("MYSQL_USER"),
    password = os.getenv("MYSQL_PASSWORD"),
    database = os.getenv("MYSQL_DATABASE")
)

# Set up the bot with when_mentioned as a command prefix
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command("help")
discord.utils.setup_logging(level = logging.INFO, root = False)
bot.db = db

# Initialize the global variable bot_commands
bot_commands = {}


@bot.event
async def on_ready():
    try:
        db.connect() # Connect to the database
        await bot.tree.sync()
        logger.info(f"Logged in as {bot.user}")
        change_status.start()
        # Get bot slash commands
        commands = await bot.tree.fetch_commands()
        
        for idx, command in enumerate(commands):
            bot_commands[str(idx)] = {
                "name": command.name,
                "id": str(command.id)
            }
            
        bot_commands_json = json.dumps(bot_commands, indent=4, ensure_ascii=False)
        
        if "bot_commands" in config:
            config["bot_commands"] = json.loads(bot_commands_json)
            
        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)
    except Exception as exp:
        print(exp)

@bot.event
async def on_disconnect():
    db.close()  # Close the connection to the database

@bot.event
async def on_guild_join(guild):
    print(f"Joined guild {guild.name} with {guild.member_count} members")

@bot.event
async def on_guild_remove(guild):
    print(f"Left guild {guild.name} with {guild.member_count} members")

@tasks.loop(seconds=10)
async def change_status():
    unique_members = set()
        
    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                unique_members.add(member.id)
            
    
    statuses = [
        discord.Game(name=f"/{GetCommand(4)["name"]} | v{config["bot"]["version"]}"),
        discord.Activity(type=discord.ActivityType.watching, name="за {count_member} користувачами".format(count_member=len(unique_members)))
    ]
    
    for status in statuses:
        await bot.change_presence(status=discord.Status.online, activity=status)
        await asyncio.sleep(25)
    
async def load_extensions():
    """Load cogs in main file"""
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            await bot.load_extension(f"cogs.{filename[:-3]}")

    # Додаткове завантаження папок
    for foldername in os.listdir("./cogs"):
        folder_path = os.path.join("./cogs", foldername)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.endswith(".py"):
                    await bot.load_extension(f"cogs.{foldername}.{filename[:-3]}")
    

if __name__ == '__main__':
    async def main():
        await load_extensions()
        await bot.start(os.getenv("BOT_TOKEN"))
        
    asyncio.run(main())
