import asyncio
from telethon import TelegramClient, events

# Вставьте свои данные здесь
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone = '+77766349341'  # Ваш номер телефона

client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    # Проверяем, что это личный чат
    if event.is_private:
        await event.respond("Вас приветствует Кристалл, за меня отвечает автоответчик. "
                            "Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. "
                            "Просьба не спамить!")

async def main():
    await client.start()
    print("Автоответчик запущен!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
