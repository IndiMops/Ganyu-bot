import discord

from ganyu_utils import *
from discord.ext import commands
from discord import app_commands
from datetime import datetime

config = LoadJson("config.json")
logger = setup_logging()

class InfoCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name = "info", description = "Отримайте інформацію та статистику про {0}".format(config["bot"]["name"]))
    async def info_(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title = config["bot"]["name"],
            description = "Привіт, я Ґанью секретар Цісін в Ліюе. Моє завдання допомагати мандрівникам освоюватися з дивовижним світом Тейват\n\nЯ використовую слеш-команди, тому тепер я стала ще більш зручним ботом. Якщо ти хочеш дізнатися всі мої команди тоді можеш скористатися </{0}:{1}>. Або скористайся </{2}:{3}>, щоб розпочати свою подорож{4}".format(GetCommand(4)["name"], GetCommand(4)["id"], "journey", "1264024444454371144", "<a:ganyuroll:1265243572500955197>"),
            color = HexToColor(config["bot"]["color"]["default"]),
        )
        
        embed.set_thumbnail(url = config["bot"]["icon"])
        embed.set_footer(
            text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
            icon_url = config["bot"]["icon"]
        )
        # TODO: Add function to grab the last updated date of the bot from GitHub repository release  
        embed.add_field(
            name = "Збірка:",
            value= "{0} (<t:{1}:d>)".format(config["bot"]["version"], config["bot"]["last_updated"]),
        )
        
        embed.add_field(
            name = "Мій розробник:",
            value = "{0} [{1}](https://discord.com/users/{2})".format(config["dev"]["emoji"], config["dev"]["name"], config["dev"]["id"]),
        )
        
        # This empty field is needed to align all the fields, or if you ever have additional information, you can add it here
        embed.add_field(
            name = "⠀",
            value = "⠀"
        )
        
        embed.add_field(
            name = "Корисні посилання:",
            value = "[Веб-сайт]({0})\n[Сервер підтримки]({1})".format(config["bot"]["site"], config["bot"]["other_links"]["support_server"]),
        )
        
        embed.add_field(
            name = "⠀",
            value = "[GitHub репозиторій]({0})\n[top.gg]({1})".format(config["bot"]["other_links"]["github_repo"], config["bot"]["other_links"]["top.gg"]),
        )
        
        embed.add_field(
            name = '⠀',
            value = '[Patreon]({0})\n[Diaka]({1})'.format(config["bot"]["other_links"]["patreon"], config["bot"]["other_links"]["diaka"])
        )
        
        await interaction.response.send_message(embed = embed, ephemeral = True)

async def setup(bot):
    await bot.add_cog(InfoCommand(bot))