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
        
    @app_commands.command(name="mute", description="Тимчасово заглушити коритсувача на сервері")
    @app_commands.describe(member="Учасник, якому треба видаити мут.")
    @app_commands.describe(reason="Причина через яку видається мут.")
    @app_commands.describe(duration="Час на який видається мут. За замовчуванням на 60 секунд.")
    @app_commands.checks.has_permissions(deafen_members=True)
    async def mute(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str], duration: Optional[str] = "60s"):
        try:
            duration = parse_timespan(duration)
        except InvalidTimespan:
            embed = discord.Embed(
                title="Попередження!",
                description="Ви ввели не правильний формат часу.\nПідтримується такий формат часу: `5s`, `5m`, `5h`, `5d`.",
                color=HexToColor(config["bot"]["color"]["warn"])
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
    
        if duration <= float(2419200):
            mute_reason = "{administrator_name} видав мут {member_name} з причиною: {reason}.".format(
                administrator_name=interaction.user.name,
                member_name=member.name,
                reason=reason if reason else "Причина не надана"
            )
            
            embed = discord.Embed(
                title="Учасникик був зам'ючений",
                description="Ви успішно зам'ютели учасника {member_mention} на `{duration}`\nПричина:\n`{reason_text}`".format(
                    member_mention=member.mention,
                    duration=format_timespan(duration) if duration else "60s",
                    reason_text=mute_reason
                ),
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
            
            await member.timeout(utils.utcnow() + timedelta(seconds = duration), reason = mute_reason)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title="Помилка",
                description="Виберіть менший період муту. Discord не підтримує мути більше 28 днів.",
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
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
            
    @mute.error
    async def mute_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(MuteCommand(bot))