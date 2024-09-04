from telebot import Bot, Dispatcher, types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from telebot.utils import executor

# Вставьте ваш токен
TOKEN = "7389514448:AAEAHWWJP6E6zisO0BqEoGrYD-DrRrWEEbs"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Кнопки на клавиатуре с эмодзи
button_requisites_kaspi = KeyboardButton('📩 Реквизиты Kaspi Gold')
button_requisites_halyk = KeyboardButton('📩 Реквизиты Halyk Bank')
button_contact_admin = KeyboardButton('📞 Связь с админом')
button_services = KeyboardButton('💼 Услуга')

# Создание клавиатуры
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_requisites_kaspi).add(button_requisites_halyk).add(button_contact_admin).add(button_services)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Выберите нужную опцию ниже:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == '📩 Реквизиты Kaspi Gold')
async def send_kaspi_requisites(message: types.Message):
    await message.reply("📩 Отправьте деньги по реквизитам на Kaspi Gold 🔥:\n☎️ Номер: 4400 4302 6934 6638\n👨‍💻 Имя - Данил Г.\n💬 Комментарий: НЕ ПИСАТЬ!!!")

@dp.message_handler(lambda message: message.text == '📩 Реквизиты Halyk Bank')
async def send_halyk_requisites(message: types.Message):
    await message.reply("📩 Отправьте деньги по реквизитам на Halyk Bank 🔥:\n☎️ Номер: 4405 6398 0709 6001\n👨‍💻 Имя - Данил Г.\n💬 Комментарий: НЕ ПИСАТЬ!!!")

@dp.message_handler(lambda message: message.text == '📞 Связь с админом')
async def contact_admin(message: types.Message):
    await message.reply("Пожалуйста, по всем вопросам пишите сюда @B6lyat")

@dp.message_handler(lambda message: message.text == '💼 Услуга')
async def services(message: types.Message):
    await message.reply("💼 Деанон человека - 600 тг\n💼 Фото человека - 600 тг\n💼 Узнать номера родителей человека - 800 тг\n💼 Написать человеку угрозы - 800 тг")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == 'info_1':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")
    elif call.data == 'info_2':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")
    elif call.data == 'info_3':
        bot.send_message(call.message.chat.id, "Оплатить можно на карту РОССИИ: 2200701089399395 Амир. После оплаты свяжитесь с автором данного бота @doksformoney для дальнейших переговоров")

# Запуск бота
bot.polling(none_stop=True)
