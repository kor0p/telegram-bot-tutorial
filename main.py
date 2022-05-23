from telebot import TeleBot, types

from config import BOT_TOKEN

bot = TeleBot(BOT_TOKEN)


users = {}


@bot.message_handler(commands=['start'])
def start_command(msg: types.Message):
    bot.send_message(msg.chat.id, 'Введи своє ім\'я:')
    bot.register_next_step_handler(msg, get_user_name)


def get_user_name(msg: types.Message):
    name = msg.text
    users[msg.from_user.id] = {'name': name}
    bot.send_message(msg.chat.id, f'Отже, {name}, скільки тобі років?')
    bot.register_next_step_handler(msg, get_user_age)


def get_user_age(msg: types.Message):
    age = msg.text
    try:
        age = int(age)
    except ValueError:
        bot.send_message(msg.chat.id, 'Введи число!')
        bot.register_next_step_handler(msg, get_user_age)
        return

    user = users[msg.from_user.id]
    user['age'] = age

    bot.send_message(msg.chat.id, f'Чудово, {user["name"]}! Тепер введи свою стать (Ч або Ж):')
    bot.register_next_step_handler(msg, get_user_gender)


def get_user_gender(msg: types.Message):
    gender = msg.text

    if gender not in ('Ч', 'Ж'):
        bot.send_message(msg.chat.id, 'Щось не пішло не так...\nОбери Ч або Ж:')
        bot.register_next_step_handler(msg, get_user_gender)
        return

    user = users[msg.from_user.id]
    user['gender'] = gender

    bot.send_message(
        msg.chat.id,
        f'Ура!\nТвоє ім\'я: {user["name"]}\nТвій вік: {user["age"]}\nТвоя стать: {user["gender"]}',
    )
