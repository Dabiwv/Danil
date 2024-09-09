import time
from datetime import datetime, timedelta
from telebot import TeleBot, types

# Токен бота
TOKEN = '6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c'

# Администраторы (твои и друга ID)
ADMIN_IDS = [1694921116, 6858042867]

# Создаем объект бота
bot = TeleBot(TOKEN)

# Словарь для хранения активных пользователей и сроков их подписок
active_users = {}

# Команда /start для всех пользователей
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    
    if user_id in active_users and active_users[user_id] > datetime.now():
        # Если пользователь активен, показываем кнопки
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("📧 Email снос"), types.KeyboardButton("Поддержка"))
        bot.send_message(message.chat.id, "Добро пожаловать! Ваша подписка активна.", reply_markup=markup)
    else:
        # Если подписка не активна
        bot.send_message(message.chat.id, "Добро пожаловать! Ожидайте активации подписки от администратора.")

# Команда активации подписки (только для админов)
@bot.message_handler(commands=['activate'])
def activate_subscription(message):
    if message.from_user.id in ADMIN_IDS:
        try:
            # Парсим команду /activate <user_id> <days>
            _, user_id, days = message.text.split()
            user_id = int(user_id)
            days = int(days)

            # Устанавливаем срок подписки
            active_users[user_id] = datetime.now() + timedelta(days=days)
            
            bot.send_message(message.chat.id, f"Подписка активирована для пользователя {user_id} на {days} дней.")
            bot.send_message(user_id, f"Ваша подписка активирована на {days} дней.")
        except ValueError:
            bot.send_message(message.chat.id, "Ошибка! Используйте команду в формате: /activate <user_id> <days>")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для использования этой команды.")

# Обработка нажатий на кнопки
@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.from_user.id in active_users and active_users[message.from_user.id] > datetime.now():
        if message.text == "📧 Email снос":
            bot.send_message(message.chat.id, "Введите тему жалобы:")
        elif message.text == "Поддержка":
            bot.send_message(message.chat.id, "Если у вас есть вопросы, пишите сюда: @AReCToVaN_ZA_NACIONALIZM")
    else:
        bot.send_message(message.chat.id, "Ваша подписка не активна. Ожидайте активации от администратора.")

# Запуск бота
bot.polling()
