import discord
import logging
import asyncio
from discord.ext import commands
import modules.utility.general as p3d_utility
import modules.utility.server_connection as sc

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class P3DBot(commands.Bot):

    def __init__(self):
        super().__init__(
            command_prefix='$',
            intents=discord.Intents.all(),
            application_id=906994811469438996
        )

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID:{self.user.id}))')
        self.loop.create_task(self.read_messages())

    async def on_message(self, message):
        if message.author == self.user or message.author.bot:
            return

        if message.channel.id == p3d_utility.get_server_chat_channel_id():
            await sc.handle_discord_message(message, self)

    async def read_messages(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await sc.connect_to_p3d(self)
            await asyncio.sleep(1)


bot = P3DBot()
bot.run(p3d_utility.get_token())
