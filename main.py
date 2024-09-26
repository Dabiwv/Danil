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

# Переменные для активации автоответчика
auto_responder_private = False  # Для личных сообщений
auto_responder_group = False  # Для групп
last_group_message_time = {}  # Для отслеживания времени последнего сообщения в группах

# Функция для активации автоответчика в личных сообщениях
async def auto_responder_private_chat(event):
    if auto_responder_private and event.is_private:  # Проверяем, что это личный чат
        await event.reply("Вас приветствует Кристалл, за меня отвечает автоответчик. Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. Просьба не спамить!")

# Функция для активации автоответчика в группах
async def auto_responder_group_chat(event):
    global last_group_message_time
    if auto_responder_group and event.is_group:  # Проверяем, что это группа
        chat_id = event.chat_id
        now = time.time()
        
        # Проверяем, прошло ли достаточно времени с последнего сообщения (120 секунд)
        if chat_id not in last_group_message_time or now - last_group_message_time[chat_id] >= 120:
            last_group_message_time[chat_id] = now  # Обновляем время последнего сообщения
            await event.reply("Продам данный тг аккаунт, отлега более 4 лет, есть подписки на разные боты для деанона (3мес). Цена 3$")
        else:
            print(f"Сообщение пропущено для группы {chat_id}, так как прошло недостаточно времени с последнего сообщения.")

# Обрабатываем команды
@client.on(events.NewMessage)
async def handler(event):
    global auto_responder_private, auto_responder_group

    # Только ты можешь вводить команды
    if event.sender_id == your_id:
        # Команда активации автоответчика для личных сообщений
        if event.text == '/chat' and event.is_private:
            auto_responder_private = True
            auto_responder_group = False  # Отключаем автоответчик для групп
            await event.reply("Автоответчик для личных чатов активирован!")
        
        # Команда активации автоответчика для групп
        elif event.text == '/group' and event.is_group:
            auto_responder_group = True
            auto_responder_private = False  # Отключаем автоответчик для личных чатов
            await event.reply("Автоответчик для групп активирован!")
        return
    
    # Если автоответчик активен, запускаем его для личных чатов или групп
    if auto_responder_private:
        await auto_responder_private_chat(event)
    
    if auto_responder_group:
        await auto_responder_group_chat(event)

# Запуск клиента
with client:
    client.run_until_disconnected()
