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
        "image": "somga_core.png",
        "buttons": {
            "Закинуть удочку": "/fish"
        }
    }

def debug(user, args):
    return "Нет пути, ты задал вот такие аргументы: " + str(args)

def restart(user, args):
    raise Exception("restarting")

def wipe(user, args):
    if not "да" in args:
        return "Вы точно хотите удалить все данные о пользователях? Напишите 'да' после команды чтобы подтвердить"
    elif not "точно-точно" in args:
        return "Вы уверены в этом? Напишите 'точно-точно' после команды чтобы подтвердить"

    Users.delete_all()
    
    return "Все данные о пользователях удалены"