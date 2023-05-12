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

data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()
config = LoadJson('config.json')

class Information(commands.Cog):
    """information module"""
    def __init__(self, bot):
        self.bot = bot
        self.user_info = app_commands.ContextMenu(
            name='Інформація',
            callback=self.user_info_callback
        )
        self.bot.tree.add_command(self.user_info)    
        

    @commands.Cog.listener()
    async def on_ready(self):
        print('Information commands - Ready!')
        global start_time
        start_time = int(time.time())
    
    @app_commands.command(name='help', description='Команда довідка')
    async def help(self, interaction: discord.Interaction, command: str = None):
        if command == None:
            menu = Select(
                placeholder='Виберіть категорію...',
                options=[
                    discord.SelectOption(
                        label='Інформація',
                        value='1',
                        emoji='📃'
                    ),
                    discord.SelectOption(
                        label='Економіка',
                        value='2',
                        emoji='💰'
                    )
                ]
            )
            
            async def callback(interaction:discord.Integration):
                if menu.values[0] == '1':
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
                    
                if menu.values[0] == '2':
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
                
            menu.callback = callback
            view = View()
            view.add_item(menu)
            
            embed=discord.Embed(
                title='Доступні команди:',
                description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {config["bot_prefix"]}help `<command:назва команди чи категорії>`',
                color=StrToColor(config['color_default'])
                )
            embed.set_thumbnail(url=config["bot_icon"])
            embed.set_footer(
                text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
                icon_url=config["bot_icon"]
                )
            embed.add_field(
                name=f'📃Information (`{config["bot_prefix"]}help <command:Information>)`',
                value=f'`{config["bot_prefix"]}help` `{config["bot_prefix"]}info` `{config["bot_prefix"]}stats` `{config["bot_prefix"]}server` `{config["bot_prefix"]}user` `{config["bot_prefix"]}bio`',
                inline=False
                )
            embed.add_field(
                name=f'💰Економіка (`{config["bot_prefix"]}help <command:Economy>)`',
                value=f'`{config["bot_prefix"]}card` `{config["bot_prefix"]}set_xp` `{config["bot_prefix"]}set_lvl`',
                inline=False
                )
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
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
        elif command == 'Economy':
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
            await interaction.response.send_message(embed=discord.Embed(title='Помилка', description=f'Такої команди чи категорії немає!\nПерегляньте команди за допомгою: {config["bot_prefix"]}help', color=0xff0000), ephemeral=True)
    
    @help.autocomplete("command")
    async def help_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        for command_choice in ['help', 'info', 'stats', 'server', 'user', 'bio']:
            if current.lower() in command_choice.lower():
                data.append(app_commands.Choice(name=command_choice, value=command_choice))
        return data    
    
    @app_commands.command(name='info', description=f'Корисна інформація про {config["bot_name"]}')
    async def info_(self, interaction: discord.Interaction):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        embed = discord.Embed(
            title=config["bot_name"],
            description=f'Привіт, я Ґанью секретарка Цісін в Ліюе. Моє завдання допомагати мандрівникам освоюватися з дивовижним світом Тейват\n\nМій префікс `{config["bot_prefix"]}`. Якщо ти хочеш дізнатися всі мої команди тоді можеш скористатися **{config["bot_prefix"]}help**. Або скористайся **{config["bot_prefix"]}starjour**, щоб розпочати свою подорож<a:ganyuroll:1037043774850867241>',
            color=StrToColor(config['color_default'])
        )
        
        embed.set_thumbnail(url=config["bot_icon"])
        embed.set_footer(
            text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
            icon_url=config["bot_icon"]
        )
        
        embed.add_field(
            name='Збірка:',
            value=f'{config["bot_version"]} (<t:1666194420:d>)'
        )
        embed.add_field(
            name='Мій розробник:',
            value='<:dev:1037048854190772295> [Indi Mops#0424](https://discord.com/users/734082410504781854)'
        )
        embed.add_field(
            name='⠀',
            value='⠀'
        )
        embed.add_field(
            name='Корисні посилання:',
            value=f'[Веб-сайт]({config["bot_site"]})\n[Сервер підтримки]({config["other_links"]["support_server"]})'
        )
        embed.add_field(
            name='⠀',
            value=f'[GitHub репозиторій]({config["other_links"]["github_repo"]})\n[top.gg]({config["other_links"]["top.gg"]})'
        )
        embed.add_field(
            name='⠀',
            value=f'[Patreon]({config["other_links"]["patreon"]})\n[Diaka]({config["other_links"]["diaka"]})'
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @app_commands.command(name='stats', description=f'Статистика {config["bot_name"]}')
    async def stats_(self, interaction: discord.Interaction):
        """Перевіряє чи працює Cog система"""
        ctx = await self.bot.get_context(interaction)
        ping = self.bot.latency
        for row in cur.execute(f'SELECT guilds, users, channels, commands FROM stats_bot'):
            StBguilds = row[0]
            StBusers = row[1]
            StBchannels = row[2]
            StBcommands = row[3]
          
        embed = discord.Embed(
            title=f'Статистика {config["bot_name"]}',
            color=StrToColor(config['color_default'])
            )
        embed.set_thumbnail(url=config["bot_icon"])
        embed.set_footer(
            text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
            icon_url=config["bot_icon"]
        )
        
        embed.add_field(
            name='Основна',
            value=f'Сервери: {"{0:,}".format(StBguilds).replace(",", " ")}\nКористувачів: {"{0:,}".format(StBusers).replace(",", " ")}\nКаналів: {"{0:,}".format(StBchannels).replace(",", " ")}'
        )
        embed.add_field( 
            name='Платформена',
            value=f'Команд використано: {"{0:,}".format(StBcommands + 1).replace(",", " ")}\nЗатримка: {round(ping, 2)} мс.\nЗапущений: <t:{start_time}:R>'
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    @app_commands.command(name='server', description='Детальна інформація про сервер')
    async def server_(self, interaction: discord.Interaction):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        ctx = await self.bot.get_context(interaction)
        text_channels = len(ctx.guild.text_channels)
        voice_channels = len(ctx.guild.voice_channels)
        stage_channels = len(ctx.guild.stage_channels)
        total_channels = text_channels + voice_channels + stage_channels
        
        total = len(ctx.guild.members)
        online = len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members)))
        idle = len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members)))
        dnd = len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members)))
        offline = len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))
        humans = len(list(filter(lambda m: not m.bot, ctx.guild.members)))
        bots = len(list(filter(lambda m: m.bot, ctx.guild.members)))
        
        snsfwlvl = str(ctx.guild.explicit_content_filter)
        if snsfwlvl == "all_members":
            snsfwlvl = "Перевіряти кожного учасника"
        elif snsfwlvl == "no_role":
            snsfwlvl = "Перевіряти учасників без ролей"
        elif snsfwlvl == "disabled":
            snsfwlvl = "Не встановлено"
        else:
            snsfwlvl = "Не знайдено"
        
        embed = discord.Embed(
            color = StrToColor(config['color_default']),
            title = f"Інформація про сервер {ctx.guild.name}"
        )
        
        schannel_rules = str(ctx.guild.rules_channel)
        if schannel_rules == "None":
            schannel_rules = "Немає"
        else:
            schannel_rules = f"<#{ctx.guild.rules_channel.id}>"
        
        sverification = str(ctx.guild.verification_level)
        if sverification == "extreme":
            sverification = "Найвищий"
        elif sverification == "high":
            sverification = "Високий"
        elif sverification == "medium":
            sverification = "Середній"
        elif sverification == "low":
            sverification = "Низький"
        elif sverification == "none":
            sverification = "Не встановлений"
        else:
            sverification = "Не знайдено"
        
        created_at = ctx.guild.created_at
        embed.add_field(
            name = "Власник сервера", 
            value = ctx.guild.owner.mention,
            inline = True
            )
        embed.add_field(
            name = "Id", 
            value = ctx.guild.id, 
            inline = True
            )
        embed.add_field(
            name = "Створений: ", 
            value = f'<t:{int(created_at.timestamp())}:f>', 
            inline = True
            )
        embed.add_field(
            name = "Канал з правилами:",
            value = schannel_rules,
            inline = True)
        embed.add_field(
            name = "Перевірка:", 
            value = snsfwlvl,
            inline = True
            )
        embed.add_field(
            name = "Рівень модерації:",
            value = sverification,
            inline = True)
        embed.add_field(
            name = "Учасники:", 
            value = f'<:total_members:1038376493669154836> Всього: **{total}**\n<:members:1038376476870979594> Учасників: **{humans}**\n<:bots:1038376472521482263> Ботів: **{bots}**',
            inline = True
            )
        embed.add_field(
            name = "Статуси:", 
            value = f"<:online:1038376483758030898>Онлайн: **{online}**\n<:idle:1038376474958381056>Відійшли: **{idle}**\n<:ofline:1038376481774120970>Не в мережі: **{offline}**", 
            inline = True
            )
        embed.add_field(
            name = "Канали:", 
            value = f"<:total_channels:1038376491576205375> Всього: **{total_channels}**\n<:text_channels:1038376489399357504> Текстові: **{text_channels}**\n<:voice_channels:1038376495414001724> Голосові: **{voice_channels}**"
            )
        
        embed.set_thumbnail(url = ctx.guild.icon)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()

    @app_commands.command(name='user', description=f'Детальна інформація про користувача')
    async def user_(self, interaction: discord.Interaction, *, user: discord.Member = None,):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        if user is None:
            user = interaction.user
            
        for bio in cur.execute(f'SELECT bio FROM users WHERE id = {user.id}'):
            if bio[0] == 'None':
                bio = f"Ви можете додати сюди якусь інформацію про себе. Скориставшись `{config['bot_prefix']}bio`"
        headers = {"Authorization": f"Bot {config['bot_token']}"}
        req = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=headers).json()
        
        def rgb(hex):
            rgb = []
            for i in (0, 2, 4):
                decimal = int(hex[i:i+2], 16)
                rgb.append(decimal)
            return rgb
        bio = bio[0]
        cut = (bio[:150] + '...') if len(bio) > 150 else bio
        
        if req['banner_color'] is None:
            embed = discord.Embed(description=cut, color=StrToColor(config['color_default']))
        else:
            embed = discord.Embed(description=cut, color=discord.Color.from_rgb(rgb(req['banner_color'].replace('#', ''))[0], rgb(req['banner_color'].replace('#', ''))[1], rgb(req['banner_color'].replace('#', ''))[2]))
        
        #global user_status
        user_status = interaction.guild.get_member(user.id).status
        if user_status == discord.Status.online:
            user_status = "<:online:1038376483758030898>В мережі"
        elif user_status == discord.Status.offline or user_status == discord.Status.invisible:
            user_status = "<:ofline:1038376481774120970>Не в мережі"
        elif user_status == discord.Status.idle:
            user_status = "<:idle:1038376474958381056>Відійшов"
        elif user_status == discord.Status.dnd or user_status == discord.Status.do_not_disturb:
            user_status = "<:dnd:1048546187487227914>Не турбувати"

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
                        ca = f'**Користувацький статус**: {ca_emoji}\n'
                else:
                    ca = f'**Користувацький статус:** {ca_emoji}{ca_name}\n'

            if isinstance(active, discord.Spotify):
                print(active.title)
                print(active.artist)
                artist = active.artist
                if len(artist.split('; ')) > 1:
                    artist = artist.split('; ')
                    artist = ", ".join(artist)
                else:
                    artist = artist.replace(' ', '_')
                    artist = f'[{active.artist}](https://open.spotify.com/search/{artist})'
                        
                spotify = f'**Слухає:** <:spotify:1049105195906379837> [{active.title}](https://open.spotify.com/track/{active.track_id}) - {artist}\n'
            
            if isinstance(active, discord.Game):
                game = f'**Грає в:** {active.name}\n'
        
        nick = ''
        if user.nick is None:
            pass
        else:
            nick = f'**Ім\'я на сервері:** {user.nick}\n'
          
        embed.add_field(
            name='Основна інформація',
            value=f'**Ім\'я користувача:** {user.name}#{user.discriminator}\n{nick}**Статус:** {user_status}\n{ca}{spotify}{game}**Приєднаввся:** <t:{int(user.joined_at.timestamp())}:D> (<t:{int(user.joined_at.timestamp())}:R>)\n**Зареєструвався:** <t:{int(user.created_at.timestamp())}:D> (<t:{int(user.created_at.timestamp())}:R>)'
        )
        
        embed.set_author(
            name=f'Інформація про {user.name}',
            icon_url=user.avatar
        )
        
        embed.set_thumbnail(
            url=user.avatar
        )
        
        if req['banner'] is None:
            pass
        else:
            embed.set_image(
            url=f'https://cdn.discordapp.com/banners/{user.id}/{req["banner"]}?size=2048'
        )
        
        embed.set_footer(
            text=f'ID: {user.id}'
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()  

    @app_commands.command(name='bio', description='Встановити інформацію про себе')
    async def bio_(self, interaction: discord.Interaction, user: discord.Member = None, bio: str = None):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        if user is None:
            user = interaction.user
            for row in cur.execute(f'SELECT bio FROM users WHERE id = {user.id}'):
                db_bio = row[0]
            if bio is None:# returns bio author
                if db_bio == 'None':# check bio in BD
                    embed = discord.Embed(
                        title='Помилка!',
                        description=f'Ви ще нічого не вписали про себе!\nДетальніше про команду: `{config["bot_prefix"]}help bio`',
                        color=0xff0000
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    if user.nick is None:
                        name = user.name
                    else:
                        name = user.nick
                    embed = discord.Embed(
                        title=f'Біографія {name}',
                        description=db_bio,
                        color=StrToColor(config['color_default'])
                    )
                    
                    embed.set_thumbnail(
                        url=user.avatar
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
            elif bio == '-':
                cur.execute(f'UPDATE users SET bio = "None" WHERE id = {user.id}')
                    
                embed = discord.Embed(
                    title='Біографія оновленна',
                    description='Ви прибрали свою біографію',
                    color=StrToColor(config['color_default'])
                )
                embed.set_thumbnail(
                    url=user.avatar
                )
                    
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                cur.execute(f'UPDATE users SET bio = "{bio}" WHERE id = {user.id}')
                data.commit
                embed = discord.Embed(
                    title='Біографія оновленна',
                    description=f'Ви оновили свою біографію на:\n*{bio}*',
                    color=StrToColor(config['color_default'])
                )
                embed.set_thumbnail(
                    url=user.avatar
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
        elif user.id != interaction.user.id:
            if interaction.user.id != 734082410504781854:
                embed = discord.Embed(
                    title='Помилка',
                    description='У тебе немає прав для редагування біографій користувачів',
                    color=0xff0000
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                print(interaction.user.id)
            else:
                if bio is None:
                    embed = discord.Embed(
                        title='Помилка',
                        description=f'Ти забув ввести біографію користувача\nДетальніше про команду: `{config["bot_prefix"]}help bio`',
                        color=0xff0000
                    )
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                elif bio == '-':
                    cur.execute(f'UPDATE users SET bio = "None" WHERE id = {user.id}')
                    data.commit
                    embed = discord.Embed(
                        title='Біографія оновленна',
                        description=f'Ви прибрали біографію користувача **{user.name}**',
                        color=StrToColor(config['color_default'])
                    )
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
                else:
                    cur.execute(f'UPDATE users SET bio = "{bio}" WHERE id = {user.id}')
                    embed = discord.Embed(
                        title='Біографія оновленна',
                        description=f'Ви оновили біографію користувача {user.name} на:\n*{bio}*',
                        color=StrToColor(config['color_default'])
                    )
                    
                    await interaction.response.send_message(embed=embed, ephemeral=True)
        elif user.id == interaction.user.id and bio is None:
            embed = discord.Embed(
                    title='Помилка',
                    description=f'Для чого стільки букв, якщо можна використати просто `{config["bot_prefix"]}bio`',
                    color=0xff0000
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    
    
    @app_commands.command(name='question', description=f'Запитай {config["bot_name"]} будь що')
    async def question_(self, interaction: discord.Interaction, question: str):
        ctx = await self.bot.get_context(interaction)
        await interaction.response.defer()
        answer = Chat(question)
        
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        embed = discord.Embed(
            title = 'Відповідь на твоє питання',
            color = StrToColor(config['color_default']),
            description = answer
            )
        embed.set_thumbnail(url=config["bot_icon"])
        embed.set_footer(
            text=f'Mops Storage © 2020-{datetime.datetime.now().year} Всі права захищено • https://mops-storage.xyz',
            icon_url=config["bot_icon"]
        )
        
        #await asyncio.sleep(5)
        #await interaction.response.send_message(embed=embed, ephemeral=True)
        await asyncio.sleep(delay=0)
        await interaction.followup.send(embed=embed, ephemeral=True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()

    
    async def user_info_callback(self, interaction: discord.Interaction, user: discord.User):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        ctx = await self.bot.get_context(interaction)
        
        if user is None:
            user = ctx.author
            
        for bio in cur.execute(f'SELECT bio FROM users WHERE id = {user.id}'):
            if bio[0] == 'None':
                bio = f"Ви можете додати сюди якусь інформацію про себе. Скориставшись `{config['bot_prefix']}bio`"
        headers = {"Authorization": f"Bot {config['bot_token']}"}
        req = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=headers).json()
        
        def rgb(hex):
            rgb = []
            for i in (0, 2, 4):
                decimal = int(hex[i:i+2], 16)
                rgb.append(decimal)
            return rgb
        
        if req['banner_color'] is None:
            embed = discord.Embed(description=bio[0], color=StrToColor(config['color_default']))
        else:
            embed = discord.Embed(description=bio[0], color=discord.Color.from_rgb(rgb(req['banner_color'].replace('#', ''))[0], rgb(req['banner_color'].replace('#', ''))[1], rgb(req['banner_color'].replace('#', ''))[2]))
        
        #global user_status
        user_status = interaction.guild.get_member(user.id).status
        if user_status == discord.Status.online:
            user_status = "<:online:1038376483758030898>В мережі"
        elif user_status == discord.Status.offline or user_status == discord.Status.invisible:
            user_status = "<:ofline:1038376481774120970>Не в мережі"
        elif user_status == discord.Status.idle:
            user_status = "<:idle:1038376474958381056>Відійшов"
        elif user_status == discord.Status.dnd or user_status == discord.Status.do_not_disturb:
            user_status = "<:dnd:1048546187487227914>Не турбувати"

        
        
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
                        ca = f'**Користувацький статус**: {ca_emoji}\n'
                else:
                    ca = f'**Користувацький статус:** {ca_emoji}{ca_name}\n'

            if isinstance(active, discord.Spotify):
                print(active.title)
                print(active.artist)
                artist = active.artist
                if len(artist.split('; ')) > 1:
                    artist = artist.split('; ')
                    artist = ", ".join(artist)
                else:
                    artist = artist.replace(' ', '_')
                    artist = f'[{active.artist}](https://open.spotify.com/search/{artist})'
                        
                spotify = f'**Listen:** <:spotify:1049105195906379837> [{active.title}](https://open.spotify.com/track/{active.track_id}) - {artist}\n'
            
            if isinstance(active, discord.Game):
                game = f'**Грає в:** {active.name}\n'
        
        nick = ''
        if user.nick is None:
            pass
        else:
            nick = f'**Ім\'я на сервері:** {user.nick}\n'
          
        embed.add_field(
            name='Основна інформація',
            value=f'**Ім\'я користувача:** {user.name}#{user.discriminator}\n{nick}**Статус:** {user_status}\n{ca}{spotify}{game}**Приєднаввся:** <t:{int(user.joined_at.timestamp())}:D> (<t:{int(user.joined_at.timestamp())}:R>)\n**Зареєструвався:** <t:{int(user.created_at.timestamp())}:D> (<t:{int(user.created_at.timestamp())}:R>)'
        )
        
        embed.set_author(
            name=f'Інформація про {user.name}',
            icon_url=user.avatar
        )
        
        embed.set_thumbnail(
            url=user.avatar
        )
        
        if req['banner'] is None:
            pass
        else:
            embed.set_image(
            url=f'https://cdn.discordapp.com/banners/{user.id}/{req["banner"]}?size=2048'
        )
        
        embed.set_footer(
            text=f'ID: {user.id}'
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()

async def setup(bot):
    await bot.add_cog(Information(bot))