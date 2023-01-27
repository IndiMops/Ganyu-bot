from json import loads, dumps
from discord import Guild
from os import listdir, makedirs, remove, stat, path
from typing import Any, Literal, Union



try:
    with open("config.json", 'r', encoding="utf-8") as json_file:
        output = loads(json_file.read())
        json_file.close()
except Exception:
    print(Exception)


def SaveJson(value: Any, filename: str) -> None:
    with open(filename, 'w', encoding="utf-8") as f:
        f.write(dumps(value, indent=4, ensure_ascii=False))
        f.close()

      
def LoadJson(filename: str) -> Any:
    try:
        with open(filename, 'r', encoding="utf-8") as json_file:
            output = loads(json_file.read())
            json_file.close()
    except Exception as exp:
        print(f"Could not load json file {filename} due to exception {exp}")
        output = {}
    return output


def GuildConfGet(guild: Guild, variable: str) -> Any:
    global debug
    try:
        config = LoadJson(f"guilds/{str(guild.id)}/config.json")
        return config[variable]
    except Exception as exp:
        print(f"Could not get guild config key '{variable}' due to {exp}", guild)
        return None
    
def GuildConfSet(guild: Guild, variable: str, value: Any) -> None:
    config = LoadJson(f"guilds/{str(guild.id)}/config.json")
    config[variable] = value
    try:
        SaveJson(config, f"guilds/{str(guild.id)}/config.json")
    except:
        makedirs(f"guilds/{str(guild.id)}", exist_ok=True)
        makedirs(f"guilds/{str(guild.id)}/channels", exist_ok=True)
        SaveJson(config, f"guilds/{str(guild.id)}/config.json")
    print(f"Guild config key '{variable}' is now set to '{value}'", guild)


def GuildConfReset(guild: Guild, variable: str) -> None:
    try:
        config = LoadJson(f"guilds/{str(guild.id)}/config.json")
        del config[variable]
        try:
            SaveJson(config, f"guilds/{str(guild.id)}/config.json")
        except:
            makedirs(f"guilds/{str(guild.id)}", exist_ok=True)
            makedirs(f"guilds/{str(guild.id)}/channels", exist_ok=True)
            SaveJson(config, f"guilds/{str(guild.id)}/config.json")
        print(f"Guild config key '{variable}' has been reset", guild)
    except Exception as exp:
        print(f"Could not reset guild config key '{variable}' due to {exp}", guild)


def GuildLocaleGet(guild: Guild) -> str:
    config = LoadJson(f"config.json")
    try:
        locale = GuildConfGet(guild, "locale")
    except:
        return config["bot_locale"]
    if locale is None:
        return config["bot_locale"]
    else:
        return locale


def GetMsg(string: str, guild: Union[Guild, None] = None) -> str:
    try:
        locale = LoadJson(f'locale/{GuildLocaleGet(guild)}.json')
        return locale["messages"][string]
    except Exception as exp:
        print(f"Could not get locale string named {string} due to exception {exp}", guild)
        return string

def StrToColor(string: str) -> int:
    return int(hex(int(string.replace("#", ""), 16)), 0)
