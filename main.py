from telebot import TeleBot, types

bot = TeleBot("5324505475:AAFymjlbMzPWfMi1U1RCadv-W5lS2IwLdi8")


@bot.message_handler(content_types=['text'])
def all_text_messages(msg: types.Message):
    bot.send_message(
        msg.chat.id,
        f'Ось твій текст:\n{msg.text}',
    )


bot.infinity_polling()
