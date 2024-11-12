import discord

from ganyu_utils import LoadJson, setup_logging, HexToColor, GetCommand, PagginationView
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
                        value="0",
                        emoji="📃"
                    ),
                    discord.SelectOption(
                        label="Модерація",
                        value="1",
                        emoji="🛡️"
                    )
                ]
            )

            async def callback(interaction: discord.Interaction):
                category_index = int(menu.values[0])
                category = menu.options[category_index]
                
                # We collect commands for the selected category
                commands = []
                if category.value == "0":  # Information category
                    commands = [
                        {"name": GetCommand(3)["name"], "id": GetCommand(3)["id"], "description": "Відображає перелік усіх доступних команд бота з короткими описами для кожної команди"}
                    ]
                elif category.value == "1":  # Moderation category
                    commands = [
                        {"name": GetCommand(6)["name"], "id": GetCommand(6)["id"], "description": "Виганяє зазначеного учасника з сервера."},
                        {"name": GetCommand(7)["name"], "id": GetCommand(7)["id"], "description": "Забороняє доступ зазначеному учаснику на сервер, видаючи йому бан."},
                        {"name": GetCommand(8)["name"], "id": GetCommand(8)["id"], "description": "Відображає список учасників, які отримали бан, разом із причинами їх блокування."},
                        {"name": GetCommand(9)["name"], "id": GetCommand(9)["id"], "description": "Знімає бан із зазначеного учасника, дозволяючи йому повернутися на сервер."},
                        {"name": GetCommand(10)["name"], "id": GetCommand(10)["id"], "description": "Тимчасово позбавляє учасника можливості писати повідомлення на сервері на вказаний період часу (до 28-и діб)."},
                        {"name": GetCommand(11)["name"], "id": GetCommand(11)["id"], "description": "Знімає тимчасовий м'ют із зазначеного учасника, відновлюючи його можливість писати повідомлення на сервері."}
                    ]

                # We divide the commands into pages if there are more than 10 of them
                pages = []
                for i in range(0, len(commands), 10):
                    embed = discord.Embed(
                        title=f"Доступні команди категорії {category.emoji} {category.label}",
                        description="Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою відповідного команди.",
                        color=HexToColor(config["bot"]["color"]["default"])
                    )
                    embed.set_thumbnail(url=config["bot"]["icon"])
                    embed.set_footer(
                        text="Mops Storage © 2020-{curent_year} Всі права захищено • {dev_site_url}".format(curent_year=datetime.now().year, dev_site_url=config["bot"]["site"]),
                        icon_url=config["bot"]["icon"]
                    )

                    # Add commands to the page
                    for command in commands[i:i+10]:
                        embed.add_field(
                            name=f"• </{command['name']}:{command['id']}>",
                            value=f"↪{command['description']}",
                            inline=False
                        )
                    pages.append(embed)

                # We check whether there are pages in "pages"
                if pages:
                    # If there is more than one page, we use pagination
                    if len(pages) > 1:
                        menu.callback = callback
                        await interaction.response.edit_message(embed=pages[0], view=PagginationView(pages, menu))
                    else:
                        # If there is only one page, we display it without pagination
                        view = View()
                        if menu:  # Add select if it is needed
                            view.add_item(menu)
                        await interaction.response.edit_message(embed=pages[0], view=view)
                else:
                    # If the list of pages is empty, we display a message about the absence of commands
                    embed = discord.Embed(
                        title="Команди не знайдені",
                        description="Для обраної категорії немає доступних команд.",
                        color=HexToColor(config["bot"]["color"]["default"])
                    )
                    await interaction.response.edit_message(embed=embed)


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
