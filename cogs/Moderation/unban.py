import discord

from discord import app_commands
from discord.ext import commands
from ganyu_utils import *
from typing import Optional
from datetime import datetime


config = LoadJson("config.json")


class UnbanCommand(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
    
    @app_commands.command(name="unban", description="Розбанити ")
    @app_commands.describe(member="Користувач якого потрібно розбанити. Щоб дізнатися id користувача скористайтеся `/{command_name}`.".format(command_name=GetCommand(9)["name"]))
    @app_commands.describe(reason="Причина з якої ви розбанюєте учасника.")
    @app_commands.checks.has_permissions(ban_members=True)
    async def unban(self, interaction: discord.Interaction, member: str, reason: Optional[str] = "Причина не надана"):
        member = await self.bot.fetch_user(int(member))
        unban_reason = "{administrator_name} зняв бан {member_name} з причиною: {reason}.".format(
            administrator_name=interaction.user.name,
            member_name=member.name,
            reason=reason if reason else "Причина не надана"
        )
            
        await interaction.guild.unban(member, reason=unban_reason)
            
        embed = discord.Embed(
            title="Учасник був розбанений!",
            description="Ви розбанили учасника",
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
            
        first_text_channel = None
        for channel in interaction.guild.text_channels:
            if channel.permissions_for(interaction.guild.me).create_instant_invite:
                first_text_channel = channel
                break
                
        invite = await first_text_channel.create_invite(
            max_uses=1,
            reason="Створине автоматично. Через те, що {admin_name} розбанив користувача {user_name}.".format(
                admin_name=interaction.user.name,
                user_name = member.name
            )
        )
            
        # DM member for unban
        embed=discord.Embed(
            title="Вас розбанили!",
            description="З вас зняли бан на сервері: `{guild_name}`\nАдмінстратором: {administrator_name}.\nПричина: ```{reason_unban}```\n\nЯкщо ви бажаєте повернутися на серевер ви можете скористатися цим запрошенням: {server_invite_url}".format(
                guild_name=interaction.guild.name,
                administrator_name=interaction.user.name,
                reason_unban=reason,
                server_invite_url=invite.url
            ),
            color=HexToColor(config["bot"]["color"]["default"])
        )
        embed.set_footer(
            text="Mops Storage © 2020-{curent_year} Всі права захищено • {developer_site_url}".format(
                curent_year=datetime.now().year,
                developer_site_url=config["dev"]["site"]
            ),
            icon_url=config["bot"]["icon"]
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        if interaction.guild.banner:
            embed.set_image(interaction.guild.banner)
            
        await member.send(embed=embed)
        
    
    @unban.error
    async def ban_error(self, interaction: discord.Interaction, error):
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
    await bot.add_cog(UnbanCommand(bot))