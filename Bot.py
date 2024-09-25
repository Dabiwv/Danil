import time
import asyncio
from telethon import TelegramClient, events

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+7 776 6349341'

# Создаем клиент Telethon
client = TelegramClient('auto_responder', api_id, api_hash)

# Параметры автоответчика
auto_reply_message = "Вас приветствует Кристалл, за меня отвечает автоответчик. Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. Просьба не спамить!"

# Переменные для контроля режима
chat_mode = False
group_mode = False
last_group_reply_time = 0  # Время последнего сообщения в группах

# Обработчик команды /chat (личные чаты)
@client.on(events.NewMessage(pattern='/chat'))
async def activate_chat_mode(event):
    global chat_mode, group_mode
    chat_mode = True
    group_mode = False
    await event.reply("Автоответчик для личных чатов активирован!")

# Обработчик команды /group (группы)
@client.on(events.NewMessage(pattern='/group'))
async def activate_group_mode(event):
    global group_mode, chat_mode
    group_mode = True
    chat_mode = False
    await event.reply("Автоответчик для групп активирован! Интервал между сообщениями: 20 секунд.")

# Обработчик входящих сообщений
@client.on(events.NewMessage)
async def auto_responder(event):
    global chat_mode, group_mode, last_group_reply_time
    
    # Игнорировать ботов и свои сообщения
    if event.is_private and chat_mode and not event.is_bot and event.sender_id != (await client.get_me()).id:
        await event.reply(auto_reply_message)
    
    # Отвечать только в группах при активном group_mode
    elif event.is_group and group_mode:
        current_time = time.time()
        if current_time - last_group_reply_time >= 20:  # Проверка интервала 20 секунд
            await event.reply(auto_reply_message)
            last_group_reply_time = current_time

async def main():
    await client.start(phone=phone_number)
    print("Бот запущен...")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
