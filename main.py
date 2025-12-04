import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from dotenv import load_dotenv
import os

load_dotenv()

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
ADMIN = int(os.getenv('ADMIN_ID'))
SELL_RATE = float(os.getenv('SELL_RATE', '3.85'))
BUY_RATE = float(os.getenv('BUY_RATE', '3.70'))

# Главное меню как BestChange
@bot.message_handler(commands=['start'])
def start(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add("💚 Купить USDT", "🔴 Продать USDT")
    markup.add("📊 Курс", "⭐ Отзывыви", "☎ Контакт")
    
    bot.send_message(message.chat.id, f"""
🔥 <b>Обмен USDT в Ашхабаде 24/7</b>

💚 <b>Покупка USDT</b> — {BUY_RATE} TMT
🔴 <b>Продажа USDT</b> — {SELL_RATE} TMT

Способы оплаты:
• Наличные Ашхабад / Туркменбаши
• Halkbank
• Kaspi Gold
• Деньги Mail.ru

<b>Сделок сегодня: 27 | Отзывов: 142</b>
    """, reply_markup=markup, parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == '💚 Купить USDT')
def buy(message):
    msg = bot.send_message(message.chat.id, "Сколько USDT хотите купить?\nМинимально 50 USDT")
    bot.register_next_step_handler(msg, process_buy)

@bot.message_handler(func=lambda m: m.text == '🔴 Продать USDT')
def sell(message):
    msg = bot.send_message(message.chat.id, "Сколько USDT хотите продать?\nМинимально 50 USDT")
    bot.register_next_step_handler(msg, process_sell)

def process_buy(message):
    try:
        amount = float(message.text)
        total = round(amount * SELL_RATE, 2)
        bot.send_message(ADMIN, f"🟢 КУПИТЬ USDT\nСумма: {amount} USDT\nК получению: {total} TMT\nОт @{message.from_user.username or message.from_user.id}")
        bot.send_message(message.chat.id, f"✅ Заявка принята!\n{amount} USDT = {total} TMT\nСкоро свяжусь в личку 😉")
    except:
        bot.send_message(message.chat.id, "❌ Пиши только цифры")

def process_sell(message):
    try:
        amount = float(message.text)
        total = round(amount * BUY_RATE, 2)
        bot.send_message(ADMIN, f"🔴 ПРОДАТЬ USDT\nСумма: {amount} USDT\nК выдаче: {total} TMT\nОт @{message.from_user.username or message.from_user.id}")
        bot.send_message(message.chat.id, f"✅ Заявка принята!\n{amount} USDT = {total} TMT\nЖди связи в личке 🔥")
    except:
        bot.send_message(message.chat.id, "❌ Пиши только цифры")

@bot.message_handler(func=lambda m: m.text == '📊 Курс')
def rate(message):
    bot.send_message(message.chat.id, f"💱 <b>Текущий курс</b>\n\n💚 Покупаю USDT — {BUY_RATE} TMT\n🔴 Продаю USDT — {SELL_RATE} TMT\n\nОбновляется каждые 5 минут", parse_mode='HTML')

@bot.message_handler(func=lambda m: m.text == '⭐ Отзывы')
def reviews(message):
    bot.send_message(message.chat.id, "⭐ <b>Последние отзывы</b>:\n\n✅ «Быстро, 500$ за 10 мин, рекомендую»\n✅ «Всё чётко, налик в ТЦ»\n✅ «Третий раз меняюсь, топ!»\n\nОставь свой отзыв после сделки 😎", parse_mode='HTML')

bot.infinity_polling()
