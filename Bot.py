import telebot
from telebot import types

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"
bot = telebot.TeleBot(TOKEN)

# Кнопки на клавиатуре
keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_email = types.KeyboardButton('📧 Email снос')
button_support = types.KeyboardButton('💬 Поддержка')
keyboard.add(button_email, button_support)

# Переменная для хранения данных пользователей
user_data = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Выберите действие:", reply_markup=keyboard)

# Обработка нажатия кнопки '📧 Email снос'
@bot.message_handler(func=lambda message: message.text == '📧 Email снос')
def email_snos(message):
    user_id = message.from_user.id
    user_data[user_id] = {}  # Инициализируем данные пользователя
    bot.send_message(message.chat.id, "Введите тему жалобы:")

# Обработка текста для жалобы
@bot.message_handler(func=lambda message: message.text not in ['📧 Email снос', '💬 Поддержка'])
def process_complaint(message):
    user_id = message.from_user.id

    if 'subject' not in user_data[user_id]:
        user_data[user_id]['subject'] = message.text
        bot.send_message(message.chat.id, "Теперь введите текст жалобы:")
    elif 'body' not in user_data[user_id]:
        user_data[user_id]['body'] = message.text
        bot.send_message(message.chat.id, "Сколько запросов отправить?")
    elif 'num_requests' not in user_data[user_id]:
        try:
            num_requests = int(message.text)
            user_data[user_id]['num_requests'] = num_requests
            bot.send_message(message.chat.id, f"Отправляю {num_requests} запросов...")
            
            # Имитация отправки жалоб
            for _ in range(num_requests):
                for _ in range(7):  # Сообщение выводится 7 раз
                    bot.send_message(message.chat.id, "Жалобы успешно отправлены!")
        except ValueError:
            bot.send_message(message.chat.id, "Пожалуйста, введите корректное количество запросов.")

# Обработка нажатия кнопки '💬 Поддержка'
@bot.message_handler(func=lambda message: message.text == '💬 Поддержка')
def support(message):
    bot.send_message(message.chat.id, "Напишите ваше обращение, и админ вам ответит.")

# Запуск бота
bot.polling(none_stop=True)
