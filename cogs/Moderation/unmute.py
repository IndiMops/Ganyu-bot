import discord

from discord import app_commands
from discord.ext import commands
from ganyu_utils import *
from typing import Optional
from datetime import datetime

config = LoadJson("config.json")


class UnmuteCommand(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
    
    @app_commands.command(name = "unmute", description = GetMsg("commands.unmute.description"))
    @app_commands.describe(member = GetMsg("commands.unmute.describe.member"))
    @app_commands.describe(reason = GetMsg("commands.unmute.describe.reason"))
    @app_commands.checks.has_permissions(deafen_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        if not member.is_timed_out():
            embed = discord.Embed(
                title = f"{GetMsg("errors.general.error", interaction.guild.name)}!",
                description = GetMsg("errors.general.user_not_have_mute", interaction.guild.name),
                color = HexToColor(config["bot"]["color"]["error"])
            )
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year = datetime.now().year,
                    dev_site_url = config["dev"]["site"]
                ),
                icon_url = config["bot"]["icon"]
            )
            embed.set_thumbnail(url = interaction.guild.icon)
            
            return await interaction.response.send_message(embed = embed, ephemeral = True)
            
        embed = discord.Embed(
            title = GetMsg("commands.unmute.embed.title", interaction.guild.name),
            description = GetMsg("commands.unmute.embed.description", interaction.guild).format(member_name = member.name),
            color = HexToColor(config["bot"]["color"]["ok"])
        )
        embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year = datetime.now().year,
                    dev_site_url = config["dev"]["site"]
                ),
                icon_url = config["bot"]["icon"]
            )
        embed.set_thumbnail(url = interaction.guild.icon)
        
        await member.timeout(None, reason=reason)
        await interaction.response.send_message(embed = embed, ephemeral = True)
        
        
    @unmute.error
    async def unmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = f"{GetMsg("errors.general.error", interaction.guild.name)}!",
                    description = GetMsg("general.embed.footer", interaction.guild),
                    color = HexToColor(config["bot"]["color"]["error"]),
                ).set_footer(
                    text = GetMsg("general.embed.footer", interaction.guild).format(
                        curent_year = datetime.now().year,
                        dev_site_url = config["dev"]["site"]
                    ),
                    icon_url = config["bot"]["icon"]
                ),
                ephemeral=True
            )
     

async def setup(bot):
    await bot.add_cog(UnmuteCommand(bot))