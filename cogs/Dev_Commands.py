# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
from discord.interactions import Interaction
from discord.ui import Select, View, Button, Modal
from discord import ui
from discord import app_commands
import sqlite3
import requests
from os import listdir
from ganyu import *
import typing
import asyncio


data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()
config = LoadJson("config.json")# load config

class Test_Commands(commands.Cog, name='Команди розробника'):
    """Команди для перевірки різних функцій, подій і т.д.
    
    Виокристовується лиша для тесту і не більше!
    """
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print('Test commands - Ready!')# Виводить, коли гвинтик готовий до роботи
    """
    
    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        """Перевіряє чи працює Cog система"""
        ping = self.bot.latency
        guilds = self.bot.guilds
        for guild in guilds:
            print(guild)
            print(f'Канали: {len(guild.text_channels) + len(guild.voice_channels) + len(ctx.guild.stage_channels)}')
        embed = discord.Embed(
            title=f'Пінг - {round(ping, 2)}\nСервери: {len(guilds)}\nУччасники: {len(self.bot.users)}'
        )
        await ctx.send(embed=embed)  

    @commands.command()
    @commands.is_owner()
    async def create_invite(self, ctx, server_id: int):
        guild = self.bot.get_guild(server_id)
        invite = await guild.text_channels[0].create_invite(max_age=0, max_uses=0, temporary=False)
        await ctx.send(invite)

    @app_commands.command(name = "button")
    @commands.is_owner()
    async def button(self, interaction: discord.Interaction):
        button = Button(
            label = 'Url',
            style = discord.ButtonStyle.url,
            url = 'https://mops-storage.xyz'
        )
        button1 = Button(
            label = 'Button',
            style = discord.ButtonStyle.primary
        )
        
        async def button_call_back(interaction:discord.Integration):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title='Hello',
                    color=StrToColor(config["color_default"])
                ),
                ephemeral = True
            )
        
        button1.callback = button_call_back
        
        view = View()
        view.add_item(button)
        view.add_item(button1)
        
        await interaction.response.send_message(view = view)
        
    
    
    
    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx) -> None:
        fmt = await ctx.bot.tree.sync()
        await ctx.send(f'Synced {len(fmt)} commands')
        
    @sync.error
    async def sync_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Помилка',
                description='Ви не можете використовувати цю команду!',
                color=0xff0000
            )
            await ctx.reply(embed=embed)
            
    
    @commands.command()
    @commands.is_owner()
    async def select_menu(self, ctx):
        select = Select(
            placeholder='Вибери дію...',
            options=[
                discord.SelectOption(
                    label='Padoru',
                    value='1',
                    emoji='<a:SoraoDev:931927261731516477>',
                    description='Час настав...'
                    ),
                discord.SelectOption(
                    label='Що?',
                    value='2',
                    emoji='<a:SoraSquints:931922199403696188>',
                    description='Сорова мружиться'
                    ),
                discord.SelectOption(
                    label='Хе-хе, не хе-хе',
                    value='3',
                    emoji='<a:HuTaoRock:1030925213522727122>',
                    description='Ху Тао-Скала'
                    )
                ]
            )
        
        async def my_callback(interaction:discord.Interaction):
            if select.values[0] == '1':
                await interaction.response.send_message(f'Ти вибрав {select.values[0]}')
                await ctx.send(select.values[0])
            if select.values[0] == '2':
                await interaction.response.send_message(f'Ти вибрав {select.values[0]}')
            if select.values[0] == '3':
                await interaction.response.edit_message(content=f'Ти вибрав {select.values[0]}')
        
        select.callback = my_callback
        view = View()
        view.add_item(select)
    
        await ctx.defer(ephemeral=True)
        await ctx.send('Menu', view=view)
    """
    @commands.command(name='information')
    async def information(self, ctx):
        for row in cur.execute(f'SELECT commands FROM stats_bot'):
            StBcommands = row[0]
        
        embed = discord.Embed(
                    title='Доступні команди категорії 📃Інформація',
                    description=f'Ви можете отримати детальну інформацію для кожної команди, викликавши її за допомогою {settings["prefix"]}help `<назва команди>`',
                    color=settings['color']
                )
        embed.set_thumbnail(
            url=settings['avatar']
        )
        embed.set_footer(
            text='Mops Storage © 2020-2022 Всі права захищено • https://mops-storage.xyz',
            icon_url=settings['avatar']
        )
        embed.add_field(
            name=f'{settings["prefix"]}help',
            value='Список всі доступних команд та категорій',
            inline=False
        )
        embed.add_field(
            name=f'{settings["prefix"]}info',
            value=f'Корисна інформація про {settings["name"]}',
            inline=False
        )
        embed.add_field(
            name=f'{settings["prefix"]}stats',
            value=f'Статистика використання {settings["name"]}',
            inline=False
        )
        embed.add_field(
            name=f'{settings["prefix"]}server',
            value='Інформація про поточний сервер',
            inline=False
        )
        embed.add_field(
            name=f'{settings["prefix"]}user',
            value='Інформація про учасника',
            inline=False
        )
        
        await ctx.reply(embed=embed)
        cur.execute(f'UPDATE stats_bot SET commands = {StBcommands + 1} ')
        data.commit()
    """
    
    @commands.command()
    async def get_user(self, ctx, user: discord.Member):
            headers = {"Authorization": f"Bot {config['bot_token']}"}
            req = requests.get(f"https://discord.com/api/v9/users/{user.id}", headers=headers).json()
            await ctx.reply(req)

    @app_commands.command(name = "atach", description = "Save a photo")
    async def save_photo(self, interaction: discord.Interaction, image: discord.Attachment):
        if image.content_type in ["image/npg", "image/jpg", "image/jpeg", "image/gif"]:
            image_url = (lambda url: url.split('?')[0])(image.url)
            await interaction.response.send_message(embed = discord.Embed(description = "This is image {0}".format(image_url)).set_image(url = image_url), ephemeral = True)
        else:
            await interaction.response.send_message('This is a different type of file.', ephemeral=True)

    
    @app_commands.command(name='nick', description='Змінна нікнейму')
    async def nick(self, interaction: discord.Interaction, user: discord.Member, nick: str):
        await user.edit(nick=nick)
        await interaction.response.send_message(content=f'Користувачу {user.name} було змінено нікнейм на {nick}')
    
    @app_commands.command(name='kick', description='Тест парметрів')
    async def kick_(self, interaction: discord.Interaction, user: discord.Member, channel: discord.TextChannel, reason: str = None):
        #ctx = await self.bot.get_context(interaction)
        
        await interaction.response.send_message(content=f'Вигнато користувача {channel} {user.name} за причиною:\n`{reason}`')


    
    
    @app_commands.command(name = 'modal', description = 'test modal')
    async def test_modal(self, interaction: discord.Interaction):
        class TestModal(Modal, title = 'Test Moda'):
            fb_title = ui.TextInput(
                style = discord.TextStyle.short,
                label = "Title",
                required = False,
                placeholder = "Enter your title here"
            )
            
            message = ui.TextInput(
                style = discord.TextStyle.long,
                label = "Mesage",
                required = False,
                max_length = 1024,
                placeholder = "Enter your message here"
            )
            
            async def on_submit(self, interaction: discord.Interaction):
                embed = discord.Embed(
                    title = "Новий відгук",
                    description = self.message.value,
                    color = StrToColor(config["color_deafult"])
                )
                
                embed.set_author(
                    name = interaction.user.name,
                    url = "https://discord.com/users/{0}".format(interaction.user.id),
                    icon_url = interaction.user.avatar.url
                )
                channel = interaction.guild
                await owner.send(embed = embed)
                await interaction.response.send_message("Дякую за ваш відгук", ephemeral = True)
                
            async def on_error(self, interaction: discord.Interaction, error):
                await interaction.response.send_message("Error: {0}".format(error), ephemeral = True)
            
        modal = TestModal()
        await interaction.response.send_modal(modal)

# Error callback
    @sync.error
    async def sync_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Помилка',
                description='Ви не можете використовувати цю команду!',
                color=0xff0000
            )
            await ctx.reply(embed=embed)

    @ping.error
    async def ping_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Помилка',
                description='Ви не можете використовувати цю команду!',
                color=0xff0000
            )
            await ctx.reply(embed=embed)
     
    @create_invite.error
    async def create_invite_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Помилка',
                description='Ви не можете використовувати цю команду!',
                color=0xff0000
            )
            await ctx.reply(embed=embed)
      
    @button.error
    async def button_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Помилка',
                description='Ви не можете використовувати цю команду!',
                color=0xff0000
            )
            await ctx.reply(embed=embed)

    @select_menu.error
    async def select_menu_error(self, ctx, error):
        if isinstance(error, commands.NotOwner):
            embed = discord.Embed(
                title='Помилка',
                description='Ви не можете використовувати цю команду!',
                color=0xff0000
            )
            await ctx.reply(embed=embed)
    
    @app_commands.command(name='test_locale', description='Check locale settings')
    async def test_locale_(self, interaction: discord.Interaction):
        await interaction.response.send_message(GetMsg('test_locale', interaction.guild))
""" 
    group = app_commands.Group(name='menu', description='our menu')

    @group.command(name="coffee") 
    async def my_sub_command(self, interaction: discord.Interaction):
        await interaction.response.send_message("Coffee", ephemeral=True)
        
"""
    
    
async def setup(bot):
    await bot.add_cog(Test_Commands(bot))