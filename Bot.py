import asyncio
from telethon import TelegramClient, events

# Вставьте свои данные здесь
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone_number = '+77766349341'  # Ваш номер телефона

# Создаем клиент
client = TelegramClient('auto_responder', api_id, api_hash)

# Сообщение автоответчика
auto_reply_message = (
    "Вас приветствует Кристалл, за меня отвечает автоответчик. "
    "Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. Просьба не спамить!"
)

@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    # Проверка, что вы не в сети
    if not (await client.get_me()).status == "online":
        # Проверка, что сообщение пришло в личном чате
        if event.is_private:
            await event.reply(auto_reply_message)

async def main():
    await client.start()
    print("Автоответчик запущен...")

    # Держим клиент активным
    await client.run_until_disconnected()

# Запуск основного метода
with client:
    client.loop.run_until_complete(main())            print(f"Ошибка при получении чата по ссылке {link.strip()}: {e}")

    await asyncio.gather(*tasks)

# Запуск основного метода
with client:
    client.loop.run_until_complete(main())
