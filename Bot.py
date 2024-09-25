import time
import asyncio
from telethon import TelegramClient, events

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+7 776 6349341'

# Уникальный ID тебя (владельца)
your_id = 1694921116  # Твой ID

# Создаем клиент Telethon
client = TelegramClient('auto_responder', api_id, api_hash)

# Параметры антиспама
MESSAGE_LIMIT = 6  # Максимум сообщений
TIME_WINDOW = 60  # Интервал в секундах для спама
BLOCK_TIME = 1800  # Время блокировки пользователя (30 минут)

# Словарь для отслеживания сообщений пользователей
user_messages = {}
blocked_users = {}

# Переменные для активации автоответчика
auto_responder_active = False

# Функция для активации автоответчика
async def auto_responder(event):
    global auto_responder_active
    if auto_responder_active:
        await event.reply("Вас приветствует Кристалл, за меня отвечает автоответчик. Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. Просьба не спамить!")

# Антиспам система
async def check_spam(event):
    user_id = event.sender_id
    now = time.time()
    
    if user_id in blocked_users and now < blocked_users[user_id]:
        return False  # Пользователь заблокирован
    
    if user_id not in user_messages:
        user_messages[user_id] = []
    
    user_messages[user_id].append(now)
    
    # Удаляем старые сообщения
    user_messages[user_id] = [t for t in user_messages[user_id] if now - t < TIME_WINDOW]
    
    if len(user_messages[user_id]) > MESSAGE_LIMIT:
        blocked_users[user_id] = now + BLOCK_TIME
        await event.reply("Вы заблокированы за спам.")
        return False
    
    return True

# Обрабатываем сообщения
@client.on(events.NewMessage)
async def handler(event):
    global auto_responder_active
    
    # Только ты можешь вводить команды
    if event.sender_id == your_id:
        # Команда активации автоответчика
        if event.text == '/chat':
            auto_responder_active = True
            await event.reply("Автоответчик для личных чатов активирован!")
        elif event.text == '/group':
            await event.reply("Режим автоответчика для групп активирован!")
        return
    
    # Если автоответчик активирован, проверяем на спам
    if auto_responder_active:
        if await check_spam(event):
            await auto_responder(event)

# Запуск клиента
with client:
    client.run_until_disconnected()
