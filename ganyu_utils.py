"""These are auxiliary functions to work bot"""
import logging
import random
import mysql.connector
import discord

from json import loads, dumps
from discord import Guild
from typing import Any, Union
from colorama import init, Fore, Back, Style
from mysql.connector import Error
from discord.ui import View
from typing import List, Optional


try:
    with open("config.json", 'r', encoding="utf-8") as json_file:
        output = loads(json_file.read())
        json_file.close()
except Exception:
    print(Exception)

def LoadJson(filename: str) -> Any:
    """
    Loads and parses a JSON file.

    Args:
        filename (str): The path to the JSON file to be loaded.

    Returns:
        Any: The content of the JSON file parsed into a Python object. 
             If an error occurs, returns an empty dictionary.

    Raises:
        Exception: If there is an issue opening or reading the file, or parsing the JSON.

    Notes:
        - The function handles exceptions and prints an error message if the file cannot be loaded.
        - The file is expected to be in UTF-8 encoding.

    Example:
        >>> LoadJson("data/config.json")
        {'key': 'value'}
    """
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            output = loads(json_file.read())
            json_file.close()
    except Exception as exp:
        print("Could not load json file {0} due to exception {1}".format(filename, exp))
        output = {}
    return output


def GuildLocaleGet(guild: Guild) -> str:
    """
    Retrieves the locale setting for a specific guild.

    Args:
        guild (Guild): The guild for which the locale setting is to be retrieved.

    Returns:
        str: The locale code for the guild. If no specific locale is set, 
             returns the default bot locale.

    Notes:
        - This function first tries to retrieve the locale from the guild's configuration.
        - If the locale is not found or is empty, it defaults to the bot's locale specified in the `config.json` file.
        - The `GuildConfGet` function is commented out but can be used to fetch the locale setting from guild-specific configuration.
    """
    config = LoadJson("config.json")
    try:
        locale = config["bot"]["locale"]
        #locale = GuildConfGet(guild, "locale")
    except KeyError:
        return config["bot"]["locale"]
    return locale or config["bot"]["locale"]


def GetMsg(key: str, guild: Union[Guild, None] = None) -> str:
    try:
        lang = LoadJson("config.json")
    
        locale = (
            LoadJson(f'locale/{lang["bot"]["locale"]}.json')
            if guild is None
            else LoadJson(f'locale/{GuildLocaleGet(guild)}.json')
        )
        keys = key.split('.')
        
        msg = locale
        for k in keys:
            msg = msg[k]

        return msg
    except Exception as exp:
        print(f"Could not get locale string for key '{key}' due to exception {exp}")
        return key


def HexToColor(hex_string: str) -> int:
    """
    Converts a hexadecimal color code to a Discord color integer.

    Args:
        hex_string (str): A string representing a color in hexadecimal format. 
                          It should be in the format '#RRGGBB' or 'RRGGBB'.

    Returns:
        int: An integer representing the Discord color value.

    Example:
        >>> HexToColor("#FF5733")
        16734003
    """
    return int(hex(int(hex_string.replace("#", ""), 16)), 0)

def HexToRgb(hex: str) -> tuple:
    """
    Converts a hexadecimal color code to an RGB tuple.

    Args:
        hex (str): A string representing a color in hexadecimal format. 
                   It should be in the format '#RRGGBB' or 'RRGGBB'. 

    Returns:
        tuple: A tuple containing the RGB values, each as an integer between 0 and 255.

    Raises:
        ValueError: If the input hexadecimal color code is longer than 7 characters.

    Example:
        >>> HexToRgb("#FF5733")
        (255, 87, 51)
    """
    if len(hex) > 7:
        raise ValueError("Color size exceeds 7 characters")
    
    if hex.startswith("#"):
        hex = hex[1:]
    
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    
    return tuple(rgb)


def RandomColor() -> tuple[int, int, int]:
    """
    Generates a random RGB color.

    Returns:
        tuple[int, int, int]: A tuple containing three integers representing
        the red, green, and blue components of the color, each in the range 0
        to 255.

    Example:
        >>> RandomColor()
        (123, 45, 67)
    """
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue


def GetCommand(id: int) -> dict:
    """
    Retrieves a bot command configuration by its ID.

    Args:
        id (int): The ID of the bot command to retrieve.

    Returns:
        dict: A dictionary containing the configuration of the command. 
              If the command cannot be found or an error occurs, returns an empty dictionary.

    Raises:
        Exception: If there is an issue loading the JSON file or retrieving the command.

    Example:
        >>> GetCommand(123)
        {"name": "help", "id": "1264711630495809577"}
    """
    try:
        config = LoadJson('config.json')
        return config["bot_commands"][str(id)]
    except Exception as exp:
        print(f"Failed to get command at {id} due to an exception")


