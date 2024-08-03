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
        
        
    @app_commands.command(name="kick", description="Виганяє учасника із сервера.")
    @app_commands.describe(member="Учасник, якого потрібно вигнати.")
    @app_commands.describe(reason="Причина, через яку виганяють учасника.")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str]):
        kick_reason = "{administrator_name} вигнав {kiked_member} з причиною: {reason}.".format(
            administrator_name=interaction.user.name,
            kiked_member=member.name,
            reason=reason if reason else "Причина не надана"
        )

        try:
            await member.kick(reason=kick_reason)
            
            embed = discord.Embed(
                title="Учасника було вигнано!",
                description="Ви вигнали учасника",
                color=HexToColor(config["bot"]["color"]["ok"])
            )
            embed.set_author(
                name=member.name,
                url="https://discord.com/users/{member_id}".format(member_id=member.id),
                icon_url=member.avatar.url if member.avatar else discord.Embed.Empty
            )
            embed.set_footer(
                text="Mops Storage © 2020-{curent_year} Всі права захищено • {developer_site_url}".format(
                    curent_year=datetime.now().year,
                    developer_site_url=config["dev"]["site"]
                ),
                icon_url=config["bot"]["icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        except Exception as exp:
            logger.error(exp)
        
    
    @kick.error
    async def kick_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(KickCommand(bot))