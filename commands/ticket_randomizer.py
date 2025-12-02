from users import *
from random import randint

def ticket(user, args):
    text = f'''Билет куплен успешно.
ООО "Вест Лайн"
🚏 {randint(1, 99)}
🚌 {chr(randint(1072, 1103))}{chr(randint(1072, 1103))}{randint(100, 999)}39
🪙 Тариф: Полный 38,00 ₽
🎫 Билет № {randint(1000000000, 9999999999)}
🕑 Действует всегда и везде'''

    return text