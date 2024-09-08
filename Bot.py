from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"

# Кнопки на клавиатуре
button_email = KeyboardButton('📧 Email снос')
button_support = KeyboardButton('💬 Поддержка')

keyboard = ReplyKeyboardMarkup([[button_email, button_support]], resize_keyboard=True)

# Переменная для хранения данных пользователей
user_data = {}

# Имитируемый список почт
recipients = [
    "abuse@telegram.org",
    "DMCA@telegram.org",
    "support@telegram.org",
    "Ceo@telegram.org",
    "Recover@telegram.org",
    "Spam@telegram.org"
]

# Функция для имитации отправки жалоб
async def send_complaint(subject, body, num_requests, message: Update):
    try:
        for _ in range(num_requests):
            for recipient in recipients:
                # Имитируем отправку жалобы
                print(f"Отправка жалобы на {recipient}: Тема: {subject}, Текст: {body}")

        await message.message.reply_text("Жалобы успешно отправлены (имитация)!")
    except Exception as e:
        await message.message.reply_text(f"Произошла ошибка при отправке жалоб: {e}")

# Обработчик команды /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=keyboard)

# Обработчик для кнопки "📧 Email снос"
async def email_snos(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data[user_id] = {}  # Инициализируем данные пользователя
    await update.message.reply_text("Введите тему жалобы:")

# Обработка жалоб
async def process_complaint(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if 'subject' not in user_data[user_id]:
        user_data[user_id]['subject'] = update.message.text
        await update.message.reply_text("Теперь введите текст жалобы:")
    elif 'body' not in user_data[user_id]:
        user_data[user_id]['body'] = update.message.text
        await update.message.reply_text("Сколько запросов отправить?")
    elif 'num_requests' not in user_data[user_id]:
        try:
            num_requests = int(update.message.text)
            user_data[user_id]['num_requests'] = num_requests
            await update.message.reply_text(f"Имитирую отправку {num_requests} запросов...")
            await send_complaint(
                user_data[user_id]['subject'],
                user_data[user_id]['body'],
                num_requests,
                update
            )
        except ValueError:
            await update.message.reply_text("Пожалуйста, введите корректное количество запросов.")

# Обработчик для кнопки "💬 Поддержка"
async def support(update: Update, context: CallbackContext):
    await update.message.reply_text("Напишите ваше обращение, и админ вам ответит.")

# Основная функция запуска бота
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Text('📧 Email снос'), email_snos))
    app.add_handler(MessageHandler(filters.Text('💬 Поддержка'), support))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_complaint))

    print("Бот запущен...")
    app.run_polling()

if __name__ == '__main__':
    main()
