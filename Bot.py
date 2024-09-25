import time
import random
from telethon import TelegramClient

# Вставьте свои данные здесь
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone_number = '+77766349341'  # Ваш номер телефона

# Создаем клиент
client = TelegramClient('auto_sender', api_id, api_hash)

# Сообщение для рассылки
message = "Сделаю вам авторассылку. За вас будет делать бот, чтоб не было бана, рассылка будет происходить около 5-15 минут по всем каналам, беседам, чатам. Цена 3$"

async def send_message(chat):
    await client.send_message(chat, message)
    print(f"Сообщение отправлено в {chat.title} ({chat.id})")

async def main():
    await client.start()

    # Получаем список всех чатов
    dialogs = await client.get_dialogs()
    num_dialogs = len(dialogs)

    if num_dialogs == 0:
        print("Нет доступных чатов для рассылки.")
        return

    for dialog in dialogs:
        # Проверяем, является ли диалог группой или каналом
        if dialog.is_group or dialog.is_channel:
            # Отправляем сообщение в чат
            await send_message(dialog.entity)

            # Ожидание 10 минут между отправками
            wait_time = 600  # 600 секунд = 10 минут
            print(f"Ожидание {wait_time // 60} минут перед следующей отправкой...")
            time.sleep(wait_time)

# Запуск основного метода
with client:
    client.loop.run_until_complete(main())
