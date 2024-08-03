import discord

from discord import app_commands, utils
from discord.ext import commands
from ganyu_utils import *
from humanfriendly import parse_timespan, format_timespan, InvalidTimespan
from typing import Optional
from datetime import datetime, timedelta

config = LoadJson("config.json")


class UnmuteCommand(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
    
    @app_commands.command(name="unmute", description="Зняти мут із учасника.")
    @app_commands.describe(member="Учасник, якому знімиться мут.")
    @app_commands.describe(reason="Причина через яку знімається мут.")
    @app_commands.checks.has_permissions(deafen_members=True)
    async def unmute(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        if not member.is_timed_out():
            embed = discord.Embed(
                title="Помилка!",
                description="На даний момент учасник не має мут.",
                color=HexToColor(config["bot"]["color"]["error"])
            )
            embed.set_footer(
                text="Mops Storage © 2020-{curent_year} Всі права захищено • {developer_site_url}".format(
                    curent_year=datetime.now().year,
                    developer_site_url=config["dev"]["site"]
                ),
                icon_url=config["bot"]["icon"]
            )
            embed.set_thumbnail(url=interaction.guild.icon)
            
            return await interaction.response.send_message(embed=embed, ephemeral=True)
            
        embed = discord.Embed(
            title="Мут знято",
            description="Ви знаяли мут з учасника {member_name}".format(member_name=member.name),
            color=HexToColor(config["bot"]["color"]["ok"])
        )
        embed.set_footer(
            text="Mops Storage © 2020-{curent_year} Всі права захищено • {developer_site_url}".format(
                curent_year=datetime.now().year,
                developer_site_url=config["dev"]["site"]
            ),
            icon_url=config["bot"]["icon"]
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        
        await member.timeout(None, reason=reason)
        await interaction.response.send_message(embed=embed, ephemeral=True)
        
        
    @unmute.error
    async def unmute_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title="Помилка!",
                    description="У вас не достатьо прав для використання цієї команди.",
                    color=HexToColor(config["bot"]["color"]["error"]),
                ).set_footer(
                    text="Mops Storage © 2020-{curent_year} Всі права захищено • {developer_site_url}".format(
                        curent_year=datetime.now().year,
                        developer_site_url=config["dev"]["site"]
                    ),
                    icon_url=config["bot"]["icon"]
                ),
                ephemeral=True
            )
     

async def setup(bot):
    await bot.add_cog(UnmuteCommand(bot))