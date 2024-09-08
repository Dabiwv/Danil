from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from datetime import datetime, timedelta
import logging

# Вставьте ваш токен
TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"
# Ваш ID
ADMIN_ID = 1694921116

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище данных о пользователях и подписках
user_subscriptions = {}

def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id == ADMIN_ID:
        update.message.reply_text("Привет, администратор! Используйте /activate <user_id> <days> для активации подписки.")
    else:
        update.message.reply_text("Привет! Для получения помощи напишите администратору.")

def activate(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("Вы не администратор.")
        return
    
    if len(context.args) != 2:
        update.message.reply_text("Использование: /activate <user_id> <days>")
        return
    
    try:
        target_user_id = int(context.args[0])
        days = int(context.args[1])
        if days <= 0:
            update.message.reply_text("Количество дней должно быть положительным числом.")
            return
    except ValueError:
        update.message.reply_text("Введите правильные значения.")
        return
    
    expiry_date = datetime.now() + timedelta(days=days)
    user_subscriptions[target_user_id] = expiry_date
    
    # Уведомление пользователю
    context.bot.send_message(
        chat_id=target_user_id,
        text=f"Поздравляем с приобретением подписки на {days} день(дня)!\nВаша подписка действует до {expiry_date.strftime('%d.%m.%Y %H:%M')}"
    )
    update.message.reply_text("Подписка успешно активирована.")

def email_complaints(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_subscriptions or user_subscriptions[user_id] < datetime.now():
        update.message.reply_text("Ваша подписка неактивна или истекла. Обратитесь к администратору для активации.")
        return
    
    update.message.reply_text("Введите тему жалобы:")

    # Сохранение состояния для последующей обработки
    context.user_data['complaint'] = {'state': 'subject'}

def handle_complaint(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in user_subscriptions or user_subscriptions[user_id] < datetime.now():
        update.message.reply_text("Ваша подписка неактивна или истекла. Обратитесь к администратору для активации.")
        return

    if 'complaint' not in context.user_data:
        return
    
    state = context.user_data['complaint']['state']
    if state == 'subject':
        context.user_data['complaint']['subject'] = update.message.text
        context.user_data['complaint']['state'] = 'body'
        update.message.reply_text("Теперь введите текст жалобы:")
    elif state == 'body':
        context.user_data['complaint']['body'] = update.message.text
        context.user_data['complaint']['state'] = 'requests'
        update.message.reply_text("Сколько запросов отправить?")
    elif state == 'requests':
        try:
            num_requests = int(update.message.text)
            if num_requests <= 0:
                raise ValueError
        except ValueError:
            update.message.reply_text("Пожалуйста, введите корректное количество запросов.")
            return

        subject = context.user_data['complaint']['subject']
        body = context.user_data['complaint']['body']
        update.message.reply_text("Жалобы успешно отправлены!")  # Здесь добавьте имитацию отправки

        # Очистка данных
        del context.user_data['complaint']

def support(update: Update, context: CallbackContext):
    update.message.reply_text("Если у вас есть вопросы, напишите в этот чат @AReCToVaN_ZA_NACIONALIZM")

def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("activate", activate))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_complaint))
    dp.add_handler(CommandHandler("support", support))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
