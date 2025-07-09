from users import *
from random import randint

exp_spread = 3
rods = (100, 365, 700, 1500, 2000, 3000, 5000, 10000)
fish_parts = (
    (
        ("o", 5),
        ("v", 7),
        ("m", 15),
        ("n", 20),
        ("u", 25),
        ("_", 45),
    ),
    (
        ("||", 4),
        ("( )", 5),
        ("[ ]", 14),
        ("(:)", 19),
        ("[:]", 23),
        ("(;)", 28),
        ("[;]", 47),
    ),
    (
        ("W", 3),
        ("Y", 4),
        ("N", 10),
        ("U", 13),
        ("V", 21),
        ("M", 26),
        ("J", 50),
    )
)

def fish(user):
    exp = Users.get_data(user, "exp", 0)
    rod = Users.get_data(user, "rod", 0)
    fish_count = Users.get_data(user, "fish_count", 0)

    fish_part_ranges = [int((len(fish_part) / len(rods)) * rod) for fish_part in fish_parts]

    fish_part_index_choices = [randint(0, fish_part_range) for fish_part_range in fish_part_ranges]
    
    exp_choice = [randint(fish_parts[fish_part_index][fish_part_index_choices[fish_part_index]][1] - exp_spread, fish_parts[fish_part_index][fish_part_index_choices[fish_part_index]][1] + exp_spread) for fish_part_index in range(len(fish_parts))]
    
    fish_part_choice = [fish_parts[fish_part_index][fish_part_index_choices[fish_part_index]][0] for fish_part_index in range(len(fish_parts))]

    exp_sum = sum(exp_choice)

    Users.send_data(user, {"exp": exp + exp_sum})
    Users.send_data(user, {"fish_count": fish_count + 1})
    
    text = f"Вы поймали такую рыбу:\n\n" + "\n".join([f"{fish_part_choice[fish_part_index]} - {exp_choice[fish_part_index]} фантиков" for fish_part_index in range(len(fish_parts))]) + f"\n\nЗа которую в сумме заработали {exp_sum} фантиков\nТеперь у вас {exp + exp_sum} фантиков"
    
    return {
        "text": text,
        "entities": [],
        "buttons": {
            "Рыбачить ещё!": "/fish",
            "Статистика": "/stats"
        }
    }   

def stats(user):
    exp = Users.get_data(user, "exp", 0)
    rod = Users.get_data(user, "rod", 0)
    fish_count = Users.get_data(user, "fish_count", 0)
    buttons = {
        "Рыбачить дальше!": "/fish",
        "Посмотреть топ": "/top"
    }

    text = f"Вы поймали {fish_count} рыбов на {exp} фантиков\nВаша удочка сейчас на {rod+1} уровне\n\n"
    if rod >= len(rods) - 1:
        update_text = "Ваша удочка максимального уровня"
    else:
        update_text = f"Чтобы улучшить удочку, вам нужно {rods[rod]} фантиков"
        buttons["Улучшить удочку"] = "/upgrade"
    
    return {
        "text": text + update_text,
        "entities": [],
        "buttons": buttons
    }

def upgrade(user):
    exp = Users.get_data(user, "exp", 0)
    rod = Users.get_data(user, "rod", 0)

    if rod < len(rods) - 1:
        if exp >= rods[rod]:
            Users.send_data(user, {"exp": exp - rods[rod]})
            Users.send_data(user, {"rod": rod + 1})
            text = f"Вы улучшили удочку до {rod + 2} уровня, потратив {rods[rod]} фантиков\nТеперь у вас {exp - rods[rod]} фантиков"
        else:
            text = f"Для улучшения удочки вам не хватает {rods[rod] - exp} фантиков"
    else:
        text = "Ваша удочка уже улучшена до максимального уровня"
    
    return {
        "text": text,
        "entities": [],
        "buttons": {
            "Вернуться к рыбалке": "/fish"
        }
    }

def top(user):
    users_exp = Users.get_data_from_all_users("exp", 0)
    users_exp = dict(sorted(users_exp.items(), reverse=1, key=lambda x: x[1])[:10])

    text = "Топ участников по количеству фантиков:\n"

    for exp_id in range(len(users_exp)):
        first_name = Users.get_data(list(users_exp.keys())[exp_id], 'first_name')
        last_name = Users.get_data(list(users_exp.keys())[exp_id], 'last_name')
        username = Users.get_data(list(users_exp.keys())[exp_id], 'username')
        text += f"{exp_id + 1}. {first_name} {last_name + ' ' if not last_name is None else ''}{'(@' + username + ')' if username is not None else ''} - {list(users_exp.values())[exp_id]}\n"

    return {
        "text": text,
        "entities": [],
        "buttons": {
            "Продолжить рыбалку!": "/fish"
        }
    }