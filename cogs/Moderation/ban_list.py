import discord
import io
import json

from discord import app_commands
from discord.ext import commands
from ganyu_utils import *
from typing import Optional
from datetime import datetime


config = LoadJson("config.json")
logger = setup_logging()


class BanListCommand(commands.Cog):
    def __init__(self, bot: commands):
        self.bot = bot
        
    
    @app_commands.command(name="ban_list", description="Список всіх забанених користувачів на сервері")
    @app_commands.describe(number_banned = "Скільки забанених користувачів відобразити. За замовчуванням: 1000")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban_list(self, interaction: discord.Interaction, number_banned: Optional[int] = 1000):
        bans = [entry async for entry in interaction.guild.bans(limit=number_banned)]
        bans_list = {
            index: {
                "user": {
                    "id": str(entry.user.id),
                    "name": entry.user.name
                },
                "reason": entry.reason
            }
            for index, entry in enumerate(bans)
        }
            
        if len(bans_list) > 10:
            json_data = json.dumps(bans_list, indent=4, ensure_ascii=False)
            file = discord.File(io.BytesIO(json_data.encode()), filename=f"{interaction.guild.id}|bans_list.json")
            return await interaction.response.send_message(content = GetMsg("commands.ban_list.embed.overrun_members", interaction.guild), file=file, ephemeral=True)
        elif len(bans_list) == 0:
            embed = discord.Embed(
                title = GetMsg("commands.ban_list.embed.title", interaction.guild).format(server_name = interaction.guild.name),
                description = GetMsg("commands.ban_list.embed.descriptions_no_baned_members", interaction.guild).format(emoji = "<:ganyudizzy:1265243411540082798>"),
                color = HexToColor(config["bot"]["color"]["default"]),
            )
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year=datetime.now().year,
                    dev_site_url=config["dev"]["site"]
                ),
                icon_url=config["bot"]["icon"]
            )
                
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title = GetMsg("commands.ban_list.embed.title", interaction.guild).format(server_name=interaction.guild.name),
                color=HexToColor(config["bot"]["color"]["default"])
            )
                
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(
                    curent_year=datetime.now().year,
                    dev_site_url=config["dev"]["site"]
                ),
                icon_url=config["bot"]["icon"]
            )
            embed.set_thumbnail(url=interaction.guild.icon)
                
            for key, ban in bans_list.items():
                user_info = ban["user"]
                embed.add_field(
                    name = "{user_name} (ID: `{user_id}`)".format(user_name=user_info["name"], user_id=user_info["id"]),
                    value = GetMsg("commands.ban_list.embed.ban_reason", interaction.guild).format(ban_reason=ban["reason"]),
                    inline = False
                )
            return await interaction.response.send_message(embed=embed, ephemeral=True)
        
    
    @ban_list.error
    async def ban_list_error(self, interaction: discord.Interaction, error):
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
                ).set_thumbnail(url=config["bot"]["icon"]),
                ephemeral=True
            )
    
    
        
async def setup(bot):
    await bot.add_cog(BanListCommand(bot))
