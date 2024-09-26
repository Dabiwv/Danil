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
MESSAGE_LIMIT = 6  # Максимум сообщений за время ниже
TIME_WINDOW_PRIVATE = 20  # Интервал в секундах для личных чатов
TIME_WINDOW_GROUP = 120  # Интервал в секундах для групп
BLOCK_TIME = 1800  # Время блокировки (30 минут = 1800 секунд)

# Храним информацию о пользователях
user_messages = {}  # Сообщения пользователя за последний промежуток времени
blocked_users = {}  # Время разблокировки пользователя

# ID вашего аккаунта
OWNER_ID = 1694921116

# Флаги для автоответчика и рассылки
auto_reply_enabled = False
broadcast_enabled = True

# Сообщение для рассылки в группах
BROADCAST_MESSAGE = "Продам данный тг аккаунт, отлега более 4 лет, есть подписки на разные боты для деанона (3 мес). Цена 3$"

@client.on(events.NewMessage(incoming=True))
async def handler(event):
    global auto_reply_enabled, broadcast_enabled

    # Проверяем ID отправителя
    sender_id = event.sender_id

    # Проверяем, заблокирован ли пользователь
    if sender_id in blocked_users:
        return  # Игнорируем сообщения от заблокированных пользователей

    # Если команда /chat от владельца
    if event.message.message == '/chat' and sender_id == OWNER_ID:
        auto_reply_enabled = True
        broadcast_enabled = False  # Отключаем рассылку
        await event.respond("Автоответчик для личных сообщений активирован!")
        return

    # Если команда /group от владельца
    if event.message.message == '/group' and sender_id == OWNER_ID:
        auto_reply_enabled = False
        broadcast_enabled = True  # Включаем рассылку
        await event.respond("Автоответчик отключен. Рассылка активирована!")
        return

    # Если это личные сообщения и автоответчик включен
    if event.is_private and auto_reply_enabled:
        current_time = time.time()

        # Проверка на спам
        if sender_id not in user_messages:
            user_messages[sender_id] = []

        # Добавляем текущее сообщение в список
        user_messages[sender_id].append(current_time)

        # Удаляем старые сообщения из списка
        user_messages[sender_id] = [msg for msg in user_messages[sender_id] if current_time - msg < TIME_WINDOW_PRIVATE]

        # Проверяем количество сообщений
        if len(user_messages[sender_id]) > MESSAGE_LIMIT:
            blocked_users[sender_id] = current_time + BLOCK_TIME
            await event.respond("Вы заблокированы за спам. Попробуйте позже.")
            return

        # Автоответ
        await event.respond("Вас приветствует Кристалл. Если не отвечаю, значит занят. Просьба не спамить!")

    # Рассылка в группах
    if event.is_group and broadcast_enabled:
        # Раз в 70 секунд отправляем сообщение
        while broadcast_enabled:
            await event.respond(BROADCAST_MESSAGE)
            await asyncio.sleep(70)

async def main():
    await client.start()
    print("Бот запущен и готов к работе!")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
