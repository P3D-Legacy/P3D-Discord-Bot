import websockets
import json
import asyncio
import modules.utility.general as p3d_utility
import modules.chat.server_client_chat as scc


async def connect_to_p3d(bot):
    if not hasattr(bot, 'websocket'):
        async with websockets.connect(p3d_utility.get_api_uri(), ssl=True, subprotocols=['json']) as bot.websocket:
            await bot.websocket.send('{"botName": "DiscordBot", "type": 1}')
            async for message in bot.websocket:
                if message is not None:
                    await handle_websocket_message(message, bot)
    else:
        async for message in bot.format_message_according_to_typewebsocket:
            if message is not None:
                await handle_websocket_message(message, bot)


async def handle_websocket_message(message, bot):
    converted_response = json.loads(message)
    print(converted_response)
    if "success" not in converted_response["type"]:
        if 'player' in converted_response and "DiscordBot" not in converted_response['player']:
            await scc.handle_response(converted_response, bot)
        else:
            if 'player' not in converted_response:
                await scc.handle_response(converted_response, bot)


async def handle_discord_message(context, bot):
    if not hasattr(bot, 'websocket'):
        await bot.wait_until_ready()
        while not bot.is_closed():
            await connect_to_p3d(bot)
            await asyncio.sleep(1)
            websocket = bot.websocket
    else:
        websocket = bot.websocket

    cleaned_text = p3d_utility.clean_text(context)
    if cleaned_text:
        constructed_message = {
            "sender": f"{context.author.name}",
            "message": f"{cleaned_text}",
            "type": 2
        }
        message_to_send = json.dumps(constructed_message)
        await websocket.send(message_to_send)
