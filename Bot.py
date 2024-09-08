import smtplib
from email.mime.text import MIMEText
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# SMTP настройки
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'Makarkoh39@gmail.com'
smtp_password = '09) 09) 09)'

# Кнопки на клавиатуре
button_email = KeyboardButton('📧 Email снос')
button_support = KeyboardButton('💬 Поддержка')

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add(button_email).add(button_support)

# Список почт для отправки жалоб
recipients = [
    "abuse@telegram.org",
    "DMCA@telegram.org",
    "support@telegram.org",
    "Ceo@telegram.org",
    "Recover@telegram.org",
    "Spam@telegram.org"
]

# Переменная для хранения данных пользователей
user_data = {}

async def send_complaint(subject, body, num_requests, message):
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_user, smtp_password)

        for _ in range(num_requests):
            for recipient in recipients:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = smtp_user
                msg['To'] = recipient
                server.sendmail(smtp_user, recipient, msg.as_string())

        server.quit()
        await message.reply("Жалобы успешно отправлены!")
    except Exception as e:
        await message.reply(f"Произошла ошибка при отправке жалоб: {e}")

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Выберите действие:", reply_markup=keyboard)

@dp.message_handler(lambda message: message.text == '📧 Email снос')
async def email_snos(message: types.Message):
    user_id = message.from_user.id
    user_data[user_id] = {}  # Инициализируем данные пользователя
    await message.reply("Введите тему жалобы:")

@dp.message_handler(lambda message: message.text not in ['📧 Email снос', '💬 Поддержка'])
async def process_complaint(message: types.Message):
    user_id = message.from_user.id

    if 'subject' not in user_data[user_id]:
        user_data[user_id]['subject'] = message.text
        await message.reply("Теперь введите текст жалобы:")
    elif 'body' not in user_data[user_id]:
        user_data[user_id]['body'] = message.text
        await message.reply("Сколько запросов отправить?")
    elif 'num_requests' not in user_data[user_id]:
        try:
            num_requests = int(message.text)
            user_data[user_id]['num_requests'] = num_requests
            await message.reply(f"Отправляю {num_requests} запросов...")
            await send_complaint(
                user_data[user_id]['subject'],
                user_data[user_id]['body'],
                num_requests,
                message
            )
        except ValueError:
            await message.reply("Пожалуйста, введите корректное количество запросов.")

@dp.message_handler(lambda message: message.text == '💬 Поддержка')
async def support(message: types.Message):
    await message.reply("Напишите ваше обращение и админ вам ответит")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
