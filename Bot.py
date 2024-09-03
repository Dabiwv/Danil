import telebot
from telebot import types

# Замените 'YOUR_BOT_TOKEN' на ваш токен бота
API_TOKEN = '7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs'
bot = telebot.TeleBot(API_TOKEN)

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создание клавиатуры
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton('Связь с админом')
    btn2 = types.KeyboardButton('Услуги')
    btn3 = types.KeyboardButton('Сообщение')
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(message.chat.id, "Привет! Пожалуйста, пройдите текстовую капчу. Введите: 'проверка'", reply_markup=markup)

# Функция для обработки текстового сообщения
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text.lower() == 'проверка':
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        btn1 = types.InlineKeyboardButton('Манул от Sweet Roxie: Анонимность + VPN - 330 руб', callback_data='info_1')
        btn2 = types.InlineKeyboardButton('Софты для Termux/Linux (12 штук) - 660 руб', callback_data='info_2')
        btn3 = types.InlineKeyboardButton('Обучение OSINT Framework - 250 руб', callback_data='info_3')
        
        markup.add(btn1, btn2, btn3)
        
        bot.send_message(message.chat.id, "Проверка на человека удалась 🪄, для дальнейшего действия выберите раздел:", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Пожалуйста, пройдите текстовую капчу, введя: 'проверка'")

# Функция для обработки нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'info_1':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")
    elif call.data == 'info_2':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")
    elif call.data == 'info_3':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")

# Запуск бота
bot.polling(none_stop=True)дл
