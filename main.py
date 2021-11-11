import asyncio
import discord
from discord.ext import commands
import modules.utility.general as p3d_utility
import modules.utility.server_connection as sc

client = commands.Bot(command_prefix="!")


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
    print('We have logged in as {0.user}'.format(client))

    await asyncio.create_task(sc.connect_to_p3d(p3d_utility.get_api_uri(), client))


client.run(p3d_utility.get_token())
