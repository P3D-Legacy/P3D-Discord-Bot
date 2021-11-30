import asyncio
import websockets
import json
import modules.utility.general as p3d_utility
import modules.chat.server_client_chat as scc


async def connect_to_p3d(client):
    if not hasattr(client, 'websocket'):
        async with websockets.connect(p3d_utility.get_api_uri(), ssl=True, subprotocols=['json']) as client.websocket:
            await client.websocket.send('{"botName": "DiscordBot", "type": 1}')
            async for message in client.websocket:
                if message is not None:
                    await handle_websocket_message(message, client)
    else:
        async for message in client.websocket:
            if message is not None:
                await handle_websocket_message(message, client)


async def handle_websocket_message(message, client):
    converted_response = json.loads(message)
    if "success" not in converted_response["type"] and "DiscordBot" not in converted_response['player']:
        await scc.handle_response(converted_response, client)


async def handle_discord_message(context, websocket):
    constructed_message = {
        "sender": f"{context.author.name}",
        "message": f"{context.content}",
        "type": 2
    }
    message_to_send = json.dumps(constructed_message)
    await websocket.send(message_to_send)
