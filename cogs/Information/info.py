import discord

from ganyu_utils import *
from discord.ext import commands
from discord import app_commands
from datetime import datetime

config = LoadJson("config.json")
logger = setup_logging()

class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "info", description = "Отримайте інформацію та статистику про {0}".format(config["bot"]["name"]))
    async def info_(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = config["bot"]["name"],
            description = GetMsg("commands.info.embed.description", interaction.guild).format(command_help_name = GetCommand(4)["name"], command_help_id = GetCommand(4)["id"], command_journey_name = "journey", command_journey_id = "1264024444454371144", emoji_ganyu_roll = "<a:ganyuroll:1265243572500955197>"),
            color = HexToColor(config["bot"]["color"]["default"]),
        )
        
        embed.set_thumbnail(url = config["bot"]["icon"])
        embed.set_footer(
            text = GetMsg("general.embed.footer", interaction.guild).format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
            icon_url = config["bot"]["icon"]
        )
        # TODO: Add function to grab the last updated date of the bot from GitHub repository release  
        embed.add_field(
            name = GetMsg("commands.info.fields.name.build", interaction.guild),
            value = GetMsg("commands.info.fields.value.build", interaction.guild).format(bot_version = config["bot"]["version"], last_update_Unix_time = config["bot"]["last_updated"]),
        )
        
        embed.add_field(
            name = GetMsg("commands.info.fields.name.dev", interaction.guild),
            value = GetMsg("commands.info.fields.value.dev", interaction.guild).format(dev_emoji = config["dev"]["emoji"], dev_name = config["dev"]["name"], dev_id = config["dev"]["id"]),
        )
        
        # This empty field is needed to align all the fields, or if you ever have additional information, you can add it here
        embed.add_field(
            name = "⠀",
            value = "⠀"
        )
        
        embed.add_field(
            name = GetMsg("commands.info.fields.name.link1", interaction.guild),
            value = GetMsg("commands.info.fields.value.link1").format(bot_site_url = config["bot"]["site"], bot_support_server_url = config["bot"]["other_links"]["support_server"]),
        )
        
        embed.add_field(
            name = "⠀",
            value = GetMsg("commands.info.fields.value.link2").format(bot_github_url = config["bot"]["other_links"]["github_repo"], bot_top_gg_url = config["bot"]["other_links"]["top.gg"]),
        )
        
        embed.add_field(
            name = '⠀',
            value = '[Patreon]({0})\n[Diaka]({1})'.format(config["bot"]["other_links"]["patreon"], config["bot"]["other_links"]["diaka"])
        )
        
        await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot):
    await bot.add_cog(InfoCommand(bot))