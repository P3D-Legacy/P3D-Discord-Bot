import asyncio
import discord
import emoji
import discord.utils as utils
import re

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
    return 907011413594210324


def get_server_chat_channel_id():
    return 907011414332420146


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


def clean_text(context):
    remove_formatting = utils.remove_markdown(context.content)
    removed_extern_emojis = re.sub(r'<:\w*:\d*>', '', remove_formatting)
    removed_intern_emojis = remove_emojis(removed_extern_emojis)
    for member in context.mentions:
        removed_intern_emojis = removed_intern_emojis.replace(f'<@!{member.id}>', member.name)

    return ' '.join(removed_intern_emojis.split())


def remove_emojis(data):
    emoj = re.compile("["
                      u"\U0001F600-\U0001F64F"  # emoticons
                      u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                      u"\U0001F680-\U0001F6FF"  # transport & map symbols
                      u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                      u"\U00002500-\U00002BEF"  # chinese char
                      u"\U00002702-\U000027B0"
                      u"\U00002702-\U000027B0"
                      u"\U000024C2-\U0001F251"
                      u"\U0001f926-\U0001f937"
                      u"\U00010000-\U0010ffff"
                      u"\u2640-\u2642"
                      u"\u2600-\u2B55"
                      u"\u200d"
                      u"\u23cf"
                      u"\u23e9"
                      u"\u231a"
                      u"\ufe0f"  # dingbats
                      u"\u3030"
                      "]+", re.UNICODE)
    return re.sub(emoj, '', data)
