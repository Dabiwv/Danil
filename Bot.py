from telethon import TelegramClient, events

# Вставьте свои данные
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone_number = '+77766349341'  # Ваш номер телефона

# Создаем клиент
client = TelegramClient('session_name', api_id, api_hash)

@client.on(events.NewMessage())
async def handler(event):
    # Проверяем, что это сообщение не от бота
    if event.sender_id != (await client.get_me()).id:
        await event.reply("Данный человек пока не в сети, но вы можете позвонить ему.")

async def main():
    await client.start()
    print("Бот запущен...")
    await client.run_until_disconnected()

# Запуск клиента
with client:
    client.loop.run_until_complete(main())
