import smtplib
from email.mime.text import MIMEText
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"

# SMTP настройки
smtp_server = 'smtp.gmail.com'
smtp_port = 587
smtp_user = 'Makarkoh39@gmail.com'
smtp_password = '09) 09) 09)'

# Кнопки на клавиатуре
button_email = KeyboardButton('📧 Email снос')
button_support = KeyboardButton('💬 Поддержка')

keyboard = ReplyKeyboardMarkup([[button_email, button_support]], resize_keyboard=True)

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

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Привет! Выберите действие:", reply_markup=keyboard)

def email_snos(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    user_data[user_id] = {}  # Инициализируем данные пользователя
    update.message.reply_text("Введите тему жалобы:")

def process_complaint(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    if 'subject' not in user_data[user_id]:
        user_data[user_id]['subject'] = update.message.text
        update.message.reply_text("Теперь введите текст жалобы:")
    elif 'body' not in user_data[user_id]:
        user_data[user_id]['body'] = update.message.text
        update.message.reply_text("Сколько запросов отправить?")
    elif 'num_requests' not in user_data[user_id]:
        try:
            num_requests = int(update.message.text)
            user_data[user_id]['num_requests'] = num_requests
            update.message.reply_text(f"Отправляю {num_requests} запросов...")
            send_complaint(
                user_data[user_id]['subject'],
                user_data[user_id]['body'],
                num_requests,
                update.message
            )
        except ValueError:
            update.message.reply_text("Пожалуйста, введите корректное количество запросов.")

def support(update: Update, context: CallbackContext):
    update.message.reply_text("Напишите ваше обращение и админ вам ответит")

def send_complaint(subject, body, num_requests, message):
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
        message.reply_text("Жалобы успешно отправлены!")
    except Exception as e:
        message.reply_text(f"Произошла ошибка при отправке жалоб: {e}")

def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Обработчики команд
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.regex('📧 Email снос'), email_snos))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, process_complaint))
    dispatcher.add_handler(MessageHandler(Filters.regex('💬 Поддержка'), support))

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
