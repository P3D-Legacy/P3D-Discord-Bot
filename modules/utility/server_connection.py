import websockets
import asyncio
import json
import modules.utility.general as p3d_utility
import modules.chat.server_client_chat as scc


async def connect_to_p3d(client):
    async with websockets.connect(p3d_utility.get_api_uri(), ssl=True, subprotocols=['json']) as client.websocket:
        await client.websocket.send('{"botName": "DiscordBot", "type": 1}')
        return client.websocket


async def handle_connection(websocket, client=None, context=None):
    try:
        async for response in websocket:
            if response is not None:
                print(response)
                converted_response = json.loads(response)
                if "success" in converted_response["type"] and context:
                    await handle_discord_message(context, websocket, converted_response)
                    context = None
                if client is not None:
                    if "<BOT>" not in converted_response["player"] and client:
                        await scc.handle_response(converted_response, 'post', client)
    except Exception as e:
        await asyncio.sleep(0.1)
        print('Error receiving message from websocket.')
        print(e)


async def handle_discord_message(context, websocket):
    constructed_message = {
        "sender": f"{context.author.name}",
        "message": f"{context.content}",
        "type": 2
    }
    message_to_send = json.dumps(constructed_message)
    print(message_to_send)
    await websocket.send(message_to_send)
