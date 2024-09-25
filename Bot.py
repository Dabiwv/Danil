import time
from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError

# Вставьте свои данные здесь
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone_number = '+77766349341'  # Ваш номер телефона

# Создаем клиент
client = TelegramClient('auto_sender', api_id, api_hash)

# Сообщение для рассылки
message = "Сделаю вам авторассылку. За вас будет делать бот, чтоб не было бана, рассылка будет происходить около 10 минут по всем беседам и чатам. Цена 3$"

async def send_message(chat):
    try:
        await client.send_message(chat, message)
        print(f"Сообщение отправлено в беседу: {chat.title} ({chat.id})")
    except ChatAdminRequiredError:
        print(f"Нет прав администратора для отправки сообщения в беседу: {chat.title} ({chat.id}). Пропуск...")
    except Exception as e:
        print(f"Ошибка при отправке сообщения в беседу: {chat.title} ({chat.id}): {e}")

async def main():
    await client.start()

    # Получаем список всех чатов
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        # Проверяем, является ли диалог беседой или общим чатом
        if dialog.is_group or dialog.is_channel:  # Проверяем на группы или каналы
            await send_message(dialog.entity)

            # Ожидание 4 минуты между отправками
            wait_time = 240  # 240 секунд = 4 минуты
            print(f"Ожидание {wait_time // 60} минут перед следующей отправкой...")
            time.sleep(wait_time)

# Запуск основного метода
with client:
    client.loop.run_until_complete(main())
