import telebot
import json
from os.path import join
from settings import *
from users import *
from logs import *

class CommandsHandle:
    commands_list = {}
    admin_functions_list = []

    with open(COMMANDS_FILE) as f:
        raw_data = json.loads(f.read())

    for pack in raw_data:
        exec(f"import {COMMANDS_FOLDER.strip('/.')}.{pack}")
        for command in raw_data[pack]:
            commands_list[command] = eval(f"{COMMANDS_FOLDER.strip('/.')}.{pack}.{raw_data[pack][command]['function']}")
            if "admin" in raw_data[pack][command] and raw_data[pack][command]["admin"]:
                admin_functions_list.append(commands_list[command])

    Logs.print_log("i", "Commands handle init complete")

    @staticmethod
    def create_command_handler(command, bot):
        bot.message_handler(
            commands=[command.strip("/")]
        )(
            lambda message: CommandsHandle.template_command(
                str(message.from_user.id), CommandsHandle.commands_list[command], message.chat.id, message.text, bot
            )
        )

    @staticmethod
    def create_inline_callback_handler(bot):
        bot.callback_query_handler(func=lambda call: True)(lambda call: CommandsHandle.template_inline_callback(call, bot))

    @staticmethod
    def template_command(user, function, chat_id, message_text, bot):
        if function in CommandsHandle.admin_functions_list and not user in ADMIN_USERS:
            return 0

        names = [bot.get_chat(user).username, bot.get_chat(user).first_name, bot.get_chat(user).last_name]
        Users.send_data(user, {"username": names[0]})
        Users.send_data(user, {"first_name": names[1]})
        Users.send_data(user, {"last_name": names[2]})

        args = message_text.split(' ')[1:]

        sended_message = function(user, args)
        command = [i for i in CommandsHandle.commands_list if CommandsHandle.commands_list[i] == function][0]

        if type(sended_message) == type(""):
            bot.send_message(
                chat_id=chat_id,
                text=sended_message
            )
        else:
            if not "buttons" in sended_message:
                sended_message["buttons"] = {}

            if not "entities" in sended_message:
                sended_message["entities"] = []

            if "buttons" in sended_message:
                if "button_columns" in sended_message:
                    button_columns = sended_message["button_columns"]
                else:
                    button_columns = BUTTON_COLUMNS
                
                markup = telebot.types.InlineKeyboardMarkup(row_width=button_columns)

                buttons = sended_message["buttons"]
                buttons = [telebot.types.InlineKeyboardButton(i, callback_data=buttons[i]) for i in buttons]
                markup.add(*buttons)

            if "image" in sended_message:
                bot.send_photo(
                    chat_id=chat_id,
                    caption=sended_message["text"],
                    caption_entities=sended_message["entities"],
                    photo=open(join(IMAGES_FOLDER, sended_message['image']), "rb"),
                    reply_markup=markup
                )
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text=sended_message["text"],
                    entities=sended_message["entities"],
                    reply_markup=markup
                )

        Logs.print_log("c", f"{names[1]} {names[2]} (@{names[0]}) used {command}")

    @staticmethod
    def template_inline_callback(call, bot):
        try:
            if call.message:
                if call.data in CommandsHandle.commands_list:
                    function = CommandsHandle.commands_list[call.data]
                    CommandsHandle.template_command(str(call.from_user.id), function, call.message.chat.id, call.data, bot)

        except Exception as error:
            Logs.print_log("e", f"Inline callback error occured:  {error}")