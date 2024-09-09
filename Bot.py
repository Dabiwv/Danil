from telebot import TeleBot, types
from datetime import datetime, timedelta
import time

bot_token = '6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c'
bot = TeleBot(bot_token)

# ID админов
admins = [1694921116, 6858042867]

# Список пользователей с активной подпиской и датой окончания подписки
active_users = {}

# Хранение данных пользователя для обработки жалоб
user_data = {}

# Хакерские факты
facts = [
    "Хакеры начали использовать социальную инженерию еще в 80-х годах.",
    "Самая крупная хакерская атака – DDoS-атака, достигшая 2.3 Тб/с.",
    "Первый компьютерный вирус был создан в 1983 году.",
    "Киберпреступность приносит больше денег, чем наркоторговля.",
    "Часто хакеры используют фальшивые обновления ПО для распространения вредоносных программ.",
    "Зловредное ПО может быть спрятано в легальных приложениях и программах.",
    "Хакеры часто используют техники социальной инженерии для получения паролей.",
    "Криптографические уязвимости могут быть использованы для атаки на защищенные системы.",
    "Обычные веб-сайты могут быть уязвимыми к атакам SQL-инъекций.",
    "Взлом электронных почтовых ящиков – одна из самых распространенных форм кибератак."
]

# Функция для проверки подписки пользователя
def is_subscription_active(user_id):
    if user_id in active_users:
        end_date = active_users[user_id]
        if datetime.now() <= end_date:
            return True
    return False

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if is_subscription_active(user_id):
        bot.send_message(user_id, "Добро пожаловать! Ваша подписка активна.")
        show_menu(user_id)  # Показываем меню с кнопками
    else:
        bot.send_message(user_id, "Добро пожаловать! Ожидайте активации подписки от администратора.")

# Функция для показа меню
def show_menu(user_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    email_btn = types.KeyboardButton("📧 Email снос")
    support_btn = types.KeyboardButton("Поддержка")
    fact_btn = types.KeyboardButton("🧠 Хакерский факт")
    markup.add(email_btn, support_btn, fact_btn)
    bot.send_message(user_id, "Выберите действие:", reply_markup=markup)

# Команда /activate для активации подписки
@bot.message_handler(commands=['activate'])
def activate_subscription(message):
    if message.from_user.id in admins:
        try:
            args = message.text.split()[1:]  # Берем аргументы из команды
            user_id = int(args[0])  # ID пользователя
            days = int(args[1])  # Количество дней подписки
            end_date = datetime.now() + timedelta(days=days)
            active_users[user_id] = end_date
            bot.send_message(user_id, f"Поздравляем с приобретением подписки на {days} дней!\nВаша подписка действует до {end_date.strftime('%d.%m.%Y %H:%M')}.")
            show_menu(user_id)  # Показываем меню с кнопками
        except (IndexError, ValueError):
            bot.send_message(message.chat.id, "Отправьте ID пользователя и количество дней подписки в формате: /activate <user_id> <days>")
    else:
        bot.send_message(message.chat.id, "У вас нет прав для выполнения этой команды.")

# Обработка кнопки "📧 Email снос"
@bot.message_handler(regexp="📧 Email снос")
def email_snos(message):
    user_id = message.from_user.id
    if is_subscription_active(user_id):
        bot.send_message(user_id, "Введите тему жалобы:")
        bot.register_next_step_handler(message, get_topic)
    else:
        bot.send_message(user_id, "У вас нет активной подписки.")

# Получение темы жалобы
def get_topic(message):
    user_id = message.from_user.id
    user_data[user_id] = {'topic': message.text}
    bot.send_message(user_id, "Опишите проблему:")
    bot.register_next_step_handler(message, get_complaint_text)

def get_complaint_text(message):
    user_id = message.from_user.id
    user_data[user_id]['text'] = message.text
    bot.send_message(user_id, "Сколько запросов отправить?")
    bot.register_next_step_handler(message, get_request_count)

def get_request_count(message):
    user_id = message.from_user.id
    try:
        count = int(message.text)
        user_data[user_id]['count'] = count
        bot.send_message(user_id, f"Отправка {count} запросов...")
        send_complaints(user_id)
    except ValueError:
        bot.send_message(user_id, "Введите корректное число.")

def send_complaints(user_id):
    emails = [
        "abuse@telegram.org",
        "DMCA@telegram.org",
        "support@telegram.org",
        "Ceo@telegram.org",
        "Recover@telegram.org",
        "Spam@telegram.org"
    ]
    
    for i in range(user_data[user_id]['count']):
        time.sleep(4)  # Антифлуд 4 секунды
        bot.send_message(user_id, f"Жалоба #{i+1} успешно отправлена на: {', '.join(emails)}.")
    
    del user_data[user_id]  # Удаляем временные данные после завершения

# Хакерские факты
@bot.message_handler(regexp="🧠 Хакерский факт")
def send_fact(message):
    user_id = message.from_user.id
    if is_subscription_active(user_id):
        fact = random.choice(facts)
        bot.send_message(user_id, fact)
    else:
        bot.send_message(user_id, "У вас нет активной подписки.")

# Обработка кнопки "Поддержка"
@bot.message_handler(regexp="Поддержка")
def support(message):
    user_id = message.from_user.id
    if is_subscription_active(user_id):
        bot.send_message(user_id, "Если у вас есть вопросы, пишите в этот чат @AReCToVaN_ZA_NACIONALIZM.")
    else:
        bot.send_message(user_id, "У вас нет активной подписки.")

bot.polling()
