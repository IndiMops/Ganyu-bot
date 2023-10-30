# -*- coding: utf-8 -*-
import discord
from discord.ext import commands, tasks
from discord.ui import Select, View, Button
from discord import ui
from discord import app_commands
import sqlite3
import requests
from os import listdir
from ganyu import *
import typing
import asyncio

data = sqlite3.connect('data.sqlite')# connect to BD
cur = data.cursor()
config = LoadJson("config.json")# load config

cur.execute("""CREATE TABLE IF NOT EXISTS tickets (
        'TicketID' INTEGER PRIMARY KEY AUTOINCREMENT,
        'ServerId' INTEGER,
        'UserID' INTEGER,
        'ChannelID' VARCHAR(255),
        'Status' VARCHAR(50),
        'CreatedAt' TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        'ClosedAt' TIMESTAMP NULL
        )""")

class TicketSys(commands.Cog, name = 'Система тікетів'):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    ticket_commands = app_commands.Group(name = 'ticket', description = "Ticket commands")
            
    
    @ticket_commands.command(name = 'open', description = GetMsg("command_ticket_open_description"))
    async def ticket_add(self, interaction: discord.Interaction, subject: str = None) -> None:
        close_ticket = Button(
            label = GetMsg("command_ticket_open_button_label_close_ticket", interaction.guild),
            style = discord.ButtonStyle.danger,
            emoji = "🔒",
            custom_id = "closeticket"
        )
        
        delete_ticket = Button(
            label = GetMsg("command_ticket_open_button_label_delete_ticket", interaction.guild),
            style = discord.ButtonStyle.danger,
            emoji = "🗑️",
            custom_id = "deleteticket"
        )
        
            
        # Checks whether the user has already created a ticket
        cur.execute("SELECT * FROM tickets WHERE UserID = ? AND Status = 'open' AND ChannelId IS NOT Null", (interaction.user.id,))
        existing_ticket = cur.fetchone()

    
        if existing_ticket:
            await interaction.response.send_message(GetMsg("command_ticket_open_ticket_opened", interaction.guild).format(existing_ticket[3]), ephemeral = True)
        else:
            await interaction.response.defer(ephemeral = True)
            
            # Get ticket category from server config
            category: discord.CategoryChannel
            for i in interaction.guild.categories:
                if i.id == int(GuildConfGet(interaction.guild, "ticket_category")):
                    category = i
                    break
            
            # Get admin role from server confgig
            r1: discord.Role = interaction.guild.get_role(int(GuildConfGet(interaction.guild, "ticket_admin_role")))
            overwrites = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages = False),
                r1: discord.PermissionOverwrite(read_messages = True, send_messages = True, manage_messages = True),
                interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages = True),
                interaction.guild.me: discord.PermissionOverwrite(read_messages = True, send_messages = True)
            }
                
            try:
                cur.execute("INSERT INTO tickets (UserID, Status, ServerId) VALUES ({0}, 'open', {1})".format(interaction.user.id, interaction.guild.id))
                data.commit()
            except Exception as e:
                print(e)
                data.rollback()

            
            cur.execute("SELECT TicketID FROM tickets WHERE ServerId = {0}".format(interaction.guild.id))# Obtaining the last ticket id
            last_id = len(cur.fetchall())
            
            if subject is None:
                subject = GetMsg("command_ticket_no_topic_ticket", interaction.guild)
            
            channel = await category.create_text_channel(
                name = '{0}-{1}'.format(last_id, interaction.user.name),
                topic = subject,
                overwrites = overwrites
            )
            cur.execute("UPDATE tickets SET ChannelID = ? WHERE TicketID = ?", (channel.id, last_id))
            data.commit()
            
            await interaction.followup.send(
            embed = discord.Embed(
                description = GetMsg("command_ticket_open_success_embed_description", interaction.guild).format(channel.jump_url),
                color = StrToColor(config["color_ok"])
                ), ephemeral = True
            )
            
            await channel.send(
                embed = discord.Embed(
                    title = subject,
                    description = GetMsg("command_ticket_open_first_message_in_ticket_embed_description", interaction.guild),
                    color = StrToColor(config["color_ok"])
                ),
                view = View().add_item(close_ticket)
            )
        
        async def close_ticket_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral = True)
            
            await interaction.channel.send(GetMsg("command_ticket_open_close_through", interaction.guild))
            
            await asyncio.sleep(3)
            
            cur.execute("UPDATE tickets SET Status = 'close' WHERE UserID = ? AND Status = 'open' AND ChannelId IS NOT Null", (interaction.user.id, ))
            data.commit()
            
            category: discord.CategoryChannel
            for i in interaction.guild.categories:
                if i.id == GuildConfGet(interaction.guild, "ticket_category"):
                    category = i
                    break
                
            r1: discord.Role = interaction.guild.get_role(int(GuildConfGet(interaction.guild, "ticket_admin_role")))
            overwrites = {
                r1: discord.PermissionOverwrite(read_messages = True, send_messages = False, manage_messages = True),
                interaction.user: discord.PermissionOverwrite(read_messages = True, send_messages = False),
            }
            
            await interaction.channel.edit(category = category, overwrites = overwrites)
            await interaction.channel.send(
                embed = discord.Embed(
                    description = GetMsg("comand_ticket_open_close_message", interaction.guild),
                    color = StrToColor(config["color_error"])
                ),
                 view = View().add_item(delete_ticket)
            )
        
        async def delete_ticket_callback(interaction: discord.Interaction):
            await interaction.response.defer(ephemeral = True)
            await interaction.channel.send(GetMsg("command_ticket_open_delete_through", interaction.guild))
            await asyncio.sleep(3)
            
            await interaction.channel.delete()
            cur.execute("UPDATE tickets SET Status = 'deleted' WHERE UserID = ? AND Status = 'open' AND ChannelId IS NOT Null", (interaction.user.id, ))
            data.commit()
            
        close_ticket.callback = close_ticket_callback
        delete_ticket.callback = delete_ticket_callback
    
    @ticket_commands.command(name = 'settings', description = GetMsg("command_ticket_settings_description"))
    @app_commands.checks.has_permissions(administrator = True)
    async def ticket_settings(self, interaction: discord.Interaction, settings: str,  ticket_category: discord.CategoryChannel = None, admin_role: discord.Role = None):
        if settings == "set_open_category" and admin_role is None:
            GuildConfSet(interaction.guild, "ticket_category", str(ticket_category.id))
            embed = discord.Embed(
                title = GetMsg("command_ticket_settings_set_category_embed_title"),
                description = GetMsg("command_ticket_settings_set_category_embed_description", interaction.guild).format(ticket_category.mention),
                color = StrToColor(config["color_ok"])
            )
            await interaction.response.send_message(embed = embed, ephemeral = True)
        elif settings == "set_admin_role" and ticket_category is None:
            GuildConfSet(interaction.guild, "ticket_admin_role", str(admin_role.id))
            embed = discord.Embed(
                title = GetMsg("command_ticket_settings_set_admin_embed_title", interaction.guild),
                description = GetMsg("command_ticket_settings_set_admin_embed_description", interaction.guild).format(admin_role.mention),
                color = StrToColor(config["color_ok"])
            )
            await interaction.response.send_message(embed = embed, ephemeral = True)
        else:
            embed = discord.Embed(
                title = GetMsg("error_general_title", interaction.guild),
                description = GetMsg("error_command_general_description", interaction.guild),
                color = StrToColor(config["color_error"])
            )
            print(GetMsg("error_command_general_description_console").format(interaction.guild.name, interaction.guild.id, GetMsg("error_command_bad_arguments", interaction.guild)))
        
    @ticket_settings.autocomplete("settings")
    async def ticket_settings_autocomplete(self, interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
        data = []
        data.sort()
        
        for command_choice in ['ticket_category', 'set_admin_role']:
            if current.lower() in command_choice.lower():
                data.append(app_commands.Choice(name = command_choice, value = command_choice))
        return data
    
    
    @ticket_settings.error
    async def ticket_settings_error(self, interaction: discord.Interaction, error):
        if isinstance(error, commands.MissingPermissions):
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = GetMsg("error_general_title", interaction.guild),
                    description = GetMsg("error_dont_have_premision", interaction.guild).format(GetMsg("hint_command_ticket_create", interaction.guild).format(GetCommand(0)["name"], GetCommand(0)["id"]), ),
                    color = StrToColor(config["color_error"])
                ),
                ephemeral = True
            )
            print(error)
    
async def setup(bot):
    await bot.add_cog(TicketSys(bot))