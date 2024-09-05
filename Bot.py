import telebot
from telebot import types

# Создание бота
bot = telebot.TeleBot("6699047318:AAGRIzgJy2LuPJWW59O0QsiuDCfZ20xxHws")

# Словарь с аккаунтами
accounts = {
    "Начинающий аккаунт": {
        "description": "Этот аккаунт подходит для начинающих игроков. В нем уже есть 23 бойца с максимальным рангом 10, а также 3000 кубков. Отлично подойдет для изучения основ игры.",
        "trophies": 3000,
        "brawlers": 23,
        "brawler_ranks": 10,
        "brawl_pass": False,
        "price": 160
    },
    "Средний аккаунт": {
        "description": "Средний аккаунт имеет 45 бойцов с рангом до 18, а также 12000 кубков. Этот аккаунт уже прошел этап освоения и готов для более интенсивной игры. Также включает активный Brawl Pass.",
        "trophies": 12000,
        "brawlers": 45,
        "brawler_ranks": 18,
        "brawl_pass": True,
        "price": 320
    },
    "Продвинутый аккаунт": {
        "description": "Продвинутый аккаунт обладает 55 бойцами с максимальным рангом 25 и 18000 кубков. Это отличный аккаунт для игроков, достигших высокого уровня мастерства. Также включает активный Brawl Pass.",
        "trophies": 18000,
        "brawlers": 55,
        "brawler_ranks": 25,
        "brawl_pass": True,
        "price": 440
    },
    "Элитный аккаунт": {
        "description": "Элитный аккаунт является одним из лучших. В нем 65 бойцов с рангом до 30 и 25000 кубков. Отлично подходит для соревновательной игры на высоком уровне. Также включает активный Brawl Pass.",
        "trophies": 25000,
        "brawlers": 65,
        "brawler_ranks": 30,
        "brawl_pass": True,
        "price": 550
    },
    "Топ-аккаунт": {
        "description": "Топ-аккаунт является наивысшим уровнем. В нем 78 бойцов с максимальным рангом 35 и 35000 кубков. Это идеальный выбор для опытных игроков, стремящихся к вершинам рейтинга. Также включает активный Brawl Pass.",
        "trophies": 35000,
        "brawlers": 78,
        "brawler_ranks": 35,
        "brawl_pass": True,
        "price": 660
    }
}

# Обработка команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Аккаунты")
    markup.add(item1)
    bot.send_message(chat_id=message.chat.id, text="Добро пожаловать в магазин аккаунтов Brawl Stars! Что вы хотите купить?", reply_markup=markup)

# Обработка нажатия на кнопку "Аккаунты"
@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == "Аккаунты":
        markup = types.InlineKeyboardMarkup()
        for account, data in accounts.items():
            button = types.InlineKeyboardButton(text=f"{account} - {data['price']} руб.", callback_data=account)
            markup.add(button)
        bot.send_message(chat_id=message.chat.id, text="Выберите аккаунт:", reply_markup=markup)

# Обработка выбора аккаунта
@bot.callback_query_handler(func=lambda call: call.data in accounts)
def handle_account_selection(call):
    account = call.data
    data = accounts[account]
    description = f"Выбран аккаунт: {account}\n\n{data['description']}\n\n" \
                  f"Кубков: {data['trophies']}\n" \
                  f"Бойцов: {data['brawlers']}\n" \
                  f"Ранг бойцов: до {data['brawler_ranks']}\n" \
                  f"Brawl Pass: {'Есть' if data['brawl_pass'] else 'Нет'}\n\n" \
                  f"Цена: {data['price']} рублей"
    bot.send_message(chat_id=call.message.chat.id, text=description)
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
