import time
import asyncio
from telethon import TelegramClient, events

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+7 776 6349341'

# Создаем клиент Telethon
client = TelegramClient('auto_responder', api_id, api_hash)

# Параметры антиспама
MESSAGE_LIMIT = 5  # Максимум сообщений за время ниже
TIME_WINDOW = 60  # Интервал в секундах (например, 60 секунд)
BLOCK_TIME = 1800  # Время блокировки (30 минут = 1800 секунд)

# Храним информацию о пользователях
user_messages = {}  # Сообщения пользователя за последний промежуток времени
blocked_users = {}  # Время разблокировки пользователя

# Функция для проверки на блокировку пользователя
def is_blocked(user_id):
    return user_id in blocked_users and time.time() < blocked_users[user_id]

# Функция для добавления сообщения от пользователя
def add_message(user_id):
    now = time.time()

    if user_id not in user_messages:
        user_messages[user_id] = []

    # Убираем старые сообщения
    user_messages[user_id] = [msg_time for msg_time in user_messages[user_id] if now - msg_time < TIME_WINDOW]
    
    # Добавляем текущее сообщение
    user_messages[user_id].append(now)

    # Проверяем, не превысил ли пользователь лимит сообщений
    if len(user_messages[user_id]) > MESSAGE_LIMIT:
        blocked_users[user_id] = now + BLOCK_TIME  # Блокируем пользователя на BLOCK_TIME секунд
        return True
    return False

# Обработчик новых сообщений
@client.on(events.NewMessage(incoming=True))
async def handler(event):
    sender = await event.get_sender()
    sender_id = sender.id

    # Если пользователь заблокирован, игнорируем его сообщения
    if is_blocked(sender_id):
        print(f"Пользователь {sender_id} заблокирован.")
        return

    # Добавляем сообщение от пользователя и проверяем на спам
    if add_message(sender_id):
        await event.respond("Вы отправляете слишком много сообщений. Вас заблокировали на 30 минут.")
        print(f"Пользователь {sender_id} заблокирован за спам.")
        return

    # Автоответчик
    await event.respond("Вас приветствует Кристалл, за меня отвечает автоответчик. Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. Просьба не спамить!")
    print(f"Ответ пользователю {sender_id} отправлен.")

# Запуск клиента
async def main():
    await client.start(phone_number)
    print("Бот запущен...")
    await client.run_until_disconnected()

# Запуск асинхронного кода
asyncio.run(main())
