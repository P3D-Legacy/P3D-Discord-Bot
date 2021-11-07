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
    return


def get_server_chat_channel_id():
    return


def get_pd3_category_name():
    return "Server API"


def get_pd3_server_chat_name():
    return "PD3 Server chat"

