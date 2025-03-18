import discord

from ganyu_utils import LoadJson, setup_logging, GetMsg, HexToColor
from discord.ext import commands
from discord import app_commands
from discord.app_commands import Choice
from datetime import datetime

config = LoadJson("config.json")
logger = setup_logging()

class LocaleCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    locale_group = app_commands.Group(name = "locale", description = GetMsg("commands.locale.description"))

    @app_commands.describe(locale = GetMsg("commands.locale.set.describe.locale"))
    @app_commands.choices(
        locale = [
            Choice(name = GetMsg("general.locale.be"), value = "be"),
            Choice(name = GetMsg("general.locale.de"), value = "de"),
            Choice(name = GetMsg("general.locale.en"), value = "en"),
            Choice(name = GetMsg("general.locale.es"), value = "es"),
            Choice(name = GetMsg("general.locale.fr"), value = "fr"),
            Choice(name = GetMsg("general.locale.it"), value = "it"),
            Choice(name = GetMsg("general.locale.ja"), value = "ja"),
            Choice(name = GetMsg("general.locale.ko"), value = "ko"),
            Choice(name = GetMsg("general.locale.pl"), value = "pl"),
            Choice(name = GetMsg("general.locale.pt"), value = "pt"),
            Choice(name = GetMsg("general.locale.uk"), value = "uk"),
        ]
    )
    @app_commands.checks.has_permissions(manage_guild = True)
    @locale_group.command(name = "set", description = GetMsg("commands.locale.set.description"))
    async def set(self, interaction: discord.Interaction, locale: Choice[str]):
        cursor = self.bot.db.connection.cursor()
        
        try:
            cursor.execute("UPDATE servers SET locale = %s WHERE discord_id = %s", (locale.value, str(interaction.guild_id)))
            self.bot.db.commit()
            
            embed = discord.Embed(
                title = f"{GetMsg("general.success", interaction.guild)}!",
                description = GetMsg("commands.locale.set.embed.description", interaction.guild).format(locale_name = GetMsg(f"general.locale.{locale.value}", interaction.guild)),
                color = HexToColor(config["bot"]["color"]["ok"])
            )
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                icon_url = config["bot"]["icon"]
            )
            
            await interaction.response.send_message(embed = embed, ephemeral = True)
        except Exception as e:
            logger.error(f"Error in {self.set}: {e}")
            await interaction.response.send_message(content = GetMsg("errors.general.something_went_wrong", interaction.guild), ephemeral = True)
    
    
    @locale_group.command(name = "reset", description = "Скинути мову бота на поточнмоу сервері.")
    async def reset(self, interaction: discord.Interaction):
        cursor = self.bot.db.connection.cursor()
                
        try:
            cursor.execute("UPDATE servers SET locale = %s WHERE discord_id = %s", (config["bot"]["locale"], str(interaction.guild_id),))
            self.bot.db.commit()
                    
            embed = discord.Embed(
                title = f"Успіх!",
                description = "Мова бота на цьому сервері була скинута.",
                color = HexToColor(config["bot"]["color"]["ok"])
            )
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = GetMsg("general.embed.footer", interaction.guild).format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                icon_url = config["bot"]["icon"]
            )
                    
            await interaction.response.send_message(embed = embed, ephemeral = True)
        except Exception as e:
            logger.error(f"Error in {self.reset}: {e}")
            await interaction.response.send_message(content = "Щось пішло не так.", ephemeral = True)
    
    
    
    @set.error
    async def set_error(self, interaction: discord.Interaction, error):
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
            

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.bot.tree.get_command("locale"):
            self.bot.tree.add_command(self.locale_group)

async def setup(bot):
    await bot.add_cog(LocaleCommands(bot))