import telebot
from telebot import types

# Создание бота
bot = telebot.TeleBot("6699047318:AAGRIzgJy2LuPJWW59O0QsiuDCfZ20xxHws")

# Словарь с аккаунтами
accounts = {
    "6 уровень": {"price": 200, "description": "Аккаунт 6 уровня. Простой набор вещей, небольшой дом и автомобиль."},
    "10 уровень": {"price": 300, "description": "Аккаунт 10 уровня. Средний набор вещей и инвентаря, есть дом и хорошая машина."},
    "15 уровень": {"price": 400, "description": "Аккаунт 15 уровня. Богатый набор вещей, большой дом, дорогая машина и множество аксессуаров."},
    "20 уровень": {"price": 500, "description": "Аккаунт 20 уровня. Эксклюзивный набор вещей, роскошный особняк, самая дорогая машина, уникальные аксессуары."},
    "23 уровень": {"price": 550, "description": "Аккаунт 23 уровня. Аккаунт миллиардера. Все самое лучшее: одежда, имущество, транспорт и аксессуары."}
}

# Словарь с кейсами
cases = {
    "Бомж-кейс": 140,
    "Ежедневный кейс": 230,
    "Стандартный кейс": 350,
    "Особый кейс": 500,
    "Кейс с Блэк Коинами": 700
}

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Аккаунты")
    item2 = types.KeyboardButton("Кейсы")
    markup.add(item1, item2)
    bot.send_message(chat_id=message.chat.id, text="Привет! Что вы хотите купить?", reply_markup=markup)

# Обработка нажатия на кнопку "Аккаунты"
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Аккаунты":
        markup = types.InlineKeyboardMarkup()
        for account, data in accounts.items():
            button = types.InlineKeyboardButton(text=account, callback_data=account)
            markup.add(button)
        bot.send_message(chat_id=message.chat.id, text="Выберите аккаунт:", reply_markup=markup)

    # Обработка нажатия на кнопку "Кейсы"
    elif message.text == "Кейсы":
        markup = types.InlineKeyboardMarkup()
        for case, price in cases.items():
            button = types.InlineKeyboardButton(text=f"{case} - {price} руб.", callback_data=case)
            markup.add(button)
        bot.send_message(chat_id=message.chat.id, text="Выберите кейс:", reply_markup=markup)

# Обработка выбора аккаунта
@bot.callback_query_handler(func=lambda call: call.data in accounts)
def handle_account_selection(call):
    account = call.data
    description = accounts[account]["description"]
    price = accounts[account]["price"]
    bot.send_message(chat_id=call.message.chat.id, text=f"Вы выбрали аккаунт {account}:\n\n{description}\n\nЦена: {price} рублей")
    send_payment_instructions(call.message.chat.id)

# Обработка выбора кейса
@bot.callback_query_handler(func=lambda call: call.data in cases)
def handle_case_selection(call):
    case = call.data
    price = cases[case]
    bot.send_message(chat_id=call.message.chat.id, text=f"Вы выбрали {case} за {price} рублей")
    send_payment_instructions(call.message.chat.id)

# Функция для отправки инструкций по оплате
def send_payment_instructions(chat_id):
    text = """
Выберите метод оплаты:

Телеграм кошелек - UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL

Каспи банк - 
📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:
☎️ Номер: 4400 4302 6934 6638
👨‍💻 Имя - Данил Г.
💬 Комментарий: НЕ ПИСАТЬ!!!

СБП - 
Оплатить можно на карту РОССИИ: 2200701089399395 Аким.
После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров
"""
    markup = types.InlineKeyboardMarkup()

    telegram_button = types.InlineKeyboardButton(text="Оплатить через Telegram", url="tg://wallet?recipient=UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL")
    kaspi_button = types.InlineKeyboardButton(text="Оплатить через Kaspi Bank", url="https://kaspi.kz/u/4400430269346638")
    sbp_button = types.InlineKeyboardButton(text="Оплатить через СБП", url="https://sberbank.ru/ru/person/bank_cards/sbp")
    markup.add(telegram_button, kaspi_button, sbp_button)
    bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

# Запуск бота
bot.polling(none_stop=True)
