import telebot
from datetime import datetime, timedelta

# Токен вашего бота
TOKEN = '6423641572:AAFx8dMJaahZBOgm8GRItFhkRlB3_vMa3c0'
bot = telebot.TeleBot(TOKEN)

# Администраторы
ADMIN_IDS = [1694921116, 6858042867]

# Словарь для хранения подписок пользователей
subscriptions = {}

# Команда /start
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    if user_id in subscriptions and subscriptions[user_id] > datetime.now():
        bot.send_message(user_id, "Добро пожаловать! Ваша подписка активна.")
        # Отправляем кнопки после активации подписки
        markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
        btn1 = telebot.types.KeyboardButton('📧 Email снос')
        btn2 = telebot.types.KeyboardButton('💬 Поддержка')
        markup.add(btn1, btn2)
        bot.send_message(user_id, "Выберите действие:", reply_markup=markup)
    else:
        bot.send_message(user_id, "Добро пожаловать! Ожидайте активации подписки от администратора.")

# Команда /activate для активации подписки
@bot.message_handler(commands=['activate'])
def activate_subscription(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "У вас нет прав для выполнения этой команды.")
        return

    try:
        # Команда должна быть в формате /activate <user_id> <days>
        _, user_id, days = message.text.split()
        user_id = int(user_id)
        days = int(days)

        # Устанавливаем срок подписки
        subscriptions[user_id] = datetime.now() + timedelta(days=days)
        bot.send_message(user_id, f"Поздравляем с приобретением подписки на {days} дн.\nВаша подписка активна до {subscriptions[user_id].strftime('%d.%m.%Y %H:%M')}")
        bot.send_message(message.chat.id, "Подписка успешно активирована!")

    except ValueError:
        bot.reply_to(message, "Неправильный формат команды. Используйте: /activate <user_id> <days>")

# Обработчик кнопок
@bot.message_handler(func=lambda message: message.text in ['📧 Email снос', '💬 Поддержка'])
def handle_buttons(message):
    if message.text == '📧 Email снос':
        bot.send_message(message.chat.id, "Введите тему жалобы:")
        bot.register_next_step_handler(message, get_complaint_topic)
    elif message.text == '💬 Поддержка':
        bot.send_message(message.chat.id, "Если есть вопросы, напишите сюда: @AReCToVaN_ZA_NACIONALIZM")

# Получаем тему жалобы
def get_complaint_topic(message):
    topic = message.text
    bot.send_message(message.chat.id, "Опишите проблему:")
    bot.register_next_step_handler(message, lambda m: get_complaint_text(m, topic))

# Получаем текст жалобы
def get_complaint_text(message, topic):
    complaint_text = message.text
    bot.send_message(message.chat.id, "Сколько запросов отправить?")
    bot.register_next_step_handler(message, lambda m: send_complaints(m, topic, complaint_text))

# Имитация отправки жалоб
def send_complaints(message, topic, complaint_text):
    try:
        num_requests = int(message.text)
        for _ in range(num_requests):
            # Имитация отправки запроса
            bot.send_message(message.chat.id, "Жалобы успешно отправлены!")
        bot.send_message(message.chat.id, f"Отправлено {num_requests} жалоб на тему: {topic}")
    except ValueError:
        bot.reply_to(message, "Введите число для количества запросов.")

# Запуск бота
bot.polling(none_stop=True)
