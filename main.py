import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
ADMIN = int(os.getenv('ADMIN_ID'))
BUY_RATE = float(os.getenv('BUY_RATE'))
SELL_RATE = float(os.getenv('SELL_RATE'))
MIN = int(os.getenv('MIN_AMOUNT'))

@bot.message_handler(commands=['start'])
def start(message):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(InlineKeyboardButton("Купить USDT", callback_data="buy"),
               InlineKeyboardButton("Продать USDT", callback_data="sell"))
    bot.send_message(message.chat.id, "Салам, брат! Выбери действие:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.data == "buy":
        bot.send_message(call.message.chat.id, f"Сколько USDT купить? (мин {MIN})\nКурс {SELL_RATE} TMT за 1 USDT")
        bot.register_next_step_handler(call.message, buy_process)
    elif call.data == "sell":
        bot.send_message(call.message.chat.id, f"Сколько USDT продать? (мин {MIN})\nКурс {BUY_RATE} TMT за 1 USDT")
        bot.register_next_step_handler(call.message, sell_process)

def buy_process(message):
    try:
        amount = float(message.text)
        total = round(amount * SELL_RATE, 2)
        bot.send_message(ADMIN, f"🟢 КУПИТЬ\n{amount} USDT = {total} TMT\nОт @{message.from_user.username or 'без юзера'}")
        bot.send_message(message.chat.id, "Заявка принята, скоро свяжусь!")
    except:
        bot.send_message(message.chat.id, "Пиши только цифры, брат")

def sell_process(message):
    try:
        amount = float(message.text)
        total = round(amount * BUY_RATE, 2)
        bot.send_message(ADMIN, f"🔴 ПРОДАТЬ\n{amount} USDT = {total} TMT\nОт @{message.from_user.username or 'без юзера'}")
        bot.send_message(message.chat.id, "Заявка принята, жди!")
    except:
        bot.send_message(message.chat.id, "Пиши только цифры, брат")

bot.infinity_polling()
