from users import *
from wordleanswer import getAnswer
import requests
import datetime

def sex(user, args):
    wordle_url = f"https://www.nytimes.com/svc/wordle/v2/{datetime.date.today().strftime('%Y-%m-%d')}.json"
    wordle_answer = requests.get(wordle_url).json()["solution"]

    if not wordle_answer in args:
        return "Вот это ты шалунишка!\n\nПеред тем как увидеть действие команды /sex, введи после команды ответ на сегодняшний wordle (Например: '/sex unity')"
    
    Users.send_data(user, {"sex_counter": Users.get_data(user, "sex_counter", 0) + 1})
    
    return {
        "text": "Ага, попался! На жуков дрочишь!\n\nТы занесен в базу данных смотревших жучье порно. Чтобы посмотреть её, введи команду /sex_top",
        "image": "somga_core.png"
    }

def sex_top(user, args):
    if not "21" in args:
        return

    users_sex = Users.get_data_from_all_users("sex_counter", 0)
    users_sex = dict(sorted(users_sex.items(), reverse=1, key=lambda x: x[1]))

    text = "Вот количество раз, которое пользователи смотрели жучье порно:\n"

    for sex_id in range(len(users_sex)):
        first_name = Users.get_data(list(users_sex.keys())[sex_id], 'first_name')
        last_name = Users.get_data(list(users_sex.keys())[sex_id], 'last_name')
        username = Users.get_data(list(users_sex.keys())[sex_id], 'username')
        text += f"{sex_id + 1}. {first_name} {last_name + ' ' if not last_name is None else ''}{'(@' + username + ') ' if username is not None else ''}- {list(users_sex.values())[sex_id]}\n"

    return {
        "text": text
    } 