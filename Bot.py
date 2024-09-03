import telebot
from telebot import types

# Замените 'YOUR_BOT_API_TOKEN' на ваш токен от BotFather
TOKEN = '7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs'
bot = telebot.TeleBot(TOKEN)

# Создание кнопок
def start_buttons():
    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    item1 = types.KeyboardButton("Старт")
    markup.add(item1)
    return markup

def admin_buttons():
    markup = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Связь с админом", callback_data='contact_admin')
    markup.add(button)
    return markup

def services_buttons():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Мануал от Sweet Roxie: Анонимность в интернете + бесплатный слитый VPN - 330 руб", callback_data='service_1')
    button2 = types.InlineKeyboardButton("Софты для Termux/Linux (в наличии 12 штук) - 660 руб", callback_data='service_2')
    button3 = types.InlineKeyboardButton("Обучение OSINT Framework - 250 руб", callback_data='service_3')
    markup.add(button1, button2, button3)
    return markup

# Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = start_buttons()
    bot.send_message(message.chat.id, "Пройдите текстовую капчу:", reply_markup=markup)

# Обработка текстовой капчи
@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start(message):
    # Здесь вы можете добавить логику для проверки капчи
    # Если проверка прошла успешно
    bot.send_message(message.chat.id, "Проверка на человека удалась 🪄, для дальнейшего действия, выберите раздел", reply_markup=services_buttons())
    # Если проверка не удалась
    # bot.send_message(message.chat.id, "Проверка не удалась. Пожалуйста, попробуйте снова.")

# Обработка нажатий на кнопки инлайн
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'contact_admin':
        bot.answer_callback_query(call.id, "Напишите пожалуйста сюда для дальнейших действий @doksformoney")
    elif call.data in ['service_1', 'service_2', 'service_3']:
        bot.answer_callback_query(call.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир, после оплаты надо связаться с автором данного бота для дальнейших переговоров")

# Запуск бота
bot.polling()
