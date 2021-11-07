token = open("token.txt", "r").read()

DEBUG = True


def get_token():
    return token


def log(s):
    if DEBUG:
        print(s)


def get_api_uri():
    return "wss://karp.pokemon3d.net/next/api/v1/communication/listener/ws"

