# Импорты
import telebot
from settings import *
from commands_handle import *

# Классы
class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.command_handler()
        print("[i] Bot init complete")

    def command_handler(self):
        for command in CommandsHandle.commands_list:
            CommandsHandle.create_command_handler(command, self)
        CommandsHandle.create_inline_callback_handler(self)
        print("[i] Command handler init complete")

def start(TOKEN):
    bot_object = Bot(TOKEN)

    bot_object.polling(none_stop=True)