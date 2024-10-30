import discord

from ganyu_utils import *
from discord.ext import commands
from discord import app_commands
from datetime import datetime

config = LoadJson("config.json")
logger = setup_logging()

class ServerCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        
    @app_commands.command(name = "server", description = "Інформація про поточний сервер")
    async def server_(self, interaction: discord.Interaction):
        text_channels = len(interaction.guild.text_channels)
        voice_channels = len(interaction.guild.voice_channels)
        stage_channels = len(interaction.guild.stage_channels)
        total_channels = text_channels + voice_channels + stage_channels
        
        total = len(interaction.guild.members)
        online = len(list(filter(lambda m: str(m.status) == "online", interaction.guild.members)))
        idle = len(list(filter(lambda m: str(m.status) == "idle", interaction.guild.members)))
        offline = len(list(filter(lambda m: str(m.status) == "offline", interaction.guild.members)))
        humans = len(list(filter(lambda m: not m.bot, interaction.guild.members)))
        bots = len(list(filter(lambda m: m.bot, interaction.guild.members)))
        
        schannel_rules = GetMsg("general.none", interaction.guild) if interaction.guild.rules_channel is None else f"<#{interaction.guild.rules_channel.id}>"
        
        nsfwlvl = str(interaction.guild.explicit_content_filter)
        nsfw_filters = {
            "all_members": GetMsg("general.nsfw_filters.all", interaction.guild),
            "no_role": GetMsg("general.nsfw_filters.without_role", interaction.guild),
            "disabled": GetMsg("general.nsfw_filters.disabled", interaction.guild)
        }
        nsfwlvl = nsfw_filters.get(nsfwlvl, GetMsg("general.nsfw_filters.not_found", interaction.guild))
        
        
        
        verification = str(interaction.guild.verification_level)
        verefication_levels = {
            "extreme": GetMsg("general.verification_level.extreme", interaction.guild),
            "high": GetMsg("general.verification_level.high", interaction.guild),
            "medium": GetMsg("general.verification_level.medium", interaction.guild),
            "low": GetMsg("general.verification_level.low", interaction.guild),
            "none": GetMsg("general.verification_level.none", interaction.guild)
        }
        verification = verefication_levels.get(verification, GetMsg("general.verification_level.not_found", interaction.guild))
        
        def GetChannelCount(key:str, tuple: tuple = interaction.guild.channels):
            channels_count = {"TotalChannels": 0}

            for obj in tuple:
                obj_type = type(obj).__name__

                if obj_type in channels_count:
                    channels_count[obj_type] += 1
                else:
                    channels_count[obj_type] = 1

                if obj_type != "CategoryChannel":
                    channels_count["TotalChannels"] += 1

            if key in channels_count:
                return channels_count[key]
            else:
                return None
            
         
        embed = discord.Embed(
            title = GetMsg("commands.server.embed.title", interaction.guild).format(server_name = interaction.guild.name),
            color = HexToColor(config["bot"]["color"]["default"]),
        )
        
        embed.add_field(
            name = GetMsg("commands.server.fields.name.server_owner", interaction.guild), 
            value = interaction.guild.owner.mention,
            inline = True
        )
        
        embed.add_field(
            name = "ID", 
            value = interaction.guild.id, 
            inline = True
        )
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.create_at", interaction.guild)}:", 
            value = f"<t:{int(interaction.guild.created_at.timestamp())}:f>", 
            inline = True
        )
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.сhannel_rules", interaction.guild)}:",
            value = schannel_rules,
            inline = True
        )
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.nsfw_filter", interaction.guild)}:", 
            value = nsfwlvl,
            inline = True
        )
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.verification_level", interaction.guild)}:",
            value = verification,
            inline = True
        )
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.members", interaction.guild)}:", 
            value = GetMsg("commands.server.fields.value.members", interaction.guild).format(
                emoji_total_members = "<:total_members:1301202687123259555>",
                emoji_members = "<:members:1301202604839276574>",
                emoji_bots = "<:bots:1301202569753923649>",
                total_members = total,
                members = humans,
                bots = bots
            ),
            inline = True
        )
        
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.status", interaction.guild)}:", 
            value = GetMsg("commands.server.fields.value.status").format(
                online = online, 
                idle = idle,
                offline = offline,
                emoji_online = "<:online:1301202628805529661>",
                emoji_idle = "<:idle:1301202592734384200>",
                emoji_offline = "<:ofline:1301202615899656212>"
            ), 
            inline = True
        )
        
        embed.add_field(
            name = f"{GetMsg("commands.server.fields.name.channels", interaction.guild)}:", 
            value = GetMsg("commands.server.fields.value.channels", interaction.guild).format(
                total_channels = GetChannelCount("TotalChannels"),
                text_channels = GetChannelCount("TextChannel"),
                voice_channels = GetChannelCount("VoiceChannel"),
                emoji_total_channels = "<:total_channels:1301202676683509810>",
                emoji_text_channels = "<:text_channels:1301202666273116211>",
                emoji_voice_channels = "<:voice_channels:1301202698611462225>"
            )
        )
        
        embed.set_thumbnail(url = interaction.guild.icon)
        
        await interaction.response.send_message(embed = embed, ephemeral = True)
        
        
        
async def setup(bot):
    await bot.add_cog(ServerCommand(bot))