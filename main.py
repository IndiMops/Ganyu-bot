import asyncio
import json
import discord
import os

from discord.ext import commands, tasks
from ganyu_utils import *
from dotenv import load_dotenv
from discord import app_commands
from random import random

load_dotenv()
config = LoadJson("config.json")
logger = setup_logging()

# Set up the bot with when_mentioned as a command prefix
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command("help")
discord.utils.setup_logging(level = logging.INFO, root = False)

# Initialize the global variable bot_commands
bot_commands = {}


@bot.event
async def on_ready():
    try:
        await bot.tree.sync()
        logger.info("Bot is online!")
        change_status.start()
        # Get bot slash commands
        commands = await bot.tree.fetch_commands()
        
        for idx, command in enumerate(commands):
            bot_commands[str(idx)] = {
                "name": command.name,
                "id": str(command.id)
            }
            
        # print(config["bot_commands"])
        bot_commands_json = json.dumps(bot_commands, indent=4, ensure_ascii=False)
        # print(bot_commands_json)
        
        if "bot_commands" in config:
            config["bot_commands"] = json.loads(bot_commands_json)
            
        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)
    except Exception as exp:
        print(exp)



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
