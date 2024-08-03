import discord

from ganyu_utils import *
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View


config = LoadJson("config.json")
logger = setup_logging()


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @app_commands.command(name="help", description="Показує довідкове повідомлення з усіма командами та категоріями")
    async def help(self, interaction: discord.Interaction, command: str = None, category: str = None):
        if command is None or category is None:
            menu = Select(
                placeholder="Виберіть категорію...",
                options=[
                    discord.SelectOption(
                        label="Інформація",
                        value="1",
                        emoji="📃"
                    )
                ]
            )
            
            async def callback(interaction: discord.Interaction):
                if menu.values[0] == "1":
                    embed = discord.Embed(
                        title = "Доступні команди категорії 📃Інформація",
                        descriptions = "Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою </{command_name}:{command_id}> `<назва команди чи категорії>`".format(command_name=GetCommand(3)["name"], command_id=GetCommand(3)["id"]),
                        color=HexToColor(config["color_default"])
                    )
        


async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
