import time
import random
from telebot import TeleBot, types

# Токен бота и айди админов
TOKEN = '6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c'
ADMIN_IDS = [1694921116, 6858042867]
bot = TeleBot(TOKEN)

# Список случайных фактов о хакерстве
random_facts = [
    "Первый компьютерный вирус был создан в 1986 году.",
    "White Hat хакеры помогают компаниям находить уязвимости.",
    "SQL-инъекции — один из самых распространенных методов взлома.",
    "Первый DDoS-атакующий использовал ботнет из 500 устройств.",
    "Wi-Fi сети без пароля могут быть взломаны за несколько минут.",
    "Phishing — популярный метод кражи личных данных.",
    "С помощью keylogger'ов хакеры крадут пароли с клавиатур.",
    "Tor позволяет анонимно посещать сайты в даркнете.",
    "Zero-day уязвимости могут быть проданы за миллионы.",
    "Deepfake может быть использован для обмана в интернете."
]

# Ограничение по времени для антифлуда
last_message_time = {}

# Функция антифлуда
def anti_flood(user_id):
    current_time = time.time()
    if user_id in last_message_time:
        if current_time - last_message_time[user_id] < 4:
            return False
    last_message_time[user_id] = current_time
    return True

# Команда старта
@bot.message_handler(commands=['start'])
def start(message):
    if anti_flood(message.from_user.id):
        if message.from_user.id in ADMIN_IDS:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("🎲 Случайный факт"), types.KeyboardButton("📧 Email снос"))
            bot.send_message(message.chat.id, "Добро пожаловать, админ!", reply_markup=markup)
        else:
            bot.send_message(message.chat.id, "Добро пожаловать! Ожидайте активации подписки от администратора.")
    else:
        bot.send_message(message.chat.id, "Подождите несколько секунд перед следующим сообщением.")

# Команда активации подписки
@bot.message_handler(commands=['activate'])
def activate(message):
    if message.from_user.id in ADMIN_IDS:
        try:
            _, user_id, days = message.text.split()
            user_id = int(user_id)
            days = int(days)
            bot.send_message(user_id, f"Поздравляем с приобретением подписки на {days} дней!")
            bot.send_message(user_id, "Ваша подписка активирована.")
        except ValueError:
            bot.send_message(message.chat.id, "Отправьте ID пользователя и количество дней подписки в формате: /activate <user_id> <days>")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Обработчик кнопки "🎲 Случайный факт"
@bot.message_handler(func=lambda message: message.text == "🎲 Случайный факт")
def random_fact(message):
    if anti_flood(message.from_user.id):
        fact = random.choice(random_facts)
        bot.send_message(message.chat.id, fact)
    else:
        bot.send_message(message.chat.id, "Подождите несколько секунд перед следующим сообщением.")

# Обработчик кнопки "📧 Email снос"
@bot.message_handler(func=lambda message: message.text == "📧 Email снос")
def email_snos(message):
    if anti_flood(message.from_user.id):
        bot.send_message(message.chat.id, "Введите тему жалобы:")
    else:
        bot.send_message(message.chat.id, "Подождите несколько секунд перед следующим сообщением.")

# Запуск бота
bot.polling(none_stop=True)
