import asyncio
import discord

token = open("token.txt", "r").read()

DEBUG = True


def get_token():
    return token


def log(s):
    if DEBUG:
        print(s)


def get_api_uri():
    return "wss://karp.pokemon3d.net/next/api/v1/communication/listener/ws"


def get_category_id():
    return 895408984700375051


def get_server_chat_channel_id():
    return 908438756850274304


def get_p3d_category_name():
    return "Server API"


def get_p3d_server_chat_name():
    return "P3D Server chat"


async def get_p3d_category(client):
    await asyncio.sleep(0.1)
    return discord.Client.get_channel(client, get_category_id())


async def get_p3d_server_client_chat(client):
    await asyncio.sleep(0.1)
    return discord.Client.get_channel(client, get_server_chat_channel_id())
