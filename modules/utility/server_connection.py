import websockets
import asyncio
import json
import modules.chat.server_client_chat as scc


async def connect_to_p3d(uri, client):
    websocket = await websockets.connect(uri, ssl=True, subprotocols=['json'])
    while True:
        if not websocket.open:
            try:
                await asyncio.sleep(0.1)
                print('Websocket is NOT connected. Reconnecting...')
                websocket = await websockets.connect(uri, ssl=True)
            except:
                await asyncio.sleep(1)
                print('Unable to reconnect, trying again.')
        try:
            async for response in websocket:
                if response is not None:
                    await scc.handle_response(json.loads(response), 'post', client)
        except Exception as e:
            await asyncio.sleep(0.1)
            print('Error receiving message from websocket.')
            print(e)


