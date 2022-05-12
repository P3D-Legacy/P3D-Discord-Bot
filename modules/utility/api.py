def get_bearer_key():
    return "59me0J0mdSPZGjuDjdceTy9FsNBME0qTKpu3JaXL"


def get_base_url():
    return "https://next.pokemon3d.net/api/"


def get_api_version():
    return "v1"


def get_api_headers():
    return {
        "Authorization": f"Bearer {get_bearer_key()}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


def build_api_url():
    return f"{get_base_url()}{get_api_version()}"
