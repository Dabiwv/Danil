import time
import asyncio
from telethon import TelegramClient

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+77766349341'

# Создаем клиент Telethon
client = TelegramClient('reporter', api_id, api_hash)

async def send_report(user_id):
    try:
        # Отправляем жалобу на пользователя
        await client.send_message('Telegram', f'Пожалуйста, рассмотрите жалобу на пользователя с ID {user_id}.')
        print(f"Жалоба на пользователя {user_id} отправлена.")
    except Exception as e:
        print(f"Ошибка при отправке жалобы: {e}")

async def main():
    await client.start()
    print("Бот запущен и готов к работе!")

    while True:
        user_id = input("Введите ID пользователя для отправки жалобы: ")
        await send_report(user_id)
        await asyncio.sleep(5)  # Интервал между отправкой жалоб (5 секунд)

with client:
    client.loop.run_until_complete(main())# Запуск клиента
if __name__ == "__main__":
    asyncio.run(main())
