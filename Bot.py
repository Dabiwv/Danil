from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
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
user_data = {}

def get_keyboard():
    return ReplyKeyboardMarkup([
        [KeyboardButton("📧 Email снос")],
        [KeyboardButton("💬 Поддержка")]
    ], resize_keyboard=True)

async def start(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in subscriptions and datetime.now() <= subscriptions[user_id]:
        keyboard = get_keyboard()
        await update.message.reply_text("Привет! Выберите действие:", reply_markup=keyboard)
    else:
        await update.message.reply_text("Добро пожаловать! Ожидайте активации подписки от администратора.")

async def activate(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id == ADMIN_ID:
        if len(context.args) == 2:
            try:
                target_user_id = int(context.args[0])
                days = int(context.args[1])
                expiry_date = datetime.now() + timedelta(days=days)
                subscriptions[target_user_id] = expiry_date

                # Отправка сообщения пользователю
                await context.bot.send_message(
                    target_user_id,
                    f"Поздравляем с приобретением подписки на {days} дней. Ваша подписка действует до {expiry_date.strftime('%d.%m.%Y %H:%M')}.",
                )
                
                # Отправка сообщения пользователю и установка кнопок
                keyboard = get_keyboard()
                await context.bot.send_message(
                    target_user_id,
                    "Добро пожаловать! Ваша подписка активирована. Выберите действие:",
                    reply_markup=keyboard
                )

                # Отправка сообщения администратору
                await update.message.reply_text(f"Подписка для пользователя {target_user_id} активирована на {days} дней.")
            except ValueError:
                await update.message.reply_text("Ошибка в формате. Убедитесь, что вы вводите ID пользователя и количество дней.")
        else:
            await update.message.reply_text("Используйте правильный формат: /activate <user_id> <days>")
    else:
        await update.message.reply_text("У вас нет прав для выполнения этой команды.")

async def email_snos(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in subscriptions and datetime.now() <= subscriptions[user_id]:
        await update.message.reply_text("Введите тему жалобы:")
        user_data[user_id] = {'stage': 'subject'}
    else:
        await update.message.reply_text("Ваша подписка истекла или не активирована. Пожалуйста, свяжитесь с администратором для получения доступа.")

async def support(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id in subscriptions and datetime.now() <= subscriptions[user_id]:
        await update.message.reply_text("Добавьте свой текст. Если у вас есть вопросы, пишите сюда: @AReCToVaN_ZA_NACIONALIZM")
    else:
        await update.message.reply_text("Ваша подписка истекла или не активирована. Пожалуйста, свяжитесь с администратором для получения доступа.")

if __name__ == '__main__':
    application = Application.builder().token(TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("activate", activate))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("📧 Email снос"), email_snos))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex("💬 Поддержка"), support))

    application.run_polling()
