import discord
import asyncio
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


@client.event
async def on_message(context):
    if context.author == client.user or context.author.bot:
        return

    if context.channel.id == p3d_utility.get_server_chat_channel_id():
        await sc.handle_discord_message(context, client.websocket)


async def read_messages():
    await client.wait_until_ready()
    while not client.is_closed():
        await sc.connect_to_p3d(client)
        await asyncio.sleep(1)

client.loop.create_task(read_messages())
client.run(p3d_utility.get_token())
