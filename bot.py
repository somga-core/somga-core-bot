import telebot
from settings import *
from commands_handle import *
import time
from datetime import datetime

class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.command_handler()
        print(f"[i] ({datetime.now().strftime(TIME_FORMAT)}) Bot init complete")

    def command_handler(self):
        for command in CommandsHandle.commands_list:
            CommandsHandle.create_command_handler(command, self)
        CommandsHandle.create_inline_callback_handler(self)

        self.message_handler(commands=["/restart"])(self.restart)

        print(f"[i] ({datetime.now().strftime(TIME_FORMAT)}) Commands loaded")

    def restart(self, message):
        if not message.from_user.id in ADMIN_USERS:
            return 0
        self.stop_bot()

def start(TOKEN):
    bot_object = Bot(TOKEN)

    while True:
        try:
            bot_object.polling(none_stop=True)
            break
        except Exception as e:
            print(f"[e] ({datetime.now().strftime(TIME_FORMAT)}) Bot run error occured:", e)
            time.sleep(5)
            continue