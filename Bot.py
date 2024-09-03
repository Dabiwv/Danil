import telebot
from telebot import types

bot = telebot.TeleBot("7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs")

# Основное меню
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("📚 Обучение")
    btn2 = types.KeyboardButton("💼 Услуги")
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, "Выберите раздел:", reply_markup=markup)

# Обработка выбора
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "📚 Обучение":
        send_payment_info(message)
    elif message.text == "💼 Услуги":
        send_payment_info(message)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, выберите один из разделов.")

# Отправка информации об оплате
def send_payment_info(message):
    bot.send_message(message.chat.id, "Оплачивай через крипто бота, на телеграм кошелек, на данный адрес UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL")

bot.polling()
