import discord
from os import listdir
from discord import app_commands
from discord.ext import commands
from ganyu import GetMsg, GuildConfGet, GuildConfReset, GuildConfSet, LoadJson, StrToColor


class SetLang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name='local_set', description='Set bot\'s messages language')
    @app_commands.describe(lang="Select language")
    @app_commands.choices(lang = [
        app_commands.Choice(name='English', value='en'),
        app_commands.Choice(name='Українська', value='uk'),
        app_commands.Choice(name='日本語', value='jp'),
        app_commands.Choice(name='Polski', value='pl')
    ])
    async def local_set_(self, interaction: discord.Interaction, lang: str):
        config = LoadJson("config.json")
        if interaction.guild is not None:
            if lang+".json" in listdir(f"locale"):
                GuildConfSet(interaction.guild, "locale", lang)
                print(f"Server's locale is now set to {lang}", interaction.guild)
                await interaction.response.send_message(embed=discord.Embed(title=GetMsg("set_locale_title", interaction.guild), description=GetMsg("set_locale_description", interaction.guild).format(GetMsg("locale_name", interaction.guild)), color=StrToColor(config["color_ok"])))
        else:
            await interaction.response.send_message(embed=discord.Embed(title=GetMsg("dm_title", interaction.guild), description=GetMsg("dm_description", interaction.guild), color=StrToColor(config["color_error"])))

    
async def setup(bot):
    await bot.add_cog(SetLang(bot))