import discord

from discord import app_commands
from discord.ext import commands
from discord.ui import View, Button
from ganyu_utils import LoadJson, setup_logging, PagginationView

from typing import List
from collections import deque


config = LoadJson("config.json")
logger = setup_logging()

        
class PagginationCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
        
    @app_commands.command(name="pagginatio", description="A command that demonstrates the use of pagination")
    async def paggination(self, interaction: discord.Interaction):
        if config["dev"]["id"] == str(interaction.user.id):
            embeds = [
                discord.Embed(title="Page 1", description="This is the first page"),
                discord.Embed(title="Page 2", description="This is the second page"),
                discord.Embed(title="Page 3", description="This is the third page"),
                discord.Embed(title="Page 4", description="This is the fourth page"),
                discord.Embed(title="Page 5", description="This is the fifth page"),
                discord.Embed(title="Page 6", description="This is the sixth page"),
                discord.Embed(title="Page 7", description="This is the seventh page"),
                discord.Embed(title="Page 8", description="This is the eighth page"),
                discord.Embed(title="Page 9", description="This is the ninth page"),
                discord.Embed(title="Page 10", description="This is the tenth page"),
            ]
            
            view = PagginationView(embeds)
            await interaction.response.send_message(embed=view.initial, view=view, ephemeral=True)
        else:
            await interaction.response.send_message(content="Вибач, але ти не мій господар. Тому я не буду для тебе це виконувати<:chibiganyudeadinside:1265243125740470294>", ephemeral=True)


async def setup(bot):
    await bot.add_cog(PagginationCommand(bot))