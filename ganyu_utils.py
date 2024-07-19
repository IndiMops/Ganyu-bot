"""These are auxiliary functions to work bot"""
import random

from json import loads, dumps
from discord import Guild
from typing import Any, Union
from colorama import init, Fore, Back, Style

try:
    with open("config.json", 'r', encoding="utf-8") as json_file:
        output = loads(json_file.read())
        json_file.close()
except Exception:
    print(Exception)

def LoadJson(filename: str) -> Any:
    try:
        with open(filename, "r", encoding="utf-8") as json_file:
            output = loads(json_file.read())
            json_file.close()
    except Exception as exp:
        print("Could not load json file {0} due to exception {1}".format(filename, exp))
        output = {}
    return output


def GuildLocaleGet(guild: Guild) -> str:
    config = LoadJson("config.json")
    try:
        locale = config["bot_locale"]
        #locale = GuildConfGet(guild, "locale")
    except KeyError:
        return config["bot_locale"]
    return locale or config["bot_locale"]


def GetMsg(string: str, guild: Union[Guild, None] = None) -> str:
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


def HexToColor(string: str) -> int:
    """Convert HEX color to Discord color"""
    return int(hex(int(string.replace("#", ""), 16)), 0)

def HexToRgb(hex: str) -> tuple:
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
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)

    return red, green, blue


def GetCommand(id: int) -> dict:
    """Getting the bot command by its ID"""
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
            

    
