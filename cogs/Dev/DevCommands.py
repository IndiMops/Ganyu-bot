import discord
import os
import requests

from discord import app_commands
from discord.ext import commands
from discord.ui import Select, View, Button, Modal
from ganyu_utils import *
from ganyu_utils import Database
from dotenv import load_dotenv
from typing import List

import mysql.connector
from mysql.connector import Error

config = LoadJson("config.json")
logger = setup_logging()
load_dotenv()

try:
    conn = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE")
    )
    
    cursor = conn.cursor()
    logger.info("Connected to MySQL")
except Error as e:
    logger.error("Error while connecting to MySQL", e)
    

class DevCommands(commands.Cog, name = "Developer Commands"):
    """Commands to test various functions, events, etc.
    The lichen is crystallized for the test and no more!
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.hybrid_command()
    async def sync(self, ctx: commands.Context):
        if ctx.author.id == int(config["dev"]["id"]):
            await ctx.send("Синхронізація...")
            await self.bot.tree.sync()
            await ctx.send("Синхронізація завершена!")
            commands = await self.bot.tree.fetch_commands()
            for comamnd in commands:
                print(f"Command: {comamnd.name}: {comamnd.id}")
        else:
            await ctx.send("You must be the owner to use this command!\nYour id: {0}\nOwner id: {1}".format(ctx.author.id, config["dev"]["id"]))
    
    @app_commands.command(name="test")
    async def test(self, interaction: discord.Interaction, color: bool):
        await interaction.response.send_message("Test")
        await interaction.response.send_message(str(color))
        
    @app_commands.command(name="ping")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message("Pong")
        
    @app_commands.command(name="get_user", description="Отримання інформації про користувача")
    async def get_user(self, interaction: discord.Interaction, user: discord.User):
        headers = {"Authorization": f"Bot {os.getenv("BOT_TOKEN")}"}
        req = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=headers).json()
        await interaction.response.send_message(content="User avatar: {user_avatar};\nUser banner: {user_banner};\nOther user info: {req}".format(req=req, user_avatar=user.avatar, user_banner=user.banner if user.banner is None else "User don't have a banner"), ephemeral=True)
    

    # "Test UI" command
    # Commanmd embeds
    class TestCommandEmbeds():
        main_menu_embed = discord.Embed(
            title="Головне меню",
            description="Головне меню команди",
            color=HexToColor(config["bot"]["color"]["default"])
        )
        
        submenu1_embed = discord.Embed(
            title="Підменю 1",
            description="Так, це справді під меню під номером 1",
            color=HexToColor(config["bot"]["color"]["default"])
        )
        
        submenu2_embed = discord.Embed(
            title="Підменю 2",
            description="Так, це справді під меню під номером 2",
            color=HexToColor(config["bot"]["color"]["default"])
        )

    # Command 
    class TestCommandMainMenuDrop(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(
                    value = "1",
                    label = "Підменю 1"
                ),
                discord.SelectOption(
                    value = "2",
                    label = "Підменю 2"
                )
            ]
            
            super().__init__(placeholder="Виберіть одне із підменю", options=options)
            
        async def callback(self, interaction: discord.Interaction):
            if self.values[0] == "1":
                await interaction.response.edit_message(
                    embed=DevCommands.TestCommandEmbeds.submenu1_embed,
                    view=DevCommands.TestCommandSubmenu1View()
                )
            elif self.values[0] == "2":
                await interaction.response.edit_message(content="Another work!")
            
    class TestCommandSubmenu1Drop(discord.ui.Select):
        def __init__(self):
            options = [
                discord.SelectOption(
                    value = "1",
                    label = "Підменю 1"
                ),
                discord.SelectOption(
                    value = "2",
                    label = "Підменю 2"
                ),
                discord.SelectOption(
                    value = "3",
                    label="Назад"
                )
            ]
            
            super().__init__(placeholder="Виберіть пункт...", options=options)
            
        async def callback(self, interaction: discord.Interaction):
            if self.values[0] == "1":
                await interaction.response.edit_message(
                    embed=DevCommands.TestCommandEmbeds.submenu1_embed,
                    view=DevCommands.TestCommandSubmenu1View()
                )
            elif self.values[0] == "2":
                await interaction.response.edit_message(
                    embed=DevCommands.TestCommandEmbeds.submenu2_embed,
                    view=DevCommands.TestCommandSubmenu1View()
                )
            elif self.values[0] == "3":
                await interaction.response.edit_message(embed=DevCommands.TestCommandEmbeds.main_menu_embed, view=DevCommands.TestCommandMainMenuView())
    
    
    class TestCommandMainMenuView(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(DevCommands.TestCommandMainMenuDrop())
    
    class TestCommandSubmenu1View(discord.ui.View):
        def __init__(self):
            super().__init__()
            self.add_item(DevCommands.TestCommandSubmenu1Drop())
    
    
    @app_commands.command(name="test_ui", description="Перевірка UI елементів")
    async def test_ui(self, interaction: discord.Interaction):
        if config["dev"]["id"] == str(interaction.user.id):
            await interaction.response.send_message(embed=DevCommands.TestCommandEmbeds.main_menu_embed, view=DevCommands.TestCommandMainMenuView())
        else:
            await interaction.response.send_message(content="Вибач, але ти не мій господар. Тому я не буду для тебе це виконувати<:chibiganyudeadinside:1265243125740470294>")
    
    
    
    @app_commands.command(name="test_db", description="Тестування роботи з базою даних")
    async def test_db(self, interaction: discord.Interaction):
        cursor = self.bot.db.connection.cursor()
        
        if config["dev"]["id"] == str(interaction.user.id):
            # Створюємо словник з індексом для кожного сервера
            server_data = {
                index: {
                    "name": guild.name,
                    "id": str(guild.id)
                }
                for index, guild in enumerate(self.bot.guilds)
            }
        
            for index in server_data:
                server = server_data[index]
                cursor.execute("INSERT INTO servers (name, discord_id) VALUES (%s, %s)", (server["name"], int(server["id"])))
                
            self.bot.db.commit()
        else:
            await interaction.response.send_message(content="Вибач, але ти не мій господар. Тому я не буду для тебе це виконувати<:chibiganyudeadinside:1265243125740470294>")


    @app_commands.command(name="test_db2", description="Тестування роботи з базою даних")
    async def terst_db2(self, interaction: discord.Interaction):
        cursor = self.bot.db.connection.cursor()
        
        if config["dev"]["id"] == str(interaction.user.id):
            cursor.execute("SELECT * FROM servers WHERE discord_id = %s", (interaction.guild.id,))
            servers = cursor.fetchone()
            print(servers)
        else:
            await interaction.response.send_message(content="Вибач, але ти не мій господар. Тому я не буду для тебе це виконувати<:chibiganyudeadinside:1265243125740470294>")
    

async def setup(bot):
    await bot.add_cog(DevCommands(bot))
