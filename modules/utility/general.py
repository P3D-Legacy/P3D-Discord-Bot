import asyncio
import discord
import discord.utils as utils
import re
import requests
import modules.utility.api as api

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


def get_server_event_channel_id():
    return 966381196126871552


def get_p3d_category_name():
    return "Server API"


def get_p3d_server_chat_name():
    return "P3D Server chat"


def get_p3d_server_event_name():
    return "P3D Game Events"


async def get_p3d_category(client):
    await asyncio.sleep(0.1)
    return discord.Client.get_channel(client, get_category_id())


async def get_p3d_server_client_chat_channel(client):
    await asyncio.sleep(0.1)
    return discord.Client.get_channel(client, get_server_chat_channel_id())


async def get_p3d_server_client_event_channel(client):
    await asyncio.sleep(0.1)
    return discord.Client.get_channel(client, get_server_event_channel_id())


def clean_text(context):
    remove_formatting = utils.remove_markdown(context.content)
    removed_extern_emojis = re.sub(r'<:\w*:\d*>', '', remove_formatting)
    removed_intern_emojis = remove_emojis(removed_extern_emojis)
    removed_roles = re.sub(r'<@&\d*>', '', removed_intern_emojis)
    print(removed_roles)
    for member in context.mentions:
        removed_roles = removed_roles.replace(f'<@!{member.id}>', member.name)

    return ' '.join(removed_roles.split())


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


async def handle_server_message(response, bot):
    if response['event'].get('eventType') == 'evolvedPokemon':
        return {'response': get_evolved_message(response), 'channel': await get_p3d_server_client_event_channel(bot)}

    if response['event'].get('eventType') == 'defeatedByWildPokemon':
        return {'response': get_defeated_by_wild_pokemon(response), 'channel': await get_p3d_server_client_event_channel(bot)}

    if response['event'].get('eventType') == 'defeatedByTrainer':
        return {'response': get_defeated_by_trainer(response), 'channel': await get_p3d_server_client_event_channel(bot)}

    if response['event'].get('eventType') == 'achievedEmblem':
        return {'response': get_achieved_emblem(response), 'channel': await get_p3d_server_client_event_channel(bot)}

    if response['event'].get('eventType') == 'hostedABattle':
        return {'response': get_hosted_a_battle(response), 'channel': await get_p3d_server_client_event_channel(bot)}

    return ''


def get_evolved_message(response):
    evolved_pokemon = response['event']['evolvedPokemonName']
    pokemon_image = get_pokemon_image(evolved_pokemon.lower())
    embed = discord.Embed(title="Evolved",
                          description=f"The player {response['player']} evolved their {response['event']['pokemonName']} into a  {evolved_pokemon}",
                          color=0x5CB85C)
    embed.set_thumbnail(url=pokemon_image)

    print(embed)

    return embed


def get_defeated_by_wild_pokemon(response):
    wild_pokemon = response['event']['pokemonName']
    pokemon_image = get_pokemon_image(wild_pokemon.lower())
    embed = discord.Embed(title="Defeated by wild Pokemon",
                          description=f"The player {response['player']} got defeated by a wild {response['event']['pokemonName']}",
                          color=0x5CB85C)
    embed.set_thumbnail(url=pokemon_image)

    return embed


def get_defeated_by_trainer(response):
    trainer_image = get_trainer_image()
    embed = discord.Embed(title="Defeated by trainer",
                          description=f"The player {response['player']} got defeated by {response['event']['trainerTypeAndName']}",
                          color=0x5CB85C)
    embed.set_thumbnail(url=trainer_image)

    return embed


def get_hosted_a_battle(response):
    vs_image = get_vs_image()
    embed = discord.Embed(title=f"Player Online Battle",
                          description=f"The player {response['player']} hosted a battle.",
                          color=0x5CB85C)
    embed.add_field(name="Won", value=f"{response['event']['trainer']}", inline=True)
    embed.add_field(name="Lost", value=f"{response['event']['defeatedTrainer']}", inline=True)
    embed.set_thumbnail(url=vs_image)

    return embed


def get_pokemon_image(pokemon):
    pokemon_info = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemon}")
    if pokemon_info.status_code == 200:
        info_as_json = pokemon_info.json()
        image = info_as_json['sprites']['other']['official-artwork']['front_default']
        if image:
            return image

    return ''


def get_trainer_image():
    trainer = requests.get(
        "https://static.wikia.nocookie.net/versus-compendium/images/3/3f/Pkmn_Red.png/revision/latest/scale-to-width-down/150?cb=20181108121419")
    if trainer.status_code == 200:
        return 'https://static.wikia.nocookie.net/versus-compendium/images/3/3f/Pkmn_Red.png/revision/latest/scale-to-width-down/150?cb=20181108121419'

    return ''


def get_vs_image():
    vs = requests.get(
        "https://st3.depositphotos.com/1001599/17060/i/450/depositphotos_170606960-stock-photo-versus-vs-sign-in-fire.jpg")
    if vs.status_code == 200:
        return 'https://st3.depositphotos.com/1001599/17060/i/450/depositphotos_170606960-stock-photo-versus-vs-sign-in-fire.jpg'

    return ''


def get_achieved_emblem(response):
    achieved_emblem_image = get_achievement_image(response['event']['emblem'])
    embed = discord.Embed(title="Emblem",
                          description=f"The player **{response['player']}** achieved the emblem **{response['event']['emblem']}**",
                          color=0x5CB85C)
    embed.set_thumbnail(url=achieved_emblem_image)

    return embed


def get_achievement_image(name):
    clean_name = name.replace(" ", "_").lower()
    badges = requests.get(f"{api.build_api_url()}/game/badges", headers=api.get_api_headers())
    if badges.status_code == 200:
        badges_json = badges.json()
        if clean_name in badges_json['data']:
            return badges_json['data'][clean_name]['image']

    return ''


