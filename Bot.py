import time
import asyncio
from telethon import TelegramClient

# Входные данные для вашего аккаунта
api_id = '23169896'  # Замените на ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Замените на ваш API Hash
phone_number = '+77766349341'  # Замените на ваш номер телефона без пробелов

# Создаем клиент Telethon
client = TelegramClient('reporter', api_id, api_hash)

async def send_report(user_id):
    try:
        await client.report_user(user_id, 'spam')  # Отправка жалобы
        print(f"Жалоба на пользователя {user_id} отправлена.")
    except Exception as e:
        print(f"Ошибка при отправке жалобы: {e}")

async def main():
    await client.start(phone_number)
    
    # Если требуется код подтверждения
    if not await client.is_user_authorized():
        phone_code = input('Введите код подтверждения, который пришел на ваш телефон: ')
        await client.sign_in(phone_number, phone_code)
    
    print("Авторизация прошла успешно!")

    while True:
        user_id = input("Введите ID пользователя для отправки жалобы: ")
        await send_report(user_id)
        await asyncio.sleep(5)  # Интервал между отправкой жалоб (5 секунд)

with client:
    client.loop.run_until_complete(main())
