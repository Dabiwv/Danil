import telebot
from telebot import types

API_TOKEN = '6692785864:AAEqASjDj-9JcmIZKGOjCSgvXWXDv7E7KaY'  # Замените на ваш токен
bot = telebot.TeleBot(API_TOKEN)

# Данные об аккаунтах, виртах и кейсах
accounts = {
    10: {"price": 1000, "description": "Аккаунт уровень 10, машина: ЗАЗ 968", "car": "ЗАЗ 968"},
    11: {"price": 1200, "description": "Аккаунт уровень 11, машина: ВАЗ 2101", "car": "ВАЗ 2101"},
    12: {"price": 1400, "description": "Аккаунт уровень 12, машина: ВАЗ 2107", "car": "ВАЗ 2107"},
    13: {"price": 1600, "description": "Аккаунт уровень 13, машина: ВАЗ 2110", "car": "ВАЗ 2110"},
    14: {"price": 1800, "description": "Аккаунт уровень 14, машина: ВАЗ 2115", "car": "ВАЗ 2115"},
    15: {"price": 2000, "description": "Аккаунт уровень 15, машина: Киа Рио", "car": "Киа Рио"},
    16: {"price": 2200, "description": "Аккаунт уровень 16, машина: Хендай Солярис", "car": "Хендай Солярис"},
    17: {"price": 2400, "description": "Аккаунт уровень 17, машина: Лада Веста", "car": "Лада Веста"},
    18: {"price": 2600, "description": "Аккаунт уровень 18, машина: Мицубиси Лансер", "car": "Мицубиси Лансер"},
    19: {"price": 2800, "description": "Аккаунт уровень 19, машина: Тойота Королла", "car": "Тойота Королла"},
    20: {"price": 3000, "description": "Аккаунт уровень 20, машина: Хонда Цивик", "car": "Хонда Цивик"},
    21: {"price": 3200, "description": "Аккаунт уровень 21, машина: Ауди А3", "car": "Ауди А3"},
    22: {"price": 3400, "description": "Аккаунт уровень 22, машина: БМВ 3 серии", "car": "БМВ 3 серии"},
    23: {"price": 3600, "description": "Аккаунт уровень 23, машина: Мерседес C-класс", "car": "Мерседес C-класс"},
    24: {"price": 3800, "description": "Аккаунт уровень 24, машина: Лексус IS", "car": "Лексус IS"},
    25: {"price": 4000, "description": "Аккаунт уровень 25, машина: Инфинити Q50", "car": "Инфинити Q50"},
    26: {"price": 4200, "description": "Аккаунт уровень 26, машина: Порше Панамера", "car": "Порше Панамера"},
    27: {"price": 7000, "description": "Аккаунт уровень 27, машина: Bugatti La Noire", "car": "Bugatti La Noire"}
}

cases = {
    "Бомж": 140,
    "Ежедневный": 200,
    "Стандартный": 300,
    "Особый": 450,
    "Кейс ха Блек коины": 700
}

# Хендлер для команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("Аккаунты"), types.KeyboardButton("Вирты"), types.KeyboardButton("Кейсы"))
    bot.send_message(message.chat.id, "Добро пожаловать! Выберите, что вы хотите купить:", reply_markup=markup)

# Хендлер для кнопок меню
@bot.message_handler(func=lambda message: message.text in ["Аккаунты", "Вирты", "Кейсы"])
def handle_menu(message):
    if message.text == "Аккаунты":
        markup = types.InlineKeyboardMarkup()
        for level in range(10, 28):
            account = accounts[level]
            markup.add(types.InlineKeyboardButton(f"Уровень {level}: {account['car']}", callback_data=f"account_{level}"))
        bot.send_message(message.chat.id, "Выберите аккаунт:", reply_markup=markup)
    elif message.text == "Вирты":
        bot.send_message(message.chat.id, "Здравствуйте, введите число виртов (мин 50 000, макс 45 000 000):")
    elif message.text == "Кейсы":
        markup = types.InlineKeyboardMarkup()
        for case, price in cases.items():
            markup.add(types.InlineKeyboardButton(f"{case}: {price} рублей", callback_data=f"case_{case}"))
        bot.send_message(message.chat.id, "Выберите кейс:", reply_markup=markup)

# Хендлер для выбора аккаунта
@bot.callback_query_handler(lambda c: c.data.startswith('account_'))
def process_account(callback_query):
    level = int(callback_query.data.split('_')[1])
    account = accounts[level]
    message = (
        f"Вы выбрали аккаунт уровня {level}.\n"
        f"Описание: {account['description']}\n\n"
        "Выберите метод оплаты:\n"
        "1. Телеграм кошелек - UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL\n"
        "2. Каспи банк - 📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n"
        "   ☎️ Номер: 4400 4302 6934 6638\n"
        "   👨‍💻 Имя - Данил Г.\n"
        "   💬 Комментарий: НЕ ПИСАТЬ!!!\n"
        "3. СБП - Оплатить можно на карту РОССИИ: 2200701089399395 Аким.\n"
        "После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров"
    )
    bot.send_message(callback_query.from_user.id, message)

# Хендлер для выбора кейса
@bot.callback_query_handler(lambda c: c.data.startswith('case_'))
def process_case(callback_query):
    case = callback_query.data.split('_')[1]
    price = cases[case]
    message = (
        f"Вы выбрали кейс '{case}'.\n"
        f"Цена: {price} рублей\n\n"
        "Выберите метод оплаты:\n"
        "1. Телеграм кошелек - UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL\n"
        "2. Каспи банк - 📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n"
        "   ☎️ Номер: 4400 4302 6934 6638\n"
        "   👨‍💻 Имя - Данил Г.\n"
        "   💬 Комментарий: НЕ ПИСАТЬ!!!\n"
        "3. СБП - Оплатить можно на карту РОССИИ: 2200701089399395 Аким.\n"
        "После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров"
    )
    bot.send_message(callback_query.from_user.id, message)

# Хендлер для виртуальной валюты
@bot.message_handler(func=lambda message: message.text.isdigit())
def process_virts(message):
    amount = int(message.text)
    if 50000 <= amount <= 45000000:
        price = (amount / 1000)  # Примерный расчет, замените на свой
        bot.send_message(
            message.chat.id,
            f"Вы выбрали {amount} виртов.\n"
            f"Цена: {price} рублей\n\n"
            "Выберите метод оплаты:\n"
            "1. Телеграм кошелек - UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL\n"
            "2. Каспи банк - 📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n"
            "   ☎️ Номер: 4400 4302 6934 6638\n"
            "   👨‍💻 Имя - Данил Г.\n"
            "   💬 Комментарий: НЕ ПИСАТЬ!!!\n"
            "3. СБП - Оплатить можно на карту РОССИИ: 2200701089399395 Аким.\n"
            "После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров"
        )
    else:
        bot.send_message(message.chat.id, "Введите число виртов в диапазоне от 50 000 до 45 000 000.")

# Запуск бота
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(bot, skip_updates=True)
