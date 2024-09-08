from telegram import Update
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
subscriptions = {}

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in subscriptions and datetime.now() <= subscriptions[user_id]:
        keyboard = [
            ["📧 Email снос"],
            ["💬 Поддержка"]
        ]
        reply_markup = context.bot.build_reply_markup(keyboard)
        await update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Добро пожаловать! Ожидайте активации подписки от администратора.")

async def activate(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        await update.message.reply_text("Отправьте ID пользователя и количество дней подписки в формате: /activate <user_id> <days>")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")

async def process_activate(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        try:
            args = context.args
            if len(args) != 2:
                raise ValueError("Неверное количество аргументов.")
                
            target_user_id = int(args[0])
            days = int(args[1])
            expiry_date = datetime.now() + timedelta(days=days)
            subscriptions[target_user_id] = expiry_date
            await context.bot.send_message(target_user_id, f"Поздравляем с приобретением подписки на {days} дней. Ваша подписка действует до {expiry_date.strftime('%d.%m.%Y %H:%M')}")
        except Exception as e:
            await update.message.reply_text(f"Произошла ошибка: {e}")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")

async def email_snos(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in subscriptions and datetime.now() <= subscriptions[user_id]:
        await update.message.reply_text("Введите тему жалобы:")
        user_data[user_id] = {'stage': 'subject'}
    else:
        await update.message.reply_text("Ваша подписка истекла или не активирована. Пожалуйста, активируйте её снова.")

async def support(update: Update, context: CallbackContext):
    await update.message.reply_text("Добавьте свой текст. Если у вас есть вопросы, пишите в этот чат @AReCToVaN_ZA_NACIONALIZM")

async def handle_text(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in user_data:
        stage = user_data[user_id].get('stage')
        if stage == 'subject':
            user_data[user_id]['subject'] = update.message.text
            await update.message.reply_text("Теперь введите текст жалобы:")
            user_data[user_id]['stage'] = 'body'
        elif stage == 'body':
            user_data[user_id]['body'] = update.message.text
            await update.message.reply_text("Сколько запросов отправить?")
            user_data[user_id]['stage'] = 'num_requests'
        elif stage == 'num_requests':
            try:
                num_requests = int(update.message.text)
                await update.message.reply_text(f"Отправляю {num_requests} запросов...")
                # Имитация отправки жалоб
                for _ in range(num_requests):
                    await update.message.reply_text("Жалобы успешно отправлены!")
                del user_data[user_id]  # Очистка данных пользователя
            except ValueError:
                await update.message.reply_text("Пожалуйста, введите корректное количество запросов.")
    else:
        await update.message.reply_text("Сначала активируйте подписку.")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("activate", activate))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    application.add_handler(CommandHandler("activate", process_activate))

    application.run_polling()

if __name__ == "__main__":
    main()
