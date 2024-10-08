import time
import asyncio
from telethon import TelegramClient, events
import logging

# Входные данные для вашего аккаунта
api_id = '17086106'
api_hash = '1bb38ac13a669b310a3546f46e310459'
phone_number = '+7 776 5139878'

# Уникальный ID тебя (владельца)
your_id =5117600561   # Твой ID

# Создаем клиент Telethon
client = TelegramClient('auto_responder', api_id, api_hash)

# Переменные для активации автоответчика
auto_responder_private = False  # Для личных сообщений
auto_responder_group = False  # Для групп
last_group_message_time = {}  # Для отслеживания времени последнего сообщения в группах

# Логирование
logging.basicConfig(filename='messages_log.txt', level=logging.INFO, format='%(asctime)s - %(message)s')

# Функция для записи логов
def log_message(event):
    logging.info(f"Сообщение от {event.sender_id}: {event.text}")

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
        if chat_id not in last_group_message_time or now - last_group_message_time[chat_id] >= 500:
            last_group_message_time[chat_id] = now  # Обновляем время последнего сообщения
            await event.reply("КУПЛЮ ММ2 ЗА ТЕНГЕ ОНЛИ МОЯ ДОВА ИЛИ ГАРАНТ

ТАК ЖЕ ИЩУ ФР КОРОВУ ИЛИ ЧЕРЕПАХУ")
        else:
            print(f"Сообщение пропущено для группы {chat_id}, так как прошло недостаточно времени с последнего сообщения.")

# Обрабатываем команды
@client.on(events.NewMessage)
async def handler(event):
    global auto_responder_private, auto_responder_group

    # Логирование каждого входящего сообщения
    log_message(event)

    # Только ты можешь вводить команды
    if event.sender_id == your_id:
        # Команда активации автоответчика для личных сообщений
        if event.text == '/chat' and event.is_private:
            auto_responder_private = True
            auto_responder_group = False  # Отключаем автоответчик для групп
            await event.reply("Автоответчик для личных чатов активирован!")
            print("Автоответчик для личных сообщений включен.")
        
        # Команда активации автоответчика для групп
        elif event.text == '/group' and event.is_group:
            auto_responder_group = True
            auto_responder_private = False  # Отключаем автоответчик для личных чатов
            await event.reply("Автоответчик для групп активирован!")
            print("Автоответчик для групп включен.")
        
        # Команда отключения автоответчика для личных сообщений
        elif event.text == '/stop_chat' and event.is_private:
            auto_responder_private = False
            await event.reply("Автоответчик для личных сообщений отключен.")
            print("Автоответчик для личных сообщений отключен.")
        
        # Команда отключения автоответчика для групп
        elif event.text == '/stop_group' and event.is_group:
            auto_responder_group = False
            await event.reply("Автоответчик для групп отключен.")
            print("Автоответчик для групп отключен.")
        return
    
    # Если автоответчик активен, запускаем его для личных чатов или групп
    if auto_responder_private:
        await auto_responder_private_chat(event)
    
    if auto_responder_group:
        await auto_responder_group_chat(event)

# Запуск клиента
with client:
    client.run_until_disconnected()
