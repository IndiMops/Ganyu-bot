import discord

from ganyu_utils import *
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View
from datetime import datetime


config = LoadJson("config.json")
logger = setup_logging()


class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @app_commands.command(name="help", description="Показує довідкове повідомлення з усіма командами та категоріями")
    async def help(self, interaction: discord.Interaction, command: str = None, category: str = None):
        if command is None and category is None:
            menu = Select(
                placeholder="Виберіть категорію...",
                options=[
                    discord.SelectOption(
                        label="Інформація",
                        value="1",
                        emoji="📃"
                    ),
                    discord.SelectOption(
                        label="Модерація",
                        value="2",
                        emoji="🛡️"
                    )
                ]
            )
            
            async def callback(interaction: discord.Interaction):
                # Description of the Information category menu
                if menu.values[0] == "1":
                    embed = discord.Embed(
                        title = f"Доступні команди категорії {menu.options[0].emoji} {menu.options[0].label}",
                        description = "Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою </{command_name}:{command_id}> `<command:name>`".format(command_name=GetCommand(3)["name"], command_id=GetCommand(3)["id"]),
                        color=HexToColor(config["bot"]["color"]["default"])
                    )
                    embed.set_thumbnail(url = config["bot"]["icon"])
                    embed.set_footer(
                        text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                        icon_url = config["bot"]["icon"]
                    )
                    
                    # Splitting each command of the category via discord.Embed.add_field()
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(3)["name"], GetCommand(3)["id"]),
                        value = "↪Відображає перелік усіх доступних команд бота з короткими описами для кожної команди",
                        inline = False
                    )
                    
                    await interaction.response.edit_message(embed = embed)
                
                # Description of the Moderation category menu
                if menu.values[0] == "2":
                    embed = discord.Embed(
                        title = f"Доступні команди категорії {menu.options[1].emoji} {menu.options[1].label}",
                        description = "Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою </{command_name}:{command_id}> `<command:name>`".format(command_name=GetCommand(3)["name"], command_id=GetCommand(3)["id"]),
                        color=HexToColor(config["bot"]["color"]["default"])
                    )
                    embed.set_thumbnail(url = config["bot"]["icon"])
                    embed.set_footer(
                        text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                        icon_url = config["bot"]["icon"]
                    )
                    
                    # Splitting each command of the category via discord.Embed.add_field()
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(6)["name"], GetCommand(6)["id"]),
                        value = "↪Виганяє зазначеного учасника з сервера.",
                        inline = False
                    )
                    
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(7)["name"], GetCommand(7)["id"]),
                        value = "↪Забороняє доступ зазначеному учаснику на сервер, видаючи йому бан.",
                        inline = False
                    )
                    
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(8)["name"], GetCommand(8)["id"]),
                        value = "↪Відображає список учасників, які отримали бан, разом із причинами їх блокування.",
                        inline = False
                    )
                    
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(9)["name"], GetCommand(9)["id"]),
                        value = "↪Знімає бан із зазначеного учасника, дозволяючи йому повернутися на сервер.",
                        inline = False
                    )
                    
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(10)["name"], GetCommand(10)["id"]),
                        value = "↪Тимчасово позбавляє учасника можливості писати повідомлення на сервері на вказаний період часу (до 28-и діб).",
                        inline = False
                    )
                    
                    embed.add_field(
                        name = "• </{0}:{1}>".format(GetCommand(11)["name"], GetCommand(11)["id"]),
                        value = "↪Знімає тимчасовий м'ют із зазначеного учасника, відновлюючи його можливість писати повідомлення на сервері.",
                        inline = False
                    )
                    
                    await interaction.response.edit_message(embed = embed)

            # Creating a view and adding the menu to it
            menu.callback = callback
            view = View()
            view.add_item(menu)

            
            embed = discord.Embed(
                title = "Доступні команди:",
                description="Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою </{0}:{1}> `<назва команди чи категорії>`. Або ж вибрати нижче категорію команд, щоб переглянути детальну інформацію про кожжну команду із вибраної категорії.".format(GetCommand(4)["name"], GetCommand(4)["id"]),
                color=HexToColor(config["bot"]["color"]["default"])
            )
            
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                icon_url = config["bot"]["icon"]
            )
            
            embed.add_field(
                name="📃 Інформація (</{command_help_name}:{command_help_id}> `<category:Information>)`".format(command_help_name = GetCommand(4)["name"], command_help_id = GetCommand(4)["id"]),
                value = "</{0}:{1}>".format(GetCommand(4)["name"], GetCommand(4)["id"]),
                inline = False
            )
            embed.add_field(
                name="🛡️ Модерація (</{command_help_name}:{command_help_id}> `<category:Moderation`)".format(command_help_name = GetCommand(4)["name"], command_help_id = GetCommand(4)["id"]),
                value = "</{0}:{1}> </{2}:{3}> </{4}:{5}> </{6}:{7}> </{8}:{9}> </{10}:{11}>".format(GetCommand(6)["name"], GetCommand(6)["id"], GetCommand(7)["name"], GetCommand(7)["id"], GetCommand(8)["name"], GetCommand(8)["id"], GetCommand(9)["name"], GetCommand(9)["id"], GetCommand(10)["name"], GetCommand(10)["id"], GetCommand(11)["name"], GetCommand(11)["id"]),
                inline = False
            )
            
            await interaction.response.send_message(embed = embed, view = view, ephemeral = True)
        elif command and category:
            embed = discord.Embed(
                title = "Помилка",
                description="Вибачте, але ви не можете використовувати обидва параметри одночасно. Будь ласка, використовуйте лише один параметр.",
                color=HexToColor(config["bot"]["color"]["error"])
            )
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                icon_url = config["bot"]["icon"]
            )
            
            await interaction.response.send_message(embed = embed, ephemeral = True)
        elif command == "help":
            embed = discord.Embed(
                title = "Перелік всіх команд та категорій",
                description = "Показує всі доступні команди та категорії бота",
                color=HexToColor(config["bot"]["color"]["default"])
            )
            
            embed.set_author(
                name = "Команда \"{0}\"".format(GetCommand(4)["name"])
            )
            embed.add_field(
                name = "Використання",
                value = "\"</{0}:{1}>\" `<command: назва команди>|<category: назва категорії>`".format(GetCommand(4)["name"], GetCommand(4)["id"]),
                inline = False
            )
            embed.add_field(
                name = "Приклад 1",
                value = "</{0}:{1}>\n┗Показує весь список команд".format(GetCommand(4)["name"], GetCommand(4)["id"]),
                inline = False
            )
            embed.add_field(
                name = "Приклад 2",
                value = "</{0}:{1}> `<category:Information>`\n┗Показує всі доступні команди категорії **📃Інформація**".format(GetCommand(4)["name"], GetCommand(4)["id"]),
                inline=False
            )
            embed.add_field(
                name='Приклад 3',
                value = "</{0}:{1}> `<command:help>`\n┗Показує детальну інформацію про команду </{2}:{3}> (*Ви зараз переглядаєте її*)".format(GetCommand(4)["name"], GetCommand(4)["id"], GetCommand(4)["name"], GetCommand(4)["id"])
            )
            embed.add_field(
                name='⠀',
                value='Примітка: в трикутних дужках відображається назва параметра, а після двох крапок те, що він приймає.',
                inline=False
            )
            
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                icon_url = config["bot"]["icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            embed = discord.Embed(
                title = "Попередження",
                description="Виниклая якась помилка, або такої команди немає чи її довідка ще не реалізована. Приносимо вибачення.",
                color=HexToColor(config["bot"]["color"]["warn"])
            )
            embed.set_thumbnail(url = config["bot"]["icon"])
            embed.set_footer(
                text = "Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year = datetime.now().year, dev_site_url = config["bot"]["site"]),
                icon_url = config["bot"]["icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
async def setup(bot):
    await bot.add_cog(HelpCommand(bot))
