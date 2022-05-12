import modules.utility.general as p3d_utility


async def handle_response(response, bot):
    p3d_category = await p3d_utility.get_p3d_category(bot)
    await format_message_according_to_type(p3d_category, bot, response)


async def format_message_according_to_type(category, bot, response):
    chat_channel = await p3d_utility.get_p3d_server_client_chat_channel(bot)
    match response['type']:
        case 1 | 'playerJoined':
            await chat_channel.send(f"```fix\n[SERVER]: The player {response['player']} joined the game```")
        case 2 | 'playerLeft':
            await chat_channel.send(f"```fix\n[SERVER]: The player {response['player']} left the game```")
        case 3 | 'playerSentGlobalMessage':
            await chat_channel.send(f"__*[In-Game-Chat]*__  **{response['player']}**: {response['message']}")
        case 5 | 'playerTriggeredEvent':
            result = await p3d_utility.handle_server_message(response, bot)
            result['response'].set_footer(
                text="The P3D Team",
                icon_url="https://pokemon3d.net/img/TreeLogoSmall.png"
            )
            result['response'].set_author(
                name="Pokemon3D.net",
                url="https://pokemon3d.net/",
                icon_url="https://pokemon3d.net/img/pokemon3d_logo_sm.png"
            )
            await result['channel'].send(embed=result['response'])
        case _:
            await chat_channel.send("Not yet implemented")
