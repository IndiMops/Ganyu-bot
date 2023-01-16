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
                        title='Стихіія Анемо',
                        description='Анемо — один із семи елементів і перший, який може використовувати Мандрівник. Архонт, з яким асоціюється — Барбатос, володіннями якого є Мондштадт.',
                        color=0x90dfbd
                    )

                    embed.set_image(
                        url='https://media.discordapp.net/attachments/939569454390603837/1053091519017517066/dvalin_and_venti_by_skyvixie_defnr9r-fullview.jpg'
                    )
                    embed.set_thumbnail(
                        url='https://media.discordapp.net/attachments/939569454390603837/1053095902576906270/anemo.png'
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
                            ),
                            discord.SelectOption(
                                label='Венті',
                                value='3',
                                emoji='<:avatar_Venti:1053099898377089116>'
                            ),
                            discord.SelectOption(
                                label='Джин',
                                value='4',
                                emoji='<:avavtar_jean:1053099797558607964>'
                            ),
                            discord.SelectOption(
                                label='Сяо',
                                value='5',
                                emoji='<:avatar_Xiao:1053099915254968340>'
                            ),
                            discord.SelectOption(
                                label='Каедехара Кадзуха',
                                value='6',
                                emoji='<:avatar_Kazuha:1053099819708731454>'
                            ),
                            discord.SelectOption(
                                label='Саю',
                                value='7',
                                emoji='<:avatar_Sayu:1053099844098609273>'
                            ),
                            discord.SelectOption(
                                label='Шіканоін Хейдзо',
                                value='8',
                                emoji='<:avatar_Heizo:1053099777484660756>'
                            ),
                            discord.SelectOption(
                                label='Фарузан',
                                value='9',
                                emoji='<:avatar_Faruzan:1053099756047568947>'
                            ),
                            discord.SelectOption(
                                label='Блукач',
                                value='10',
                                emoji='<:avarar_Wanderer:1053099877372010596>'
                            )
                        ]
                    )
                    
                    async def anemo(interaction: discord.Integration):
                        path = './cogs/character.json'
                        with open(path, encoding='utf-8') as f:
                            data = json.load(f)
                            
                        if anemo_menu.values[0] == '1':
                            traveler = data['anemo_traveler']
                            embed = discord.Embed(
                                title=traveler['name'],
                                description=f'*"{traveler["description"]}"*',
                                color=0x90dfbd
                            )
                            embed.set_author(
                                name='Основна інформація'
                            )
                            embed.add_field(
                                name='Стихія',
                                value=traveler['element']
                            )
                            embed.add_field(
                                name='Сузір\'я',
                                value=traveler['const']['name']
                            )
                            embed.add_field(
                                name='⠀',
                                value='⠀'
                            )
                            embed.add_field(
                                name='День народження',
                                value='Встановлю гравець'
                            )
                            embed.add_field(
                                name='Група',
                                value='Змінюється по ходу сюжету'
                            )
                            embed.add_field(
                                name='⠀',
                                value='⠀'
                            )
                            embed.add_field(
                                name='Актори озвучування',
                                value='⠀',
                                inline=False
                            )
                            embed.add_field(
                                name='EN',
                                value=traveler['voice_artist']['en']
                            )
                            embed.add_field(
                                name='CN',
                                value=traveler['voice_artist']['chn']
                            )
                            embed.add_field(
                                name='JP',
                                value=traveler['voice_artist']['jp']
                            )
                            embed.add_field(
                                name='KR',
                                value=traveler['voice_artist']['kr']
                            )                            
                            
                            embed.set_thumbnail(
                                url=traveler['avatar']
                            ) 
                            embed.set_image(
                                url=traveler['card']
                            )
                            
                            anemo_traveler_menu = Select(
                                placeholder='Виберіть вкладку...',
                                options=[
                                    discord.SelectOption(
                                        label='Рівні та ресурси',
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
                                    )
                                ]
                            )
                            
                            async def character_info(interaction: discord.Interaction):
                                if anemo_traveler_menu.values[0] == '1':
                                    embed = discord.Embed(
                                        title='Рівні та ресурси',
                                        description='Виберіть із списку потрібний вам рівень і ви отримаєте базові характеристики персонажа та ресурси для прокачування на це рівень',
                                        color=0x90dfbd
                                    )
                                    
                                    embed.set_thumbnail(
                                        url=traveler['avatar']
                                    ) 
                                    embed.set_image(
                                        url='https://media.discordapp.net/attachments/939569454390603837/1054054555995881544/banners2.png'
                                    )
                                    
                                    
                                    anemo_traveler_resource_menu = Select(
                                        placeholder='Виберіть рівень...',
                                        options=[
                                            discord.SelectOption(
                                                label='20 рівень',
                                                value='1'
                                            ),
                                            discord.SelectOption(
                                                label='40 рівень',
                                                value='2'
                                            ),
                                            discord.SelectOption(
                                                label='50 рівень',
                                                value='3'
                                            ),
                                            discord.SelectOption(
                                                label='60 рівень',
                                                value='4'
                                            ),
                                            discord.SelectOption(
                                                label='70 рівень',
                                                value='5'
                                            ),
                                            discord.SelectOption(
                                                label='80 рівень',
                                                value='6'
                                            ),
                                            discord.SelectOption(
                                                label='90 рівень',
                                                value='7'
                                            )
                                        ]
                                    )
                                    
                                    async def character_level(interaction: discord.Interaction):
                                        stats = traveler['stats']
                                        if anemo_traveler_resource_menu.values[0] == '2':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            #print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_40"]["base_HP"]}\n**Базова шкода:** {stats["lvl_40"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_40"]["base_DEF"]}\n**Шкода:** {stats["lvl_40"]["ATK"]}',
                                                inline=False
                                            )
                                            update_item = stats['lvl_40']['update_item']
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=f'**Місцеві диковини:**\n{update_item["local_specialty"]["name"]} - {update_item["local_specialty"]["count"]}\n\n**Камінь:**\n{update_item["stone"]["name"]} - {update_item["stone"]["count"]}\n\n**Ресурси із мобів:**\n{update_item["mob_loot"]["name"]} - {update_item["mob_loot"]["count"]}'
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        
                                        if anemo_traveler_resource_menu.values[0] == '1':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_20"]["base_HP"]}\n**Базова шкода:** {stats["lvl_20"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_20"]["base_DEF"]}\n**Шкода:** {stats["lvl_20"]["ATK"]}',
                                                inline=False
                                            )
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=stats['lvl_20']['update_item']
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)

                                        if anemo_traveler_resource_menu.values[0] == '3':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_50"]["base_HP"]}\n**Базова шкода:** {stats["lvl_50"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_50"]["base_DEF"]}\n**Шкода:** {stats["lvl_50"]["ATK"]}',
                                                inline=False
                                            )
                                            update_item = stats['lvl_50']['update_item']
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=f'**Місцеві диковини:**\n{update_item["local_specialty"]["name"]} - {update_item["local_specialty"]["count"]}\n\n**Камінь:**\n{update_item["stone"]["name"]} - {update_item["stone"]["count"]}\n\n**Ресурси із мобів:**\n{update_item["mob_loot"]["name"]} - {update_item["mob_loot"]["count"]}'
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                            
                                        if anemo_traveler_resource_menu.values[0] == '4':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_60"]["base_HP"]}\n**Базова шкода:** {stats["lvl_60"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_60"]["base_DEF"]}\n**Шкода:** {stats["lvl_60"]["ATK"]}',
                                                inline=False
                                            )
                                            update_item = stats['lvl_60']['update_item']
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=f'**Місцеві диковини:**\n{update_item["local_specialty"]["name"]} - {update_item["local_specialty"]["count"]}\n\n**Камінь:**\n{update_item["stone"]["name"]} - {update_item["stone"]["count"]}\n\n**Ресурси із мобів:**\n{update_item["mob_loot"]["name"]} - {update_item["mob_loot"]["count"]}'
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)

                                        if anemo_traveler_resource_menu.values[0] == '5':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_70"]["base_HP"]}\n**Базова шкода:** {stats["lvl_70"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_70"]["base_DEF"]}\n**Шкода:** {stats["lvl_70"]["ATK"]}',
                                                inline=False
                                            )
                                            update_item = stats['lvl_70']['update_item']
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=f'**Місцеві диковини:**\n{update_item["local_specialty"]["name"]} - {update_item["local_specialty"]["count"]}\n\n**Камінь:**\n{update_item["stone"]["name"]} - {update_item["stone"]["count"]}\n\n**Ресурси із мобів:**\n{update_item["mob_loot"]["name"]} - {update_item["mob_loot"]["count"]}'
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        
                                        if anemo_traveler_resource_menu.values[0] == '6':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_80"]["base_HP"]}\n**Базова шкода:** {stats["lvl_80"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_80"]["base_DEF"]}\n**Шкода:** {stats["lvl_80"]["ATK"]}',
                                                inline=False
                                            )
                                            update_item = stats['lvl_80']['update_item']
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=f'**Місцеві диковини:**\n{update_item["local_specialty"]["name"]} - {update_item["local_specialty"]["count"]}\n\n**Камінь:**\n{update_item["stone"]["name"]} - {update_item["stone"]["count"]}\n\n**Ресурси із мобів:**\n{update_item["mob_loot"]["name"]} - {update_item["mob_loot"]["count"]}'
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        
                                        if anemo_traveler_resource_menu.values[0] == '7':
                                            embed = discord.Embed(
                                                title='Рівні та ресурси',
                                                color=0x90dfbd
                                            )
                                            print(anemo_traveler_resource_menu.values)
                                            embed.set_author(
                                                name=traveler['name']
                                            )

                                            embed.add_field(
                                                name='Базові характеристики',
                                                value=f'**Базове здоров\'я:** {stats["lvl_90"]["base_HP"]}\n**Базова шкода:** {stats["lvl_90"]["base_ATK"]}\n**Базовий захист:** {stats["lvl_90"]["base_DEF"]}\n**Шкода:** {stats["lvl_90"]["ATK"]}',
                                                inline=False
                                            )
                                            update_item = stats['lvl_90']['update_item']
                                            embed.add_field(
                                                name='Ресурси для покращення',
                                                value=f'**Місцеві диковини:**\n{update_item["local_specialty"]["name"]} - {update_item["local_specialty"]["count"]}\n\n**Камінь:**\n{update_item["stone"]["name"]} - {update_item["stone"]["count"]}\n\n**Ресурси із мобів:**\n{update_item["mob_loot"]["name"]} - {update_item["mob_loot"]["count"]}'
                                            )
                                            
                                            embed.set_thumbnail(
                                                url=traveler['avatar']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1054064966996598824/banners3.png'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)


                                    anemo_traveler_resource_menu.callback = character_level
                                    anemo_traveler_resurse_view = View()
                                    anemo_traveler_resurse_view.add_item(anemo_traveler_resource_menu)
                                    
                                    await interaction.response.edit_message(embed=embed, view=anemo_traveler_resurse_view)

                                if anemo_traveler_menu.values[0] == '2':
                                    embed = discord.Embed(
                                        title='Сузір\'я',
                                        description='Виберіть із списку потрібне вам сузір\'я. Ви отримаєте всю інформацію про сузір\'я персонажа.',
                                        color=0x90dfbd
                                    )
                                    embed.set_thumbnail(
                                        url=traveler['avatar']
                                    ) 
                                    embed.set_image(
                                        url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                    )
                                    
                                    const = traveler['const']
                                    anemo_traveler_const_menu = Select(
                                        placeholder='Виберіть сузір\'я...',
                                        options=[
                                            discord.SelectOption(
                                                label=const['const1']['name'],
                                                value='1',
                                                emoji=const['const1']['emoji']
                                            ),
                                            discord.SelectOption(
                                                label=const['const2']['name'],
                                                value='2',
                                                emoji=const['const2']['emoji']
                                            ),
                                            discord.SelectOption(
                                                label=const['const3']['name'],
                                                value='3',
                                                emoji=const['const3']['emoji']
                                            ),
                                            discord.SelectOption(
                                                label=const['const4']['name'],
                                                value='4',
                                                emoji=const['const4']['emoji']
                                            ),
                                            discord.SelectOption(
                                                label=const['const5']['name'],
                                                value='5',
                                                emoji=const['const5']['emoji']
                                            ),
                                            discord.SelectOption(
                                                label=const['const6']['name'],
                                                value='6',
                                                emoji=const['const6']['emoji']
                                            ),
                                        ]
                                    )
                                    
                                    async def character_const(interaction: discord.Interaction):
                                        if anemo_traveler_const_menu.values[0] == '1':
                                            embed = discord.Embed(
                                                title=f'Сузір\'я - {const["const1"]["emoji"]}{const["const1"]["name"]}',
                                                description=const['const1']['desc'],
                                                color=0x90dfbd
                                            )
                                            embed.set_thumbnail(
                                                url=const['const1']['image']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        if anemo_traveler_const_menu.values[0] == '2':
                                            embed = discord.Embed(
                                                title=f'Сузір\'я - {const["const2"]["emoji"]}{const["const2"]["name"]}',
                                                description=const['const1']['desc'],
                                                color=0x90dfbd
                                            )
                                            embed.set_thumbnail(
                                                url=const['const2']['image']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        if anemo_traveler_const_menu.values[0] == '3':
                                            embed = discord.Embed(
                                                title=f'Сузір\'я - {const["const3"]["emoji"]}{const["const3"]["name"]}',
                                                description=const['const3']['desc'],
                                                color=0x90dfbd
                                            )
                                            embed.set_thumbnail(
                                                url=const['const3']['image']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        if anemo_traveler_const_menu.values[0] == '4':
                                            embed = discord.Embed(
                                                title=f'Сузір\'я - {const["const4"]["emoji"]}{const["const4"]["name"]}',
                                                description=const['const4']['desc'],
                                                color=0x90dfbd
                                            )
                                            embed.set_thumbnail(
                                                url=const['const4']['image']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        if anemo_traveler_const_menu.values[0] == '5':
                                            embed = discord.Embed(
                                                title=f'Сузір\'я - {const["const5"]["emoji"]}{const["const5"]["name"]}',
                                                description=const['const5']['desc'],
                                                color=0x90dfbd
                                            )
                                            embed.set_thumbnail(
                                                url=const['const5']['image']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        if anemo_traveler_const_menu.values[0] == '6':
                                            embed = discord.Embed(
                                                title=f'Сузір\'я - {const["const6"]["emoji"]}{const["const6"]["name"]}',
                                                description=const['const6']['desc'],
                                                color=0x90dfbd
                                            )
                                            embed.set_thumbnail(
                                                url=const['const6']['image']
                                            )
                                            embed.set_image(
                                                url='https://media.discordapp.net/attachments/939569454390603837/1064661947527737425/banners4.jpeg'
                                            )
                                            
                                            await interaction.response.edit_message(embed=embed)
                                        
                                    
                                    anemo_traveler_const_menu.callback = character_const
                                    anemo_traveler_const_view = View()
                                    anemo_traveler_const_view.add_item(anemo_traveler_const_menu)
                                    
                                    await interaction.response.edit_message(embed=embed, view=anemo_traveler_const_view)
                                    
                            anemo_traveler_menu.callback = character_info
                            anemo_traveler_view = View()
                            anemo_traveler_view.add_item(anemo_traveler_menu)
                            
                            await interaction.response.edit_message(embed=embed, view=anemo_traveler_view)
                    
                    
                    anemo_menu.callback = anemo
                    anemo_view = View()
                    anemo_view.add_item(anemo_menu)
                    
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
            
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    
async def setup(bot):
    await bot.add_cog(Character(bot))
