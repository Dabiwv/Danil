import telebot
from telebot import types

# Замените 'YOUR_BOT_API_TOKEN' на ваш токен от BotFather
TOKEN = '7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs'
bot = telebot.TeleBot(TOKEN)

# Функции для создания кнопок
def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Услуги")
    item2 = types.KeyboardButton("Связь с админом")
    markup.add(item1, item2)
    return markup

def services_buttons():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Анонимность в интернете + VPN - 330 руб", callback_data='service_1')
    button2 = types.InlineKeyboardButton("Софты для Termux/Linux (12 штук) - 660 руб", callback_data='service_2')
    button3 = types.InlineKeyboardButton("Обучение OSINT Framework - 250 руб", callback_data='service_3')
    markup.add(button1, button2, button3)
    return markup

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Пройдите текстовую капчу для подтверждения.", reply_markup=main_menu())

# Обработка нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == "Услуги":
        bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=services_buttons())
    elif message.text == "Связь с админом":
        bot.send_message(message.chat.id, "Напишите пожалуйста сюда для дальнейших действий @doksformoney")

# Обработка нажатий на инлайн кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'service_1' or call.data == 'service_2' or call.data == 'service_3':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир, после оплаты надо связаться с автором данного бота @doksformoney для дальнейших переговоров")

# Запуск бота
bot.polling()
