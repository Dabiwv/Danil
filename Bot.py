from telebot import TeleBot, types
import random
import time

bot_token = '6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c'
bot = TeleBot(bot_token)

# ID админов
admins = [1694921116, 6858042867]

# Факты о хакерстве
facts = [
    "Первый хакерский взлом был в 1903 году.",
    "Самый длинный пароль в мире содержит 189 819 символов.",
    "Анонимус - одна из самых известных хакерских группировок.",
    "SQL-инъекции - один из самых распространённых методов взлома.",
    "Социальная инженерия - популярная техника у хакеров.",
    "Первые вирусы создавались в учебных целях.",
    "95% успешных хакерских атак вызваны человеческими ошибками.",
    "Хакеры могут взламывать умные лампочки.",
    "Первые хакеры были радиолюбителями.",
    "Мировая экономика теряет до 600 миллиардов долларов ежегодно из-за киберпреступлений."
]

# Словарь для временного хранения данных пользователя (например, тема и текст жалобы)
user_data = {}

# Начало работы
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    if user_id in admins:
        bot.send_message(message.chat.id, "Привет, админ! Вы можете активировать подписки через /activate.")
    else:
        bot.send_message(message.chat.id, "Добро пожаловать! Ожидайте активации подписки от администратора.")

    # Добавляем кнопки
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    email_btn = types.KeyboardButton("📧 Email снос")
    support_btn = types.KeyboardButton("Поддержка")
    fact_btn = types.KeyboardButton("🧠 Хакерский факт")
    markup.add(email_btn, support_btn, fact_btn)
    bot.send_message(message.chat.id, "Выберите действие:", reply_markup=markup)

# Поддержка
@bot.message_handler(regexp="Поддержка")
def handle_support(message):
    bot.send_message(message.chat.id, "Если у вас есть вопросы, пишите в этот чат: @AReCToVaN_ZA_NACIONALИЗM")

# Обработка кнопки "📧 Email снос"
@bot.message_handler(regexp="📧 Email снос")
def email_snos(message):
    user_id = message.from_user.id
    bot.send_message(user_id, "Введите тему жалобы:")
    bot.register_next_step_handler(message, get_topic)

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
        # Имитируем отправку жалобы
        bot.send_message(user_id, f"Жалоба #{i+1} успешно отправлена на: {', '.join(emails)}.")
    
    del user_data[user_id]  # Удаляем временные данные после завершения

# Хакерские факты
@bot.message_handler(regexp="🧠 Хакерский факт")
def send_fact(message):
    fact = random.choice(facts)
    bot.send_message(message.chat.id, fact)

# Запуск бота
bot.polling()
