import discord
from discord.ext import commands
import websockets as create_connection
import modules.utility.general as general

client = commands.Bot(command_prefix="!")



client.run(general.get_token())

