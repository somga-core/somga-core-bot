import telebot
from settings import *
from commands_handle import *
import time
from logs import *

class Bot(telebot.TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.command_handler()
        Logs.print_log("i", "Bot init complete")

    def command_handler(self):
        for command in CommandsHandle.commands_list:
            CommandsHandle.create_command_handler(command, self)
        CommandsHandle.create_inline_callback_handler(self)

        Logs.print_log("i", "Commands loaded")

def start(TOKEN):
    bot_object = Bot(TOKEN)

    while True:
        try:
            bot_object.polling(none_stop=True)
        except Exception as error:
            Logs.print_log("e", f"An error occured: {error}")
            Logs.print_log("i", f"Waiting 5 seconds and restarting")
            time.sleep(5)
            break