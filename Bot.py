from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
from datetime import datetime, timedelta
import logging

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"
# Ваш ID
ADMIN_ID = 1694921116

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Переменные для хранения данных пользователей
user_data = {}
subscriptions = {}

async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    keyboard = [
        ["📧 Email снос"],
        ["💬 Поддержка"]
    ]
    reply_markup = context.bot.build_reply_markup(keyboard)
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)

async def activate(update: Update, context: CallbackContext):
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("Отправьте ID пользователя и количество дней подписки в формате: /activate <user_id> <days>")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")

async def process_activate(update: Update, context: CallbackContext):
    if update.effective_user.id == ADMIN_ID:
        try:
            user_id = int(context.args[0])
            days = int(context.args[1])
            expiry_date = datetime.now() + timedelta(days=days)
            subscriptions[user_id] = expiry_date
            await context.bot.send_message(user_id, f"Поздравляем с приобретением подписки на {days}d. Ваша подписка действует до {expiry_date.strftime('%d.%m.%Y %H:%M')}")
            await update.message.reply_text("Подписка успешно активирована!")
        except (IndexError, ValueError):
            await update.message.reply_text("Использование: /activate <user_id> <days>")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")

async def email_snos(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in subscriptions and subscriptions[user_id] > datetime.now():
        user_data[user_id] = {}
        await update.message.reply_text("Введите тему жалобы:")
    else:
        await update.message.reply_text("Ваша подписка истекла или не активирована.")

async def process_complaint(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in user_data:
        if 'subject' not in user_data[user_id]:
            user_data[user_id]['subject'] = update.message.text
            await update.message.reply_text("Теперь введите текст жалобы:")
        elif 'body' not in user_data[user_id]:
            user_data[user_id]['body'] = update.message.text
            await update.message.reply_text("Сколько запросов отправить?")
        elif 'num_requests' not in user_data[user_id]:
            try:
                num_requests = int(update.message.text)
                await update.message.reply_text(f"Отправляю {num_requests} запросов...")
                # Имитация отправки жалоб
                for _ in range(num_requests):
                    await update.message.reply_text("Жалобы успешно отправлены!")
                user_data.pop(user_id, None)  # Удаляем данные после отправки
            except ValueError:
                await update.message.reply_text("Пожалуйста, введите корректное количество запросов.")
    else:
        await update.message.reply_text("Вы не начали процесс отправки жалобы.")

async def support(update: Update, context: CallbackContext):
    await update.message.reply_text("Напишите ваше обращение и админ вам ответит. Если у вас есть вопросы, пишите сюда @AReCToVaN_ZA_NACIONALIZM")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("activate", activate))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^/activate'), process_activate))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^📧 Email снос$'), email_snos))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, process_complaint))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^💬 Поддержка$'), support))

    application.run_polling()

if __name__ == '__main__':
    main()
