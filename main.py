import discord
from discord.ext import commands
from pprint import pprint
import websockets as create_connection
import modules.utility.general as general

client = commands.Bot(command_prefix="!")


@client.event
async def on_guild_join(guild):
    pd3_category = discord.utils.get(guild.categories, id=general.get_category_id())
    pd3_server_chat = discord.utils.get(guild.channels, id=general.get_server_chat_channel_id())

    if not pd3_category:
        pd3_category = await guild.create_category(general.get_pd3_category_name(), overwrites=None, reason=None)

    if not pd3_server_chat:
        await guild.create_text_channel(general.get_pd3_server_chat_name(), category=pd3_category)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))




client.run(general.get_token())

