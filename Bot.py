import telebot
from telebot import types

# Замените 'YOUR_BOT_API_TOKEN' на ваш токен от BotFather
TOKEN = '7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs'
bot = telebot.TeleBot(TOKEN)

# Создание кнопок, которые будут под клавиатурой
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Услуги")
    item2 = types.KeyboardButton("Связь с админом")
    markup.add(item1, item2)
    return markup

# Функции для создания кнопок с услугами
def services_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    service1 = types.KeyboardButton("Анонимность в интернете + VPN - 330 руб")
    service2 = types.KeyboardButton("Софты для Termux/Linux (12 штук) - 660 руб")
    service3 = types.KeyboardButton("Обучение OSINT Framework - 250 руб")
    markup.add(service1, service2, service3)
    return markup

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Пройдите текстовую капчу для подтверждения.", reply_markup=main_menu())

# Обработка сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Услуги":
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=services_buttons())
    elif message.text == "Связь с админом":
        bot.send_message(message.chat.id, "Напишите пожалуйста сюда для дальнейших действий @doksformoney")
    elif "Анонимность" in message.text or "Софты" in message.text or "Обучение" in message.text:
        bot.send_message(message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир, после оплаты надо связаться с автором данного бота @doksformoney для дальнейших переговоров")

# Запуск бота
bot.polling()
