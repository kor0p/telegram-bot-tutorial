from functools import wraps

import psycopg2
from psycopg2.extensions import cursor

from telebot import TeleBot, types

from config import BOT_TOKEN, DB_URL

bot = TeleBot(BOT_TOKEN, threaded=False)
connection = psycopg2.connect(DB_URL)


def with_cursor(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        with connection:
            with connection.cursor() as cr:
                return fn(cr, *args, **kwargs)

    return wrapper


@bot.message_handler(commands=['start'])
@with_cursor
def start_command(cr: cursor, msg: types.Message):
    id = msg.from_user.id
    name = msg.from_user.full_name

    cr.execute(
        'SELECT 1 FROM users WHERE id = %s',
        (id,),
    )
    if cr.fetchone():
        send_info(cr, msg)
        return

    cr.execute(
        'INSERT INTO users (id, name) VALUES (%s, %s)',
        (id, name),
    )

    bot.send_message(msg.chat.id, f'Отже, {name}, скільки тобі років?')
    bot.register_next_step_handler(msg, get_user_age)


@with_cursor
def get_user_age(cr: cursor, msg: types.Message):
    id = msg.from_user.id
    age = msg.text
    try:
        age = int(age)
    except ValueError:
        bot.send_message(msg.chat.id, 'Введи число!')
        bot.register_next_step_handler(msg, get_user_age)
        return

    cr.execute(
        'SELECT name FROM users WHERE id = %s',
        (id,),
    )
    name, = cr.fetchone()

    cr.execute(
        'UPDATE users SET age = %s WHERE id = %s',
        (age, id),
    )

    bot.send_message(msg.chat.id, f'Чудово, {name}! Тепер введи свою стать (Ч або Ж):')
    bot.register_next_step_handler(msg, get_user_gender)


@with_cursor
def get_user_gender(cr: cursor, msg: types.Message):
    gender = msg.text

    if gender not in ('Ч', 'Ж'):
        bot.send_message(msg.chat.id, 'Щось не пішло не так...\nОбери Ч або Ж:')
        bot.register_next_step_handler(msg, get_user_gender)
        return

    cr.execute(
        'UPDATE users SET gender = %s WHERE id = %s',
        (gender, msg.from_user.id),
    )

    send_info(cr, msg)


def send_info(cr: cursor, msg: types.Message):
    cr.execute(
        'SELECT name, age, gender FROM users WHERE id = %s',
        (msg.from_user.id,),
    )
    name, age, gender = cr.fetchone()

    bot.send_message(
        msg.chat.id,
        f'Ура!\nТвоє ім\'я: {name}\nТвій вік: {age}\nТвоя стать: {gender}',
    )
