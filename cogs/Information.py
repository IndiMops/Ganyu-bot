from discord.ext import commands, tasks
from discord.ui import Select, View
import discord
import sqlite3
import time
from discord import app_commands
import typing
import requests
from ganyu import *
import datetime
import asyncio
import random

data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()
config = LoadJson('config.json')

class Information(commands.Cog):
    """information module"""
    def __init__(self, bot):
        self.bot = bot
        """self.user_info = app_commands.ContextMenu(
            name = GetMsg("context_command_user_name"),
            callback = self.user_info_callback
        )
        self.bot.tree.add_command(self.user_info)
        """  
        

    @commands.Cog.listener()
    async def on_ready(self):
        global start_time
        start_time = int(time.time())
    
    @app_commands.command(name = 'help', description = GetMsg("command_descriptions_help"))
    async def help(self, interaction: discord.Interaction, command: str = None):
        if command == None:
            menu = Select(
                placeholder = GetMsg("select_component_placeholder", interaction.guild),
                options = [
                    discord.SelectOption(
                        label = GetMsg("command_help_selection_options_label_information", interaction.guild),
                        value = '1',
                        emoji = '📃'
                    ),
                    discord.SelectOption(
                        label = GetMsg("command_help_selection_options_label_ranking", interaction.guild),
                        value = '2',
                        emoji = '🏆'
                    )
                ]
            )
            
            async def callback(interaction: discord.Integration):
                if menu.values[0] == '1':
                    embed = discord.Embed(
                        title = GetMsg("command_help_information_embed_title", interaction.guild),
                        description = GetMsg("commandd_help_inforation_embed_descriptions", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]),
                        color = StrToColor(config['color_default'])
                    )
                    embed.set_thumbnail(
                        url = config["bot_icon"]
                    )
                    embed.set_footer(
                        text = GetMsg("footer_copyright_with_link", interaction.guild).format(datetime.datetime.now().year, config["dev"]["site"]),
                        icon_url = config["bot_icon"]
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(0)["name"], GetCommand(0)["id"]),
                        value = GetMsg("command_help_information_help_descriptions", interaction.guild),
                        inline = False
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(1)["name"], GetCommand(1)["id"]),
                        value = GetMsg("command_help_information_info_descriptions", interaction.guild).format(config["bot_name"]),
                        inline = False
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(2)["name"], GetCommand(2)["id"]),
                        value = GetMsg("command_help_information_stats_descriptions", interaction.guild).format(config["bot_name"]),
                        inline = False
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(3)["name"], GetCommand(3)["id"]),
                        value = GetMsg("command_help_information_server_descriptions", interaction.guild).format(config["bot_name"]),
                        inline = False
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(4)["name"], GetCommand(4)["id"]),
                        value = GetMsg("command_help_information_user_descriptions", interaction.guild),
                        inline = False
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(5)["name"], GetCommand(5)["id"]),
                        value = GetMsg("command_help_information_bio_descriptions", interaction.guild),
                        inline = False
                    )
                    await interaction.response.send_message(embed = embed)
                    
                if menu.values[0] == '2':
                    embed = discord.Embed(
                        title = GetMsg("command_help_ranking_embed_title", interaction.guild),
                        description = GetMsg("commandd_help_inforation_embed_descriptions", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]),
                        color = StrToColor(config['color_default'])
                    )
                    embed.set_thumbnail(
                        url = config["bot_icon"]
                    )
                    embed.set_footer(
                        text = GetMsg("footer_copyright_with_link", interaction.guild).format(datetime.datetime.now().year, config["dev"]["site"]),
                        icon_url = config["bot_icon"]
                    )
                    embed.add_field(
                        name = "</{0}:{1}>".format(GetCommand(6)["name"], GetCommand(6)["id"]),
                        value = GetMsg("command_help_ranking_card_descriptions", interaction.guild),
                        inline = False
                    )
                    
                    await interaction.response.send_message(embed = embed)
                
            menu.callback = callback
            view = View()
            view.add_item(menu)
            
            embed = discord.Embed(
                title = GetMsg("title_avalible_commands", interaction.guild),
                description = GetMsg("commandd_help_inforation_embed_descriptions", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]),
                color = StrToColor(config['color_default'])
                )
            embed.set_thumbnail(url = config["bot_icon"])
            embed.set_footer(
                text = GetMsg("footer_copyright_with_link", interaction.guild).format(datetime.datetime.now().year, config["dev"]["site"]),
                icon_url = config["bot_icon"]
                )
            embed.add_field(
                name = GetMsg("command_help_embed_title_information", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]),
                value = "</{0}:{1}> </{2}:{3}> </{4}:{5}> </{6}:{7}> </{8}:{9}> </{10}:{11}>".format(GetCommand(0)["name"], GetCommand(0)["id"], GetCommand(1)["name"], GetCommand(1)["id"], GetCommand(2)["name"], GetCommand(2)["id"], GetCommand(3)["name"], GetCommand(3)["id"], GetCommand(4)["name"], GetCommand(4)["id"], GetCommand(5)["name"], GetCommand(5)["id"]),
                inline = False
                )
            embed.add_field(
                name = GetMsg("command_help_embed_title_ranking", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]),
                value = '</{0}:{1}> </{2}:{3}> </{4}:{5}> </{6}:{7}>'.format(GetCommand(6)["name"], GetCommand(6)["id"], GetCommand(7)["name"], GetCommand(7)["id"], GetCommand(8)["name"], GetCommand(8)["id"], GetCommand(9)["name"], GetCommand(9)["id"]),
                inline = False
                )
            
            await interaction.response.send_message(embed = embed, view = view)
        elif command == 'help':
            embed = discord.Embed(
                title='Перелік всіх команд та категорій',
                description='Показує всі доступні команди та категорії бота',
                color=StrToColor(config['color_default'])
            )
            
            embed.set_author(
                name=f'Команда "{config["bot_prefix"]}help"'
            )
            embed.add_field(
                name='Використання',
                value=f'{config["bot_prefix"]}help `<command: назва команди чи категорії>`',
                inline=False
            )
            embed.add_field(
                name='Приклад 1',
                value=f'{config["bot_prefix"]}help\n┗Показує весь список команд',
                inline=False
            )
            embed.add_field(
                name='Приклад 2',
                value=f'{config["bot_prefix"]}help `<command:information>`\n┗Показує всі доступні команди категорії **📃Інформація**',
                inline=False
            )
            embed.add_field(
                name='Приклад 3',
                value=f'{config["bot_prefix"]}help `<command:help>`\n┗Показує детальну інформацію про команду **{config["bot_prefix"]}help** (!Ви зараз переглядаєте її!)'
            )
            embed.add_field(
                name='⠀',
                value='Примітка: в трикутних дужках відображається назва параметра, а після двох крапок те, що від приймає',
                inline=False
            )
            
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'info':
            embed = discord.Embed(
                title=f'Корисна інформація про {config["bot_name"]}',
                description=f'Показує корисну інформацію про {config["bot_name"]} (версія, автор, посилання на ресурси і т.д.)',
                color=StrToColor(config['color_default'])
            )
            
            embed.set_author(
                name=f'Команда "{config["bot_prefix"]}info"'
            )
            embed.add_field(
                name='Використання',
                value=f'{config["bot_prefix"]}info',
                inline=False
            )
            
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'stats':
            embed = discord.Embed(
                title=f'Статистика використання {config["bot_name"]}',
                description=f'Показує загальну статистику {config["bot_name"]}, таку як: кількість серверів, учасників використаних команд і т.д',
                color=StrToColor(config['color_default'])
            )
            
            embed.set_author(
                name=f'Команда "{config["bot_prefix"]}stats"'
            )
            embed.add_field(
                name='Використання',
                value=f'{config["bot_prefix"]}stats',
                inline=False
            )
            
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'server':
            embed = discord.Embed(
                title='Інформація про сервер',
                description='Відображає інформацію про сервер де була введена команда.',
                color=StrToColor(config['color_default'])
            )
            
            embed.set_author(
                name=f'Команда "{config["bot_prefix"]}server"'
            )
            embed.add_field(
                name='Використання',
                value=f'{config["bot_prefix"]}server',
                inline=False
            )
            
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'user':
            embed = discord.Embed(
                title='Інформація про користувача',
                description='Відображає інформацію про користувача',
                color=StrToColor(config['color_default'])
            )
            
            embed.set_author(
                name=f'Команда "{config["bot_prefix"]}user"'
            )
            embed.add_field(
                name='Використання',
                value=f'{config["bot_prefix"]}user `<user:користувача у форматі @username>`',
                inline=False
            )
            embed.add_field(
                name='Приклад 1',
                value=f'{config["bot_prefix"]}user\n┗Відображає інформацію, того хто надіслав команду',
                inline=False
            )
            embed.add_field(
                name='Приклад 2',
                value=f'{config["bot_prefix"]}user `<user:@Ganyu>`\n┗Відображає інформацію про користувача, якого вказант в параметрі',
                inline=False
            )
            embed.add_field(
                name='Приклад 3',
                value=f'Використання застосунка через контекстне меню натиснувши на правою клавішою миші по користувача(на телеофні просто зажміть ім\'я користувача)',
                inline=False
            )
            embed.add_field(
                name='⠀',
                value='Примітка: в трикутних дужках відображається назва параметра, а після двох крапок те, що від приймає',
                inline=False
            )
            
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'bio':
            embed = discord.Embed(
                title='Встановити біографію',
                description='Дозволяє встановити біографію, або відобразити біографію',
                color=StrToColor(config['color_default'])
            )
            
            embed.set_author(
                name=f'Команда "{config["bot_prefix"]}bio"'
            )
            embed.add_field(
                name='Використання',
                value=f'{config["bot_prefix"]}bio `<user:користувач у форматі @username>` `<bio:текст біографії>`',
                inline=False
            )
            embed.add_field(
                name='Приклад 1',
                value=f'{config["bot_prefix"]}bio\n┗Відображає біографію, того хто відправив команду',
                inline=False
            )
            embed.add_field(
                name='Приклад 2',
                value=f'{config["bot_prefix"]}bio `<bio:Моя біографія>`\n┗Встановити біграфію',
                inline=False
            )
            embed.add_field(
                name='Приклад 3',
                value=f'{config["bot_prefix"]}bio `<bio:->`\n┗Очистити біграфію',
                inline=False
            )
            embed.add_field(
                name='Приклад 4',
                value=f'{config["bot_prefix"]}bio `<user:користувач у форматі @username>` `<bio:Біографія користувача>`\n┗Встановлює біографію вибраному користувачу',
                inline=False
            )
            embed.add_field(
                name='Приклад 5',
                value=f'{config["bot_prefix"]}bio `<user:користувач у форматі @username>` `<bio:->`\n┗Очистити біографію вибраному користувачу',
                inline=False
            )
            
            embed.add_field(
                name='⠀',
                value='Примітка: в трикутних дужках відображається назва параметра, а після двох крапок те, що від приймає',
                inline=False
            )
            
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'Information':
            embed = discord.Embed(
                title='Доступні команди категорії 📃Інформація',
                description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {config["bot_prefix"]}help `<command:назва команди чи категорії>`',
                color=StrToColor(config['color_default'])
            )
            embed.set_thumbnail(
                url=config["bot_icon"]
            )
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}help',
                value='Перелік всіх команд та категорій',
                inline=False
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}info',
                value=f'Корисна інформація про {config["bot_name"]}',
                inline=False
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}stats',
                value=f'Статистика використання {config["bot_name"]}',
                inline=False
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}server',
                value='Інформація про поточний сервер',
                inline=False
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}user',
                value='Інформація про учасника',
                inline=False
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}bio',
                value='Встановити біографію',
                inline=False
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif command == 'Ranking':
            embed = discord.Embed(
                title='Доступні команди категорії 💰Економіка',
                description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {config["bot_prefix"]}help `<command:назва команди чи категорї>`',
                color=StrToColor(config['color_default'])
            )
            embed.set_thumbnail(
                url=config["bot_icon"]
            )
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
            )
            embed.add_field(
                name=f'{config["bot_prefix"]}card `<користувач>`',
                value='Виводить інформацію про рівень користувача',
                inline=False
            )
                    
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(embed = discord.Embed(title = GetMsg("error_general_title", interaction.guild), description = GetMsg("error_missing_command_or_category").format(GetCommand(0)["name"], GetCommand(0)["id"]), color = config["color_error"]))
    
    @help.autocomplete("command")
    async def help_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        
        names = [command['name'] for command in config.get('bot_commands', {}).values()]
        
        names.sort()

        if len(names) > 25:
            names = random.sample(names, 25)
        
        command = names
        
        return [
            app_commands.Choice(name = command, value = command)
            for command in command if current.lower() in command.lower()
        ]   
    
    @app_commands.command(name = 'info', description = GetMsg("command_help_information_info_descriptions").format(config['bot_name']))
    async def info_(self, interaction: discord.Interaction):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        embed = discord.Embed(
            title = config["bot_name"],
            description = GetMsg("command_info_embed_descriptions", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"], GetCommand(10)["name"], GetCommand(10)["id"],),
            color = StrToColor(config['color_default'])
        )
        
        embed.set_thumbnail(url = config["bot_icon"])
        embed.set_footer(
            text = GetMsg("footer_copyright_with_link", interaction.guild).format(datetime.datetime.now().year, config["dev"]["site"]),
            icon_url = config["bot_icon"]
        )
        
        embed.add_field(
            name = GetMsg("command_info_bot_build", interaction.guild),
            value = '{0} (<t:{1}:d>)'.format(config["bot_version"], config["bot_last_updated"])
        )
        embed.add_field(
            name = GetMsg("command_info_bot_developer", interaction.guild),
            value = '{0} [{1}](https://discord.com/users/{2})'.format(config["dev"]["emoji"], config["dev"]["name"], config["dev"]["id"])
        )
        # This empty field is needed to align all the fields, or if you ever have additional information, you can add it here
        embed.add_field(
            name = '⠀',
            value = '⠀'
        )
        embed.add_field(
            name = GetMsg("command_info_links", interaction.guild),
            value = GetMsg("command_info_links_text1", interaction.guild).format(config["bot_site"], config["other_links"]["support_server"])
        )
        embed.add_field(
            name = '⠀',
            value = GetMsg("command_info_links_text2").format(config["other_links"]["github_repo"], config["other_links"]["top.gg"])
        )
        embed.add_field(
            name = '⠀',
            value = '[Patreon]({0})\n[Diaka]({1})'.format(config["other_links"]["patreon"], config["other_links"]["diaka"])
        )
        await interaction.response.send_message(embed = embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @app_commands.command(name = 'stats', description = GetMsg("command_help_information_stats_descriptions").format(config["bot_name"]))
    async def stats_(self, interaction: discord.Interaction):
        ping = self.bot.latency
        for row in cur.execute(f'SELECT guilds, users, channels, commands FROM stats_bot'):
            StBguilds = row[0]
            StBusers = row[1]
            StBchannels = row[2]
            StBcommands = row[3]
          
        embed = discord.Embed(
            title = GetMsg("command_stats_embed_title", interaction.guild).format(config["bot_name"]),
            color = StrToColor(config['color_default'])
            )
        embed.set_thumbnail(url = config["bot_icon"])
        embed.set_footer(
            text = GetMsg("footer_copyright_with_link", interaction.guild).format(datetime.datetime.now().year, config["dev"]["site"]),
            icon_url = config["bot_icon"]
        )
        
        embed.add_field(
            name = GetMsg("command_stats_general_title", interaction.guild),
            value = GetMsg("command_stats_general_descriptions", interaction.guild).format("{0:,}".format(StBguilds).replace(",", " "), "{0:,}".format(StBusers).replace(",", " "), "{0:,}".format(StBchannels).replace(",", " "))
        )
        embed.add_field( 
            name = GetMsg("command_stats_platform_title", interaction.guild),
            value = GetMsg("command_stats_platform_descriptions", interaction.guild).format("{0:,}".format(StBcommands + 1).replace(",", " "), int(ping * 1000), start_time)
        )
        
        await interaction.response.send_message(embed = embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @app_commands.command(name = 'server', description = GetMsg("command_help_information_server_descriptions"))
    async def server_(self, interaction: discord.Interaction):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        
        text_channels = len(interaction.guild.text_channels)
        voice_channels = len(interaction.guild.voice_channels)
        stage_channels = len(interaction.guild.stage_channels)
        total_channels = text_channels + voice_channels + stage_channels
        
        total = len(interaction.guild.members)
        online = len(list(filter(lambda m: str(m.status) == "online", interaction.guild.members)))
        idle = len(list(filter(lambda m: str(m.status) == "idle", interaction.guild.members)))
        offline = len(list(filter(lambda m: str(m.status) == "offline", interaction.guild.members)))
        humans = len(list(filter(lambda m: not m.bot, interaction.guild.members)))
        bots = len(list(filter(lambda m: m.bot, interaction.guild.members)))
        
        snsfwlvl = str(interaction.guild.explicit_content_filter)
        if snsfwlvl == "all_members":
            snsfwlvl = GetMsg("command_server_content_filter_all", interaction.guild)
        elif snsfwlvl == "no_role":
            snsfwlvl = GetMsg("command_server_content_filter_no_role", interaction.guild)
        elif snsfwlvl == "disabled":
            snsfwlvl = GetMsg("command_server_content_filter_disabled", interaction.guild)
        else:
            snsfwlvl = GetMsg("command_server_content_filter_not_found", interaction.guild)
        
        embed = discord.Embed(
            title = GetMsg("command_server_embed_title", interaction.guild).format(interaction.guild.name),
            color = StrToColor(config['color_default'])
        )
        
        schannel_rules = str(interaction.guild.rules_channel)
        if schannel_rules == "None":
            schannel_rules = GetMsg("command_server_channel_rules_none", interaction.guild)
        else:
            schannel_rules = f"<#{interaction.guild.rules_channel.id}>"
        
        sverification = str(interaction.guild.verification_level)
        if sverification == "extreme":
            sverification = GetMsg("command_server_verification_level_extreme", interaction.guild)
        elif sverification == "high":
            sverification = GetMsg("command_server_verification_level_high", interaction.guild)
        elif sverification == "medium":
            sverification = GetMsg("command_server_verification_level_medium", interaction.guild)
        elif sverification == "low":
            sverification = GetMsg("command_server_verification_level_low", interaction.guild)
        elif sverification == "none":
            sverification = GetMsg("command_server_verification_level_none", interaction.guild)
        else:
            sverification = GetMsg("command_server_verification_level_not_found", interaction.guild)
        
        def GetChannelCount(key:str, my_tuple: tuple = interaction.guild.channels):
            """
            Returns the value of the key key in the dictionary, which contains the number of channels of each type.
            :param key: - The key whose value is to be returned. Can be 'TotalChannels' or channel type. Example: TotalChannels, TextChannel, CategoryChannel, VoiceChannel, ForumChannel'
            :param my_tuple: - Tuple with channel objects.
            :return: - The value of the key in the channels_count dictionary.
            """
            channels_count = {"TotalChannels": 0}

            for obj in my_tuple:
                obj_type = type(obj).__name__

                if obj_type in channels_count:
                    channels_count[obj_type] += 1
                else:
                    channels_count[obj_type] = 1

                if obj_type != "CategoryChannel":
                    channels_count["TotalChannels"] += 1

            # Перевірте, чи ключ існує в словнику
            if key in channels_count:
                return channels_count[key]
            else:
                return None

        
        created_at = interaction.guild.created_at
        embed.add_field(
            name = GetMsg("command_server_owner", interaction.guild), 
            value = interaction.guild.owner.mention,
            inline = True
            )
        
        embed.add_field(
            name = "ID", 
            value = interaction.guild.id, 
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_created", interaction.guild), 
            value = f'<t:{int(created_at.timestamp())}:f>', 
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_channel_rules", interaction.guild),
            value = schannel_rules,
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_content_filter", interaction.guild), 
            value = snsfwlvl,
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_verification_level", interaction.guild),
            value = sverification,
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_members", interaction.guild), 
            value = GetMsg("command_server_members_value", interaction.guild).format(total, humans, bots),
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_status", interaction.guild), 
            value = GetMsg("command_server_status_value").format(online, idle, offline), 
            inline = True
            )
        
        embed.add_field(
            name = GetMsg("command_server_channels", interaction.guild), 
            value = GetMsg("command_server_channels_value", interaction.guild).format(GetChannelCount("TotalChannels"), GetChannelCount("TextChannel"), GetChannelCount("VoiceChannel"))
            )
        
        embed.set_thumbnail(url = interaction.guild.icon)
        
        
        
        await interaction.response.send_message(embed = embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()

    @app_commands.command(name = 'user', description = GetMsg("command_help_information_user_descriptions"))
    async def user_(self, interaction: discord.Interaction, *, user: discord.Member = None,):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        if user is None:
            user = interaction.user
            
        for bio in cur.execute(f'SELECT bio FROM users WHERE id = {user.id}'):
            if bio[0] == 'None':
                bio = GetMsg("", interaction.guild).format(GetCommand(5), GetCommand(5))
        headers = {"Authorization": f"Bot {config['bot_token']}"}
        req = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers = headers).json()
        
        def rgb(hex):
            rgb = []
            for i in (0, 2, 4):
                decimal = int(hex[i:i+2], 16)
                rgb.append(decimal)
            return rgb
        
        bio = bio[0]
        cut = (bio[:150] + '...') if len(bio) > 150 else bio
        
        if req['banner_color'] is None:
            embed = discord.Embed(description = cut, color = StrToColor(config['color_default']))
        else:
            embed = discord.Embed(description = cut, color = discord.Color.from_rgb(rgb(req['banner_color'].replace('#', ''))[0], rgb(req['banner_color'].replace('#', ''))[1], rgb(req['banner_color'].replace('#', ''))[2]))
        
        #global user_status
        user_status = interaction.guild.get_member(user.id).status
        if user_status == discord.Status.online:
            user_status = GetMsg("command_user_user_online", interaction.guild)
        elif user_status == discord.Status.offline or user_status == discord.Status.invisible:
            user_status = GetMsg("command_user_user_offline", interaction.guild)
        elif user_status == discord.Status.idle:
            user_status = GetMsg("command_user_user_idle", interaction.guild)
        elif user_status == discord.Status.dnd or user_status == discord.Status.do_not_disturb:
            user_status = GetMsg("command_user_user_dnd", interaction.guild)

        global ca, spotify, game
        ca = ''
        spotify = ''
        game = ''
        for active in interaction.guild.get_member(user.id).activities:
            if isinstance(active, discord.CustomActivity):
                global ca_emoji_type, ca_emoji_id
                ca_emoji_type = ''
                ca_emoji_id = ''
                if active.emoji is None: # Checks whether the user status is emoji
                    pass
                else:
                    if active.emoji.animated is True: # Checks whether emoji is animated
                        ca_emoji_type = 'a'
                    ca_emoji_name = active.emoji.name
                    ca_emoji_id = active.emoji.id
                ca_name = active.name
                global ca_emoji
                ca_emoji = None
                if self.bot.get_emoji(ca_emoji_id) == None:# Can a bot to reflect that emoji
                    ca_emoji = ''
                else:
                    ca_emoji =  f'<{ca_emoji_type}:{ca_emoji_name}:{ca_emoji_id}>'

                if ca_name is None:
                    if self.bot.get_emoji(ca_emoji_id) == None:
                        ca = ''
                    else:
                        ca = GetMsg("command_user_custom_status_emoji", interaction.guild).format(ca_emoji)
                else:
                    ca = GetMsg("command_user_custom_status", interaction.guild).format(ca_emoji, ca_name)

            if isinstance(active, discord.Spotify):
                artist = active.artist
                if len(artist.split('; ')) > 1:
                    artist = artist.split('; ')
                    artist = ", ".join(artist)
                else:
                    artist = artist.replace(' ', '_')
                    artist = f'[{active.artist}](https://open.spotify.com/search/{artist})'
                        
                spotify = GetMsg("command_user_status_spotify", interaction.guild).format(active.title, active.track_id, artist)
            
            if isinstance(active, discord.Game):
                game = GetMsg("", interaction.guild).format(active.name)
        
        nick = ''
        if user.nick is not None:
            nick = GetMsg("command_user_nickname", interaction.guild).format(user.nick)
          
        embed.add_field(
            name = GetMsg("command_user_main_category", interaction.guild),
            value = GetMsg("command_user_main_category_text", interaction.guild).format(user.name, nick, user_status, ca, spotify, game, int(user.joined_at.timestamp()), int(user.created_at.timestamp()))
        )
        
        embed.set_author(
            name = GetMsg("command_user_subtitle", interaction.guild).format(user.name),
            icon_url = user.avatar
        )
        
        embed.set_thumbnail(
            url = user.avatar
        )
        
        if req['banner'] is None:
            embed.set_image(
                url = config["bot_banner"]
            )
        else:
            embed.set_image(
            url = f'https://cdn.discordapp.com/banners/{user.id}/{req["banner"]}?size=2048'
        )
        
        embed.set_footer(
            text = 'ID: {0}'.format(user.id)
        )
        
        await interaction.response.send_message(embed = embed, ephemeral = True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()  

    # create group for bio commands
    bio_commands = app_commands.Group(name = 'bio', description = "Group bio commands")
    
    @bio_commands.command(name = "view", description = GetMsg("command_bio_view_description"))
    async def bio_view(self, interaction: discord.Interaction, user: discord.User = None):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        if user is None:
            user = interaction.user # set target user what send command
            
        # get bio from DB
        for row in cur.execute(f'SELECT bio FROM users WHERE id = {user.id}'):
            db_bio = row[0]
        
        # if bio is not in DB, return hint
        if db_bio == 'None':
            embed = discord.Embed(
                title = GetMsg("error_general_title", interaction.guild),
                description = GetMsg("command_bio_not_found_bio", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]),
                color = StrToColor(config['color_error'])
            )
            await interaction.response.send_message(embed = embed, ephemeral = True)
        else:
            # Checking whether user has a nickname in server
            if user.nick is None:
                name = user.name
            else:
                name = user.nick

            embed = discord.Embed(
                title = GetMsg("command_bio_embed_title", interaction.guild).format(name),
                description = db_bio,
                color = StrToColor(config['color_default'])
            )
                    
            embed.set_thumbnail(
                url = user.avatar
            )
            await interaction.response.send_message(embed = embed, ephemeral = True)
        # where command has completed
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    
    @bio_commands.command(name = "set", description = GetMsg("command_bio_set_description"))
    async def bio_set(self, interaction: discord.Interaction, text: str):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        for row in cur.execute(f'SELECT bio FROM users WHERE id = {interaction.user.id}'):
            bio = row[0]
        
        cur.execute(f'UPDATE users SET bio = "{text}" WHERE id = {interaction.user.id}')
        data.commit
        
        if bio == "None" or bio is None:
            description = GetMsg("command_bio_set_embed_description_none", interaction.guild).format(text)
        else:
            description = GetMsg("command_bio_set_embed_description", interaction.guild).format(text)
        
        embed = discord.Embed(
            title = GetMsg("command_bio_set_embed_title", interaction.guild),
            description = description,
            color = StrToColor(config['color_ok'])
        )
        embed.set_thumbnail(
            url = interaction.user.avatar
        )
        await interaction.response.send_message(embed = embed, ephemeral = True)
        
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    
    @bio_commands.command(name = "reset", description = GetMsg("command_bio_reset_description"))
    async def bio_reset(self, interaction: discord.Interaction):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
            
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        
        try: 
            cur.execute(f'UPDATE users SET bio = Null WHERE id = {interaction.user.id}')
            
            embed = discord.Embed(
                title = GetMsg("success_title", interaction.guild),
                description = GetMsg("command_bio_reset_embed_description", interaction.guild),
                color = StrToColor(config["color_ok"])
            )
            
            await interaction.response.send_message(embed = embed, ephemeral = True)
        except Exception as e:
            embed = discord.Embed(
                title = GetMsg("error_general_title", interaction.guild),
                description = GetMsg("error_command_general_description", interaction.guild),
                color = StrToColor(config["color_error"])
            )
            await interaction.response.send_message(embed = embed, ephemeral = True)
            print(GetMsg("error_command_general_description_console").format(interaction.guild.name, interaction.guild.id, e))
            
        data.commit

async def setup(bot):
    await bot.add_cog(Information(bot))