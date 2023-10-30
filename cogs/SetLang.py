import discord
from os import listdir, path
import json
from discord import app_commands
from discord.ext import commands
from ganyu import GetMsg, GuildConfGet, GuildConfReset, GuildConfSet, LoadJson, StrToColor

# Define a new cog for language settings
class SetLang(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Define a group of commands for language settings
    locale_group = app_commands.Group(name = 'locale', description='language settings')

    # Command to set the language
    @locale_group.command(name = 'set', description = GetMsg("command_descriptions_locale_set"))
    @app_commands.describe(lang = GetMsg("command_describe_locale_set"))
    @app_commands.choices(lang = [
        app_commands.Choice(name = 'English', value='en'),
        app_commands.Choice(name = 'Українська(Ukrainian)', value='uk'),
        app_commands.Choice(name = '日本語(Japanese)', value='jp'),
        app_commands.Choice(name = 'Polski(Polish)', value='pl')
    ])
    async def local_set(self, interaction: discord.Interaction, lang: str):
        # Load configuration from a JSON file
        config = LoadJson("config.json")

        # Check if the interaction happened in a guild (server)
        if interaction.guild is not None:
            if lang + ".json" in listdir(f"locale"):
                # Set the language in the guild's configuration
                GuildConfSet(interaction.guild, "locale", lang)

                # Send a confirmation message
                await interaction.response.send_message(
                    embed = discord.Embed(
                        title = GetMsg("set_locale_title", interaction.guild),
                        description = GetMsg("set_locale_description", interaction.guild).format(
                            GetMsg("locale_name", interaction.guild)),
                        color = StrToColor(config["color_ok"])
                    )
                )
        else:
            # If the interaction is in a DM, send an error message
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = GetMsg("dm_title", interaction.guild),
                    description = GetMsg("dm_description", interaction.guild),
                    color = StrToColor(config["color_error"])
                )
            )

    # Command to reset the language to the default
    @locale_group.command(name = 'reset', description = GetMsg("command_descriptions_locale_reset"))
    async def local_reset(self, interaction: discord.Interaction):
        config = LoadJson("config.json")
        if interaction.guild is not None:
            GuildConfSet(interaction.guild, "locale", config["bot_locale"])
            # Send a confirmation message with ephemeral set to True (only visible to the user who triggered the command)
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = GetMsg("reset_locale_title". interaction.guild),
                    description = GetMsg("reset_locale_description", interaction.guild).format(
                        GetMsg("locale_name", interaction.guild)),
                    color = StrToColor(config["color_ok"])
                ),
                ephemeral = True
            )
        else:
            await interaction.response.send_message(
                embed = discord.Embed(
                    title = GetMsg("dm_title", interaction.guild),
                    description = GetMsg("dm_description", interaction.guild),
                    color = StrToColor(config["color_error"])
                ),
                ephemeral = True
            )

    # Command to view available languages
    @locale_group.command(name='view', description = GetMsg("command_descriptions_locale_view"))
    async def locale_view(self, interaction: discord.Interaction):
        config = LoadJson("config.json")
        folder_path = 'locale'

        locales = []

        # Iterate through all files in the folder
        for filename in listdir(folder_path):
            file_path = path.join(folder_path, filename)

            # Check if it's a JSON file
            if path.isfile(file_path) and filename.endswith('.json'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    try:
                        data = json.load(file)

                        # Check if "messages" and "locale_name" keys exist
                        if 'messages' in data and 'locale_name' in data['messages']:
                            locale_name = data['messages']['locale_name']

                            # Save the value in a dictionary
                            locales.append(locale_name)

                    except json.JSONDecodeError:
                        print(f"Error decoding JSON in file: {file_path}")

        # Display unique "locale_name" values
        embed = discord.Embed(
            description = ', '.join([f"`{locale}`" for locale in locales]),
            color = StrToColor(config["color_default"])
        )
        embed.set_author(
            name = GetMsg("language_avalible_title", interaction.guild),
            icon_url = "https://media.discordapp.net/attachments/939569454390603837/1158850324128350289/gl.png"
        )

        def modify_locale(locale_code):
            if locale_code == "uk":
                return "ua"
            elif locale_code == "en":
                return "gb"
            elif locale_code is None:
                return "uk"
            else:
                return locale_code

        embed.add_field(
            name = GetMsg("language_curent_language_title", interaction.guild),
            value = f':flag_{modify_locale(GuildConfGet(interaction.guild, "locale"))}: {GetMsg("locale_name", interaction.guild)}',
            inline = True
        )
        embed.add_field(
            name = GetMsg("language_join_crowdir_title", interaction.guild),
            value = GetMsg("language_join_crowdir_desciption", interaction.guild).format(config["other_links"]["crowdir"]),
            inline = False

        )
        # Send the embed with ephemeral set to True
        await interaction.response.send_message(embed = embed, ephemeral=True)
        print(locales)

# Function to set up the cog
async def setup(bot):
    await bot.add_cog(SetLang(bot))
