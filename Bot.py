import time
from datetime import datetime, timedelta
from telebot import TeleBot, types

# Инициализация бота с токеном
TOKEN = '6423641572:AAFx8dMJaahZBOgm8GRItFhkRlB3_vMa3c0'
bot = TeleBot(TOKEN)

# ID администраторов
ADMINS = [1694921116, 6858042867]

# Словарь для хранения подписок пользователей
user_subscriptions = {}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    if user_id in user_subscriptions:
        bot.send_message(user_id, "Добро пожаловать! Ваша подписка активна.")
        show_buttons(user_id)
    else:
        bot.send_message(user_id, "Добро пожаловать! Ожидайте активации подписки от администратора.")

# Функция для отображения кнопок после активации
def show_buttons(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    email_snoss = types.KeyboardButton("📧 Email снос")
    support = types.KeyboardButton("Поддержка")
    markup.add(email_snoss, support)
    bot.send_message(user_id, "Выберите действие:", reply_markup=markup)

# Обработчик команды /activate для активации подписки
@bot.message_handler(commands=['activate'])
def activate_subscription(message):
    if message.from_user.id in ADMINS:
        try:
            # Получаем аргументы команды
            args = message.text.split()
            if len(args) == 3:
                user_id = int(args[1])
                days = int(args[2])
                expiration_date = datetime.now() + timedelta(days=days)
                user_subscriptions[user_id] = expiration_date
                bot.send_message(user_id, f"Поздравляем! Ваша подписка активирована до {expiration_date.strftime('%d.%m.%Y %H:%M')}.")
                show_buttons(user_id)
            else:
                bot.send_message(message.chat.id, "Отправьте ID пользователя и количество дней подписки в формате: /activate <user_id> <days>")
        except ValueError:
            bot.send_message(message.chat.id, "Неверный формат. Используйте: /activate <user_id> <days>")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Обработчик кнопки "📧 Email снос"
@bot.message_handler(func=lambda message: message.text == "📧 Email снос")
def email_snoss(message):
    user_id = message.from_user.id
    if user_id in user_subscriptions and user_subscriptions[user_id] > datetime.now():
        msg = bot.send_message(user_id, "Введите тему:")
        bot.register_next_step_handler(msg, ask_complaint_text)
    else:
        bot.send_message(user_id, "У вас нет активной подписки. Ожидайте активации от администратора.")

def ask_complaint_text(message):
    user_id = message.from_user.id
    if user_id in user_subscriptions and user_subscriptions[user_id] > datetime.now():
        msg = bot.send_message(user_id, "Опишите проблему:")
        bot.register_next_step_handler(msg, ask_complaint_amount)
    else:
        bot.send_message(user_id, "У вас нет активной подписки. Ожидайте активации от администратора.")

def ask_complaint_amount(message):
    user_id = message.from_user.id
    if user_id in user_subscriptions and user_subscriptions[user_id] > datetime.now():
        msg = bot.send_message(user_id, "Сколько запросов отправить?")
        bot.register_next_step_handler(msg, send_complaints)
    else:
        bot.send_message(user_id, "У вас нет активной подписки. Ожидайте активации от администратора.")

def send_complaints(message):
    try:
        complaint_count = int(message.text)
        for _ in range(complaint_count):
            time.sleep(4)  # Имитация антифлуда
            bot.send_message(message.chat.id, "Жалобы успешно отправлены!")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

# Обработчик кнопки "Поддержка"
@bot.message_handler(func=lambda message: message.text == "Поддержка")
def support(message):
    bot.send_message(message.chat.id, "Если есть вопросы, пишите сюда: @AReCToVaN_ZA_NACIONALIZM")

# Запуск бота
bot.polling(none_stop=True)
