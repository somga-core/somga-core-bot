from users import *
from random import *

def ticket(user, args):
    text = f'''Билет куплен успешно.
ООО "Вест Лайн"
🚏 {random.randint(1, 99)}
🚌 {chr(random.randint(1072, 1103))}{chr(random.randint(1072, 1103))}{random.randint(100, 999)}39
🪙 Тариф: Полный 38,00 ₽
🎫 Билет № f{random.randint(1000000000, 9999999999)}
🕑 Действует всегда и везде'''

    return text