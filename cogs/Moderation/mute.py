import discord

from discord import app_commands, utils
from discord.ext import commands
from ganyu_utils import *
from humanfriendly import parse_timespan, format_timespan, InvalidTimespan
from typing import Optional
from datetime import datetime, timedelta

config = LoadJson("config.json")


class MuteCommand(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
    @app_commands.command(name = "mute", description = GetMsg("commands.mute.description"))
    @app_commands.describe(member = GetMsg("commands.mute.describe.member"))
    @app_commands.describe(reason = GetMsg("commands.mute.describe.reason"))
    @app_commands.describe(duration = GetMsg("commands.mute.describe.duration"))
    @app_commands.checks.has_permissions(deafen_members = True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str], duration: Optional[str] = "60s"):
        try:
            duration = parse_timespan(duration)
        except InvalidTimespan:
            embed = discord.Embed(
                title = f"{GetMsg("errors.general.warning", interaction.guild)}!",
                description = GetMsg("errors.general.invalid_timespan", interaction.guild),
                color = HexToColor(config["bot"]["color"]["warn"])
            )
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year = datetime.now().year,
                    dev_site_url = config["dev"]["site"]
                ),
                icon_url=config["bot"]["icon"]
            )
            embed.set_thumbnail(url=interaction.guild.icon)
            
            return await interaction.response.send_message(embed = embed, ephemeral = True)
    
        if duration <= float(2419200):
            mute_reason = GetMsg("commands.mute.mute_reason.if_reason_exists", interaction.guild).format(
                administrator_name = interaction.user.name,
                member_name = member.name,
                reason = reason if reason else GetMsg("general.no_reason", interaction.guild)
            )
            
            embed = discord.Embed(
                title = GetMsg("commands.mute.embed.title", interaction.guild),
                description = GetMsg("commands.mute.embed.description", interaction.guild).format(
                    member_mention = member.mention,
                    duration = format_timespan(duration) if duration else "60s",
                    reason_text = mute_reason
                ),
                color=HexToColor(config["bot"]["color"]["ok"])
            )
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year = datetime.now().year,
                    dev_site_url = config["dev"]["site"]
                ),
                icon_url = config["bot"]["icon"]
            )
            embed.set_thumbnail(url=interaction.guild.icon)
            
            await member.timeout(utils.utcnow() + timedelta(seconds = duration), reason = mute_reason)
            await interaction.response.send_message(embed = embed, ephemeral = True)
        else:
            embed = discord.Embed(
                title = GetMsg("errors.general.error", interaction.guild),
                description = GetMsg("errors.general.nute_duration_limit", interaction.guild),
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
            await interaction.response.send_message(embed = embed, ephemeral = True)
            
            
    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(MuteCommand(bot))