import telebot
from config import *
from extensions import *
from telebot import types

conv_buttons = types.ReplyKeyboardMarkup(one_time_keyboard = True)
buttons = []
for but in currencies.keys():
    buttons.append(types.KeyboardButton(but.capitalize()))
conv_buttons.add(*buttons)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Чтобы узнать курс валют, введите команду /convert\nУзнать доступные валюты: /values'
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in currencies.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(commands=['convert'])
def convert(message: telebot.types.Message):
    text = 'Выберите Валюту: '
    bot.send_message(message.chat.id, text, reply_markup = conv_buttons)
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip()
    text = 'В какую конвертировать: '
    bot.send_message(message.chat.id, text, reply_markup = conv_buttons)
    bot.register_next_step_handler(message, quote_handler, base)

def quote_handler(message: telebot.types.Message, base):
    quote = message.text.strip()
    text = 'Количество валюты: '
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, quote)

def amount_handler(message: telebot.types.Message, base, quote):
    amount = message.text.strip()
    try:
        new_price = Convertor.get_price(base, quote, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f'Ошибка конвертации: \n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} : {new_price}'
        bot.send_message(message.chat.id, text)



bot.polling()

