from settings import ADMIN_USERS
from users import *

def start(user, args):
    start_count = Users.get_data(user, "start_count")
    if start_count is None:
        start_count = 0
    start_count += 1
    Users.send_data(user, {"start_count": start_count})

    text = f"Привет, это бот Сёмга кор!\nОн пока ничего не умеет, но ты можешь порыбачить\nКстати, ты вызывал меня {start_count} раз"

    return {
        "text": text,
        "entities": [],
        "image": "somga_core.png",
        "buttons": {
            "Закинуть удочку": "/fish"
        }
    }

def debug(user, args):
    return "Эта команда доступна только админам!!!!!!! Если ты это читаешь, то ты - админ!!!!"

def restart(user, args):
    raise Exception("restarting")