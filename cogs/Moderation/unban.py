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
        
    
    @app_commands.command(name = "unban", description = GetMsg("commands.unbun.description"))
    @app_commands.describe(member = GetMsg("commands.unbun.describe.member").format(command_name = GetCommand(9)["name"]))
    @app_commands.describe(reason = GetMsg("commands.unbun.describe.reason"))
    @app_commands.checks.has_permissions(ban_members = True)
    async def unban(self, interaction: discord.Interaction, member: str, reason: Optional[str]):
        member = await self.bot.fetch_user(int(member))
        unban_reason = GetMsg("commands.unbun.unban_reason", interaction.guild).format(
            administrator_name = interaction.user.name,
            member_name = member.name,
            reason = reason if reason else GetMsg("general.no_reason", interaction.guild)
        )
            
        await interaction.guild.unban(member, reason = unban_reason)
            
        embed = discord.Embed(
            title = GetMsg("commands.unbun.embed.title", interaction.guild),
            description = GetMsg("commands.unbun.embed.description", interaction.guild),
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
            
            
        await interaction.response.send_message(embed = embed, ephemeral = True)
            
        first_text_channel = None
        for channel in interaction.guild.text_channels:
            if channel.permissions_for(interaction.guild.me).create_instant_invite:
                first_text_channel = channel
                break
                
        invite = await first_text_channel.create_invite(
            max_uses = 1,
            reason = GetMsg("commands.unbun.invite", interaction.guild).format(
                admin_name = interaction.user.name,
                user_name = member.name
            )
        )
            
        # DM member for unban
        embed = discord.Embed(
            title = GetMsg("commands.unbun.DM.embed.title, interaction.guild"),
            description = GetMsg("commands.unbun.DM.embed.description").format(
                guild_name = interaction.guild.name,
                administrator_name = interaction.user.name,
                reason_unban = reason,
                server_invite_url = invite.url
            ),
            color = HexToColor(config["bot"]["color"]["default"])
        )
        embed.set_footer(
            text = GetMsg("general.embed.footer", interaction.guild).format(
                curent_year = datetime.now().year,
                dev_site_url = config["dev"]["site"]
            ),
            icon_url = config["bot"]["icon"]
        )
        embed.set_thumbnail(url = interaction.guild.icon)
        if interaction.guild.banner:
            embed.set_image(interaction.guild.banner)
            
        await member.send(embed = embed)
        
    
    @unban.error
    async def ban_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = f"{GetMsg("errors.general.error", interaction.guild)}!",
                    description = GetMsg("errors.general.missing_permissions", interaction.guild),
                    color = HexToColor(config["bot"]["color"]["error"]),
                ).set_footer(
                    text = GetMsg("general.embed.footer").format(
                        curent_year = datetime.now().year,
                        dev_site_url = config["dev"]["site"]
                    ),
                    icon_url = config["bot"]["icon"]
                ),
                ephemeral = True
            )
        
        
async def setup(bot):
    await bot.add_cog(UnbanCommand(bot))