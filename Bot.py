import telebot
from datetime import datetime, timedelta

TOKEN = "6702141092:AAFfXtlkW4U8fPT3VnBJMZToHP4GKjpwc2c"
ADMIN_ID = 1694921116  # Ваш Telegram ID

bot = telebot.TeleBot(TOKEN)

# Словарь для хранения подписок пользователей
user_subscriptions = {}

# Команда /start для всех пользователей
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Добро пожаловать! Дождитесь активации подписки от администратора.")

# Команда активации подписки, доступна только администратору
@bot.message_handler(commands=['activate'])
def activate_subscription(message):
    if message.from_user.id == ADMIN_ID:
        try:
            # Команда должна быть в формате: /activate <user_id> <days>
            command_parts = message.text.split()
            user_id = int(command_parts[1])
            days = int(command_parts[2])
            
            # Рассчитываем дату окончания подписки
            expiration_date = datetime.now() + timedelta(days=days)
            user_subscriptions[user_id] = expiration_date

            # Отправляем сообщение пользователю о начале подписки
            bot.send_message(user_id, f"Поздравляем с приобретением подписки на {days} дней.\n"
                                      f"Ваша подписка действует до {expiration_date.strftime('%d.%m.%Y %H:%M')}")

            # Подтверждаем активацию администратору
            bot.reply_to(message, f"Подписка на {days} дней успешно активирована для пользователя {user_id}.")
        except (IndexError, ValueError):
            bot.reply_to(message, "Неверный формат команды. Используйте: /activate <user_id> <days>")
        except Exception as e:
            bot.reply_to(message, f"Произошла ошибка: {e}")
    else:
        bot.reply_to(message, "У вас нет прав на использование этой команды.")

# Команда проверки подписки для всех пользователей
@bot.message_handler(commands=['check'])
def check_subscription(message):
    user_id = message.from_user.id
    if user_id in user_subscriptions:
        expiration_date = user_subscriptions[user_id]
        if datetime.now() < expiration_date:
            bot.reply_to(message, f"Ваша подписка действует до {expiration_date.strftime('%d.%m.%Y %H:%M')}")
        else:
            bot.reply_to(message, "Срок вашей подписки истек.")
    else:
        bot.reply_to(message, "У вас нет активной подписки.")

# Запуск бота
if __name__ == "__main__":
    bot.polling(none_stop=True)
