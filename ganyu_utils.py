"""These are auxiliary functions to work bot"""
import logging
import random
import time

from json import loads, dumps
from discord import Guild
from typing import Any, Union
from colorama import init, Fore, Back, Style
from time import time

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
        locale = config["bot_locale"]
        #locale = GuildConfGet(guild, "locale")
    except KeyError:
        return config["bot_locale"]
    return locale or config["bot_locale"]


def GetMsg(string: str, guild: Union[Guild, None] = None) -> str:
    """
    Retrieves a localized message string based on the provided key and guild context.

    Args:
        string (str): The key for the localized message string.
        guild (Union[Guild, None], optional): The guild context used to determine the locale. 
                                               If None, the default bot locale is used. Defaults to None.

    Returns:
        str: The localized message string corresponding to the provided key. 
             If an error occurs or the key is not found, returns the key itself.

    Raises:
        Exception: If there is an issue loading the locale files or retrieving the message.

    Example:
        >>> GetMsg("welcome_message")
        "Welcome to the server!"

    Notes:
        - This function loads locale data from JSON files based on the bot's or guild's locale.
        - The locale JSON files should be in the 'locale' directory with names matching the locale codes.
    """
    try:
        lang = LoadJson("config.json")
        if guild is None:
            locale = LoadJson(f'locale/{lang["bot_locale"]}.json')
        else:
            locale = LoadJson(f'locale/{GuildLocaleGet(guild)}.json')
        return locale["messages"][string]
    except Exception as exp:
        print(
            f"Could not get locale string named {string} due to exception {exp}", guild)
        return string


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