class ColorPrinter():
    def __init__(self, text):
        init()
        self.text = text
        self.fore_color = Fore.RESET
        self.back_color = Back.RESET
        self.style = Style.NORMAL

    def set_color(self, color):
        self.fore_color = getattr(Fore, color.upper(), Fore.RESET)
        return self

    def set_bcolor(self, color):
        self.back_color = getattr(Back, color.upper(), Back.RESET)
        return self

    def set_style(self, style):
        self.style = getattr(Style, style.upper(), Style.NORMAL)
        return self

    def formating(self):
        return f"{self.style}{self.fore_color}{self.back_color}{self.text}{Style.RESET_ALL}"
    
    def __str__(self):
        return self.formating()
    
    @staticmethod
    def list_colors() -> list:
        colors = [attr for attr in dir(Fore) if not attr.startswith('_')]
        return colors

    @staticmethod
    def list_bcolors() -> list:
        bcolors = [attr for attr in dir(Back) if not attr.startswith('_')]
        return bcolors

    @staticmethod
    def list_styles() -> list:
        styles = [attr for attr in dir(Style) if not attr.startswith('_')]
        return styles
            
def setup_logging():
    config = LoadJson("config.json")
    
    # Converting a string to the appropriate logging level
    log_level = getattr(logging, config["loging"]["log_leveling"].upper(), logging.WARNING)

    # Login settings
    logger = logging.getLogger('discord')
    logger.setLevel(log_level)  # Sets the logging level according to the configuration

    # Handler for writing to a file
    file_handler = logging.FileHandler(filename=config["loging"]["log_file_path"], encoding='utf-8', mode='w')
    file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(file_handler)

    # # Handler for output to the console
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(log_level)
    # console_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    # logger.addHandler(console_handler)

    return logger

class Database:
    def __init__(self, host, user, password, database):
        self.connection = None
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.loggin = setup_logging()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                logging.info("Successfully connected to the database")
        except Error as e:
            logging.error("Error while connecting to MySQL:\n", e)
            
    def commit(self):
        if self.connection.is_connected():
            self.connection.commit()
        else:
            logging.error("Database is not connected")

    def close(self):
        if self.connection.is_connected():
            self.connection.close()
            logging.error("Database connection closed")
            
            
class PagginationView(View):
    def __init__(self, embeds: List[discord.Embed], select_menu: Optional[discord.ui.Select]) -> None:
        super().__init__()
        
        self._embeds = embeds
        self._initial = embeds[0] # First embed
        self._len = len(embeds)
        self._current_page = 1
        self.children[0].disabled = True
        self.children[1].disabled = True
        self.children[2].label = f"{self._current_page}/{self._len}"
        
        if select_menu:
            self.add_item(select_menu)
        
    async def update_butons(self, interaction: discord.Interaction) -> None:
        self.children[0].disabled = self._current_page == 1  # Previous
        self.children[1].disabled = self._current_page == 1  # First
        self.children[2].label = f"{self._current_page}/{self._len}"
        self.children[3].disabled = self._current_page == self._len  # Last
        self.children[4].disabled = self._current_page == self._len  # Next
        
        await interaction.edit_original_response(view=self)
    
    @discord.ui.button(emoji="⏪")
    async def first(self, interaction: discord.Interaction, _):
        self._current_page = 1
        await interaction.response.edit_message(embed=self._embeds[self._current_page - 1])
        await self.update_butons(interaction)
    
    @discord.ui.button(emoji="◀️")
    async def previous(self, interaction: discord.Interaction, _):
        if self._current_page > 1:
            self._current_page -= 1
            await interaction.response.edit_message(embed=self._embeds[self._current_page - 1])
            await self.update_butons(interaction)
            
            
    @discord.ui.button(style=discord.ButtonStyle.danger,  disabled=True)
    async def curent_page(self, interaction: discord.Interaction, _):
        pass
        
    @discord.ui.button(emoji="▶️")
    async def next(self, interaction: discord.Interaction, _):
        if self._current_page < self._len:
            self._current_page += 1
            await interaction.response.edit_message(embed=self._embeds[self._current_page - 1])
            await self.update_butons(interaction)
        
    @discord.ui.button(emoji="⏩")
    async def last(self, interaction: discord.Interaction, _):
        self._current_page = self._len
        await interaction.response.edit_message(embed=self._embeds[self._current_page - 1])
        await self.update_butons(interaction)
        
    @property
    def initial(self) -> discord.Embed:
        return self._initial
    
