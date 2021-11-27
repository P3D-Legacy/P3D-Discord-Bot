import asyncio

import discord
from discord.ext import commands
import modules.utility.general as p3d_utility
import modules.utility.server_connection as sc

client = commands.Bot(command_prefix="!")

client.websocket = None


async def init_websocket():
    client.websocket = await sc.connect_to_p3d(client)


@client.event
async def on_guild_join(guild):
    p3d_category = discord.utils.get(guild.categories, id=p3d_utility.get_category_id())
    p3d_server_chat = discord.utils.get(guild.channels, id=p3d_utility.get_server_chat_channel_id())

    if not p3d_category:
        p3d_category = await guild.create_category(p3d_utility.get_p3d_category_name(), overwrites=None, reason=None)

    if not p3d_server_chat:
        await guild.create_text_channel(p3d_utility.get_p3d_server_chat_name(), category=p3d_category)


@client.event
async def on_ready():
    await init_websocket()
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(context):
    if context.author == client.user or context.author.bot:
        return

    if context.channel.id == p3d_utility.get_server_chat_channel_id():
        await sc.handle_discord_message(context, client.websocket)


client.run(p3d_utility.get_token())
