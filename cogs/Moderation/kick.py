import discord

from discord import app_commands
from discord.ext import commands
from ganyu_utils import *
from typing import Optional
from datetime import datetime

config = LoadJson("config.json")
logger = setup_logging()


class KickCommand(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
        
    @app_commands.command(name = "kick", description = GetMsg("commands.kick.description"))
    @app_commands.describe(member = GetMsg("commands.kick.describe.member"))
    @app_commands.describe(reason = GetMsg("commands.kick.describe.reason"))
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        kick_reason = GetMsg("commands.kick.kick_reason.if_reason_exists", interaction.guild).format(
            administrator_name = interaction.user.name,
            kiked_member = member.name,
            reason = reason if reason else GetMsg("general.no_reason", interaction.guild)
        )

        try:
            await member.kick(reason = kick_reason)
            
            embed = discord.Embed(
                title = GetMsg("commands.kick.embed.title", interaction.guild),
                description = GetMsg("commands.kick.embed.description", interaction.guild),
                color = HexToColor(config["bot"]["color"]["ok"])
            )
            embed.set_author(
                name = member.name,
                url = "https://discord.com/users/{member_id}".format(member_id=member.id),
                icon_url = member.avatar.url if member.avatar else discord.Embed.Empty
            )
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year = datetime.now().year,
                    dev_site_url = config["dev"]["site"]
                ),
                icon_url = config["bot"]["icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as exp:
            logger.error(exp)
        
    
    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = f"{GetMsg("errors.general.error", interaction.guild)}!",
                    description = GetMsg("errors.general.missing_permissions", interaction.guild),
                    color = HexToColor(config["bot"]["color"]["error"]),
                ).set_footer(
                    text = GetMsg("general.embed.footer", interaction.guild).format(
                        curent_year = datetime.now().year,
                        dev_site_url = config["dev"]["site"]
                    ),
                    icon_url = config["bot"]["icon"]
                ),
                ephemeral = True
            )
    
        
async def setup(bot):
    await bot.add_cog(KickCommand(bot))