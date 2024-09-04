import telebot
from telebot import types

# Вставьте ваш токен
TOKEN = "7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs"
bot = telebot.TeleBot(TOKEN)

# Функция для обработки команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создание клавиатуры
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn_kaspi = types.KeyboardButton('📩 Реквизиты Kaspi Gold')
    btn_halyk = types.KeyboardButton('📩 Реквизиты Halyk Bank')
    btn_admin = types.KeyboardButton('📞 Связь с админом')
    btn_services = types.KeyboardButton('💼 Услуга')
    
    markup.add(btn_kaspi, btn_halyk, btn_admin, btn_services)
    
    bot.send_message(message.chat.id, "Привет! Выберите нужную опцию ниже:", reply_markup=markup)

# Функция для обработки нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == '📩 Реквизиты Kaspi Gold':
        bot.send_message(message.chat.id, "📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n☎️ Номер: 4400 4302 6934 6638\n👨‍💻 Имя - Данил Г.\n💬 Комментарий: НЕ ПИСАТЬ!!!")
    elif message.text == '📩 Реквизиты Halyk Bank':
        bot.send_message(message.chat.id, "📩 Отправьте деньги по реквизитам на Halyk Bank 🔥:\n☎️ Номер: 4405 6398 0709 6001\n👨‍💻 Имя - Данил Г.\n💬 Комментарий: НЕ ПИСАТЬ!!!")
    elif message.text == '📞 Связь с админом':
        bot.send_message(message.chat.id, "Пожалуйста, по всем вопросам пишите сюда @B6lyat")
    elif message.text == '💼 Услуга':
        bot.send_message(message.chat.id, "💼 Деанон человека - 600 тг\n💼 Фото человека - 600 тг\n💼 Узнать номера родителей человека - 800 тг\n💼 Написать человеку угрозы - 800 тг")

# Запуск бота
bot.polling(none_stop=True)
