import asyncio
import json
import discord
from discord.ext import commands
import websockets
import modules.utility.general as general
from pprint import pprint

client = commands.Bot(command_prefix="!")

uri = 'wss://karp.pokemon3d.net/next/api/v1/communication/listener/ws:80'


async def send_message():
    async with websockets.connect(uri) as websocket:
        message = input("msg: ")

        await websocket.send(message)
        print(f"[ws client] message  > {message}")

        #answer = await websocket.recv()
        #print(f"[ws client] answer < {answer}")

asyncio.get_event_loop().run_until_complete(send_message())


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


print(f"running connection to {general.get_api_uri()}")


client.run(general.get_token())
