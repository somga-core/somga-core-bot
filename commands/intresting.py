from users import *
from wordleanswer import getAnswer
import requests
import datetime

def sex(user, args):
    wordle_url = f"https://www.nytimes.com/svc/wordle/v2/{datetime.date.today().strftime('%Y-%m-%d')}.json"
    wordle_answer = requests.get(wordle_url).json()["solution"]

    if not wordle_answer in args:
        return "Вот это ты шалунишка!\n\nПеред тем как увидеть действие команды /sex, введи после команды ответ на сегодняшний wordle (Например: /sex unity)"
    
    Users.send_data(user, {"sex_counter": Users.get_data(user, "sex_counter", 0) + 1})
    
    return {
        "text": "Ага, попался! На жуков дрочишь!\n\nТы занесен в базу данных смотревших жучье порно. Чтобы посмотреть её, введи команду /sex_top",
        "image": "zuche_onrop.jpg"
    }

def sex_top(user, args):
    if not Users.get_data(user, "sex_password") in args:
        return "Ты не признанный сексолог. Таким смотреть /sex_top нельзя\n\nПожалуйся, зарегистрируй себя как сексолог зарегистрируясь по команде: /sex_register password. Вместо password поставь свой пароль\n\n Потом, чтобы посмотреть топ, введи: /sex_top password. Вместо password опять введи свой пароль"

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

def sex_register(user, args):
    if len(args) == 0:
        return "Ты не ввёл свой пароль. Введи: /sex_register password. Замени password на свой пароль"
    
    if not Users.get_data(user, "sex_password") is None:
        return "Прости, но ты уже регистрировался как сексолог\n\nПароль поменять нельзя\n\nВообще никак"

    Users.send_data(user, {"sex_password": args[0]})

    return "Поздравляю, теперь ты признанный сексолог!"