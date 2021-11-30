import modules.utility.general as p3d_utility


async def handle_response(response, client):
    p3d_category = await p3d_utility.get_p3d_category(client)
    p3d_server_client_chat = await p3d_utility.get_p3d_server_client_chat(client)
    formatted_message = format_message_according_to_type(response)

    if formatted_message:
        await send_message_to_channel(p3d_category, p3d_server_client_chat, formatted_message)


def format_message_according_to_type(response):
    match response['type']:
        case 1 | 'playerJoined':
            message = f"```fix\n[SERVER]: The player {response['player']} joined the game```"
        case 2 | 'playerLeft':
            message = f"```fix\n[SERVER]: The player {response['player']} left the game```"
        case 3 | 'playerSentGlobalMessage':
            message = f"__*[In-Game-Chat]*__  **{response['player']}**: {response['message']}"
        case _:
            message = "Not yet implemented"

    return message


async def send_message_to_channel(category, channel, message):
    await channel.send(message)
