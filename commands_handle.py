import telebot
import json
from os.path import join
from settings import *
from users import *

class CommandsHandle:
    commands_list = {}
    buttons_list = {}

    with open(COMMANDS_FILE) as f:
        raw_data = json.loads(f.read())

    for pack in raw_data:
        exec(f"import {COMMANDS_FOLDER.strip('/.')}.{pack}")
        for command in raw_data[pack]:
            commands_list[command] = eval(f"{COMMANDS_FOLDER.strip('/.')}.{pack}.{raw_data[pack][command]['function']}")
            
    for pack in raw_data:
        for command in raw_data[pack]:
            for button in raw_data[pack][command]["buttons"]:
                buttons_list[button] = [commands_list[command], commands_list[raw_data[pack][command]["buttons"][button]]]

    print("[i] Commands handle init complete")

    @staticmethod
    def create_command_handler(command, bot):
        bot.message_handler(
            commands=[command.strip("/")]
        )(
            lambda message: CommandsHandle.template_command(
                str(message.from_user.id), CommandsHandle.commands_list[command], message, bot
            )
        )

    @staticmethod
    def create_inline_callback_handler(bot):
        bot.callback_query_handler(func=lambda call: True)(lambda call: CommandsHandle.template_inline_callback(call, bot))

    @staticmethod
    def template_command(user, function, message, bot):
        chat_id = message.chat.id

        names = [bot.get_chat(user).username, bot.get_chat(user).first_name, bot.get_chat(user).last_name]
        Users.send_data(user, {"username": names[0]})
        Users.send_data(user, {"first_name": names[1]})
        Users.send_data(user, {"last_name": names[2]})

        sended_message = function(user)
        command = [i for i in CommandsHandle.commands_list if CommandsHandle.commands_list[i] == function][0]

        # markup = telebot.types.ReplyKeyboardRemove(selective=False)
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        buttons = CommandsHandle.buttons_list
        buttons = [telebot.types.InlineKeyboardButton(i, callback_data=i) for i in buttons if buttons[i][0] == function]
        markup.add(*buttons)

        if type(sended_message) == type(""):
            bot.send_message(
                chat_id=chat_id,
                text=sended_message,
                reply_markup=markup
            )
        elif "image" in sended_message:
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

        print(f"[c] {names[1]} {names[2]} (@{names[0]}) used {command}")

    @staticmethod
    def template_inline_callback(call, bot):
        try:
            if call.message:
                if call.data in CommandsHandle.buttons_list:
                    function = CommandsHandle.buttons_list[call.data][1]
                    CommandsHandle.template_command(str(call.from_user.id), function, call.message, bot)

        except Exception as error:
            print("[e] Inline callback error occured: " + str(error))