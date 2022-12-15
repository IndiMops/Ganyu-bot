import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import Select, View, Button
from discord import ui
from config import settings
import sqlite3
import json

data = sqlite3.connect('data.sqlite')#connect to BD
cur = data.cursor()

class Character(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    
    @app_commands.command(name='character', description='Відображає основну інформацію про персонажа')
    async def character_(self, interaction: discord.Integration, character: str = None):
        if character is None:
            menu = Select(
                placeholder='Виберіть стихію...',
                options=[
                    discord.SelectOption(
                        label='Анемо',
                        value='1',
                        emoji='<:anemo:1052652587708600380>'
                    ),
                    discord.SelectOption(
                        label='Кріо',
                        value='2',
                        emoji='<:crio:1052652588966871040>'
                    ),
                    discord.SelectOption(
                        label='Дендро',
                        value='3',
                        emoji='<:dendro:1052652590225174618>'
                    ),
                    discord.SelectOption(
                        label='Електро',
                        value='4',
                        emoji='<:electro:1052652591512813599>'
                    ),
                    discord.SelectOption(
                        label='Гео',
                        value='5',
                        emoji='<:geo:1052652592754331708>'
                    ),
                    discord.SelectOption(
                        label='Гідро',
                        value='6',
                        emoji='<:hidro:1052652593790341202>'
                    ),
                    discord.SelectOption(
                        label='Піро',
                        value='7',
                        emoji='<:piro:1052652594813743207>'
                    )
                ]
            )
            
            async def no_character(interaction: discord.Integration):
                if menu.values[0] == '1':
                    embed = discord.Embed(
                        title='Стихіія Анемо'
                    )
                    
                    anemo_menu = Select(
                        placeholder='Виберіть персонажа...',
                        options=[
                            discord.SelectOption(
                                label='Мандрівник(анемо)',
                                value='1',
                                emoji='<:traveler:1052662876948668436>'
                            ),
                            discord.SelectOption(
                                label='Цукроза',
                                value='2',
                                emoji='<:sucrose:1052662935845085214>'
                            )
                        ]
                    )
                     # paginatio
                    first_page = Button(
                        emoji='⬅️',
                        style=discord.ButtonStyle.blurple,
                        disabled=True
                    )
                    pervision_page = Button(
                        emoji='⏮️',
                        style=discord.ButtonStyle.green,
                        disabled=True
                    )
                    next_page = Button(
                        emoji='⏭️',
                        style=discord.ButtonStyle.green
                    )
                    last_page = Button(
                        emoji='➡️',
                        style=discord.ButtonStyle.blurple
                    )
                    
                    async def anemo(interaction: discord.Integration):
                        if anemo_menu.values[0] == '1':
                            path = './cogs/character.json'
                            with open(path, encoding='utf-8') as f:
                                data = json.load(f)
                            
                            embed = discord.Embed(
                                title=data['anemo_traveler']['name'],
                                description=f'*"{data["anemo_traveler"]["description"]}"*',
                                color=data['anemo_traveler']['color']
                            )
                            embed.set_author(
                                name='Основна інформація'
                            )
                            embed.add_field(
                                name='Стихія',
                                value=data['anemo_traveler']['element'],
                                inline=False
                            )
                            embed.add_field(
                                name='Сузір\'я',
                                value=data['anemo_traveler']['element'],
                                inline=False
                            )
                            embed.set_thumbnail(
                                url=data['anemo_traveler']['avatar']
                            )
                            
                            anemo_traveler_menu = Select(
                                placeholder='Виберіть вкладку...',
                                options=[
                                    discord.SelectOption(
                                        label='Основне',
                                        value='1'
                                    ),
                                    discord.SelectOption(
                                        label='Сузір\'я',
                                        value='2'
                                    ),
                                    discord.SelectOption(
                                        label='Таланти',
                                        value='3'
                                    ),
                                    discord.SelectOption(
                                        label='Історія',
                                        value='4'
                                    ),
                                    discord.SelectOption(
                                        label='Інше',
                                        value='5'
                                    )
                                ]
                            )
                            async def character_info(interaction: discord.Interaction):
                                pass
                            
                            anemo_traveler_menu.callback = character_info
                            anemo_traveler_view = View()
                            anemo_traveler_view.add_item(anemo_traveler_menu)
                            
                            await interaction.response.edit_message(embed=embed, view=anemo_traveler_view)
                    
                    
                    anemo_menu.callback = anemo
                    anemo_view = View()
                    anemo_view.add_item(anemo_menu)
                    anemo_view.add_item(first_page)
                    anemo_view.add_item(pervision_page)
                    anemo_view.add_item(next_page)
                    anemo_view.add_item(last_page)
                    
                    await interaction.response.edit_message(embed=embed, view=anemo_view)
            
            menu.callback = no_character
            view = View()
            view.add_item(menu)
            
            embed = discord.Embed(
                title='Персонажі',
                description='Персонажі є одержуваними одиницями в Ґеншін Імпакт. Вони бувають різної рідкості (4-зіркові та 5-зіркові), узгоджені зі стихією, оснащені певною зброєю та належать до регіону.',
                color=settings['color']
            )
            embed.add_field(
                name='Як отримати?',
                value='Персонажів можна отримати в основному за допомогою <:IntertwinedFates:939550612935282738>Переплетена доля або <:Item_Acquaint_Fate:939550687275139113>Доля зустрічі (придбані за Примоґеми, або отримані через події, завдання або куплені в щомісяця оновлювальному магазині на <:MasterlessStardust:939550787724537927>Безгосподарний зоряний пил або <:MasterlessStarglitter:939550714810732615>Безгосподарний зоряний блиск в Угоді з Паймон), щоб зробити Бажання. <:Noelle:939551108823662703>Ноель — це гарантований персонаж у банері Бажаннях новачка.',
                inline=False
            )
            embed.set_thumbnail(
                url=settings['avatar']
            )
            embed.set_image(
                url='https://media.discordapp.net/attachments/939569454390603837/1052884455355850752/chapter.png'
            )
            
            await interaction.response.defer(thinking=True)
            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
    
    
async def setup(bot):
    await bot.add_cog(Character(bot))
