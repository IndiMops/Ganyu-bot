"""
This module sets up and runs a Discord bot using the discord.py library.

The bot connects to a MySQL database, loads configuration from a JSON file,
and dynamically loads command extensions (cogs) from the 'cogs' directory.
It also handles various bot events such as on_ready, on_disconnect, on_guild_join,
and on_guild_remove, and periodically changes its status.

Modules:
    asyncio: Provides support for asynchronous programming.
    json: Provides support for JSON encoding and decoding.
    discord: Provides the core functionality for interacting with the Discord API.
    os: Provides a way of using operating system dependent functionality.
    dotenv: Loads environment variables from a .env file.
    random: Implements pseudo-random number generators for various distributions.
    typing: Provides runtime support for type hints.

Functions:
    load_extensions: Loads command extensions (cogs) from the 'cogs' directory.

Classes:
    Database: A custom class for interacting with the MySQL database.

Events:
    on_ready: Called when the bot is ready.
    on_disconnect: Called when the bot disconnects.
    on_guild_join: Called when the bot joins a new guild.
    on_guild_remove: Called when the bot leaves a guild.

Tasks:
    change_status: Periodically changes the bot's status.

Entry Point:
    main: The main entry point for running the bot.
"""
import os
import json
import logging

import asyncio

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

from ganyu_utils import Database, LoadJson, setup_logging, GetCommand


load_dotenv()
config = LoadJson("config.json")
logger = setup_logging()
db = Database(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    password=os.getenv("MYSQL_PASSWORD"),
    database=os.getenv("MYSQL_DATABASE")
)

# Set up the bot with when_mentioned as a command prefix
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command("help")
discord.utils.setup_logging(level=logging.INFO, root=False)
bot.db = db

# Initialize the global variable bot_commands
bot_commands = {}


@bot.event
async def on_ready():
    """
    Asynchronous event handler called when the bot is ready to start processing events.
    This function performs the following tasks:
    1. Connects to the database.
    2. Synchronizes the bot's command tree.
    3. Logs in the bot user.
    4. Starts a task to periodically change the bot's status.
    5. Fetches the bot's slash commands and stores them in a dictionary.
    6. Serializes the bot's command dictionary to JSON and updates the "bot_commands" field in the
    config file.
    If any exception occurs during the execution of this function, it will be printed to the
    console.
    Parameters:
        None
    Returns:
        None
    """
    try:
        db.connect()  # Connect to the database
        await bot.tree.sync()
        logger.info("Logged in as %s", bot.user)
        change_status.start()
        # Get bot slash commands
        fetched_commands = await bot.tree.fetch_commands()

        for idx, command in enumerate(fetched_commands):
            bot_commands[str(idx)] = {
                "name": command.name,
                "id": str(command.id)
            }

        bot_commands_json = json.dumps(
            bot_commands, indent=4, ensure_ascii=False)

        if "bot_commands" in config:
            config["bot_commands"] = json.loads(bot_commands_json)

        with open("config.json", "w", encoding="utf-8") as config_file:
            json.dump(config, config_file, indent=4, ensure_ascii=False)
    except discord.DiscordException as discord_err:
        logger.error("Discord API error: %s", discord_err)
    except ConnectionError as conn_err:
        logger.error("Database connection error: %s", conn_err)


@bot.event
async def on_disconnect():
    """
    Asynchronous function called when the client disconnects.

    Closes the connection to the database.

    Parameters:
        None

    Returns:
        None
    """
    db.close()


@bot.event
async def on_guild_join(guild):
    """
    Event handler called when the bot joins a guild.

    Args:
        guild (Guild): The guild that the bot has joined.

    Returns:
        None
    """
    print(f"Joined guild {guild.name} with {guild.member_count} members")


@bot.event
async def on_guild_remove(guild):
    """
    Event handler called when the bot is removed from a guild.

    Parameters:
        guild (Guild): The guild the bot was removed from.

    Returns:
        None
    """
    print(f"Left guild {guild.name} with {guild.member_count} members")


@tasks.loop(seconds=10)
async def change_status():
    """
    Changes the status and activity of the bot.
    This function iterates through the guilds the bot is a member of and counts the unique non-bot
    members.
    It then sets the bot's status and activity using the count of unique members.
    Parameters:
        None
    Returns:
        None
    """
    unique_members = set()

    for guild in bot.guilds:
        for member in guild.members:
            if not member.bot:
                unique_members.add(member.id)

    statuses = [
        discord.Game(
            name=f"/{GetCommand(4)["name"]} | v{config["bot"]["version"]}"),
        discord.Activity(
            type=discord.ActivityType.watching,
            name=f"за {len(unique_members)} користувачами"
        )
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
        """
        Main function that loads extensions and starts the bot.

        Usage:
            - Ensure that the necessary extensions are loaded before starting the bot.
            - Start the bot by passing the bot token as an environment variable.

        Returns:
            None
        """
        await load_extensions()
        await bot.start(os.getenv("BOT_TOKEN"))

    asyncio.run(main())
