import telebot
from telebot import types

# Создание бота
bot = telebot.TeleBot("6699047318:AAGRIzgJy2LuPJWW59O0QsiuDCfZ20xxHws")

# Словари с данными
accounts = {
    "6 lvl": {"price": 500, "description": "Аккаунт 6 уровня с небольшим набором предметов и инвентарем."},
    "10 lvl": {"price": 1000, "description": "Аккаунт 10 уровня с хорошим набором предметов и инвентарем."},
    "15 lvl": {"price": 2500, "description": "Аккаунт 15 уровня с отличным набором предметов и инвентарем."},
    "20 lvl": {"price": 5000, "description": "Аккаунт 20 уровня с высокоуровневым набором предметов и инвентарем."},
    "23 lvl": {"price": 10000, "description": "Аккаунт 23 уровня с уникальными предметами и инвентарем."}
}

virtual_currency = {
    "50 000 виртов": 100,
    "100 000 виртов": 180,
    "500 000 виртов": 800,
    "1 000 000 виртов": 1500,
    "5 000 000 виртов": 6000,
    "10 000 000 виртов": 11000,
    "45 000 000 виртов": 45000
}

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
    item2 = types.KeyboardButton("Виртуальная валюта")
    item3 = types.KeyboardButton("Кейсы")
    markup.add(item1, item2, item3)
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

    # Обработка нажатия на кнопку "Виртуальная валюта"
    elif message.text == "Виртуальная валюта":
        bot.send_message(chat_id=message.chat.id, text="Здравствуйте, введите число виртов, мин 50тыс, максм 45млн.")
        
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
    bot.send_message(chat_id=chat_id, text="Выберите метод оплаты:\n\nТелеграм кошелек - UQC8Y2ZLGUJSmAasHTw_VNvO5jQ4w4OeJC_DQBO-wnqUItAL\nКаспи банк - 📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n☎️ Номер: 4400 4302 6934 6638\n👨‍💻 Имя - Данил Г.\n💬 Комментарий: НЕ ПИСАТЬ!!!\nСБП - Оплатить можно на карту РОССИИ: 2200701089399395 Аким. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")

# Запуск бота
bot.polling(none_stop=True)
