import discord

from discord import app_commands
from discord.ext import commands
from ganyu_utils import *
from datetime import datetime
from typing import Optional


config = LoadJson("config.json")


class BanCommand(commands.Cog):
    def __init__(self, bot: commands.bot):
        self.bot = bot
        
    @app_commands.command(name="ban", description="Забанити учасника на сервері.")
    @app_commands.describe(member="Користувач, якого треба забанити.")
    @app_commands.describe(reason="Прична бану учасника.")
    @app_commands.describe(delete_message="Видалити повідомлення учасника за останні дні(1 = 1 день).")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, interaction: discord.Interaction, member: discord.Member, reason: Optional[str], delete_message: Optional[int]):
        ban_reason = GetMsg("commands.ban.ban_reason.if_reason_exists", interaction.guild).format(
            administrator_name = interaction.user.name,
            baned_member = member.name,
            reason = reason if reason else GetMsg("general.no_reason")
        )

        if delete_message is None:
            await member.ban(reason=ban_reason)
        else:
            await member.ban(reason=ban_reason, delete_message_days=delete_message)
        
        embed = discord.Embed(
            title = GetMsg("commands.ban.embed.administrator.title", interaction.guild),
            description = GetMsg("commands.ban.embed.administrator.description", interaction.guild),
            color = HexToColor(config["bot"]["color"]["ok"])
        )
        embed.set_author(
            name = member.name,
            url = "https://discord.com/users/{member_id}".format(member_id = member.id),
            icon_url = member.avatar.url if member.avatar else discord.Embed.Empty
        )
        embed.set_footer(
            text = GetMsg("general.embed.footer").format(
                curent_year = datetime.now().year,
                dev_site_url = config["dev"]["site"]
            ),
            icon_url=config["bot"]["icon"]
        )
            
        await interaction.response.send_message(embed = embed, ephemeral = True)
            
        # The message of the punished member
        reason = GetMsg("commands.ban.ban_reason.no_reason", interaction.guild) if reason is None else reason
        embed = discord.Embed(
            title = GetMsg("commands.ban.embed.DM_member.title", interaction.guild),
            description = GetMsg("commands.ban.embed.DM_member.description").format(guild_name = interaction.guild.name, administrator_name = interaction.user.name, reason_ban = reason),
            color = HexToColor(config["bot"]["color"]["default"])
        )
        embed.set_footer(
            text = GetMsg("general.embed.footer", interaction.guild).format(
                curent_year=datetime.now().year,
                dev_site_url=config["dev"]["site"]
            ),
            icon_url=config["bot"]["icon"]
        )
        embed.set_thumbnail(url=interaction.guild.icon)
        if interaction.guild.banner:
            embed.set_image(interaction.guild.banner)
            
        await member.send(embed=embed)
        
        
    @ban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = GetMsg("errors.general.error", interaction.guild) + "!",
                    description = GetMsg("errors.general.missing_permissions", interaction.guild),
                    color=HexToColor(config["bot"]["color"]["error"]),
                ).set_footer(
                    text = GetMsg("general.embed.footer", interaction.guild).format(
                        curent_year=datetime.now().year,
                        dev_site_url=config["dev"]["site"]
                    ),
                    icon_url=config["bot"]["icon"]
                ),
                ephemeral = True
            )

        
async def setup(bot):
    await bot.add_cog(BanCommand(bot))