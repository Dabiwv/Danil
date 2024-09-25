import time
import asyncio
from telethon import TelegramClient, events

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+7 776 6349341'

# Создаем клиент Telethon для вашего аккаунта
user_client = TelegramClient('user', api_id, api_hash)

# Токен вашего бота
bot_token = '7058388588:AAHWd-c2BEmG8penT2VXGxveMg-tftPeJWs'
bot_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def send_report(user_id):
    try:
        user = await user_client.get_entity(user_id)
        await user_client.report(user, 'spam')
        print(f"Жалоба на пользователя {user_id} отправлена.")
    except Exception as e:
        print(f"Ошибка при отправке жалобы: {e}")

@bot_client.on(events.NewMessage(pattern='/report (.*)'))
async def report(event):
    user_id = event.pattern_match.group(1)
    await send_report(user_id)
    await event.respond(f"Жалоба на пользователя {user_id} отправлена.")

async def main():
    await user_client.start(phone_number)
    
    # Если требуется код подтверждения
    if not await user_client.is_user_authorized():
        phone_code = input('Введите код подтверждения, который пришел на ваш телефон: ')
        await user_client.sign_in(phone_number, phone_code)
    
    print("Авторизация пользователя прошла успешно!")
    
    await bot_client.run_until_disconnected()

with user_client:
    user_client.loop.run_until_complete(main())        user_id = input("Введите ID пользователя для отправки жалобы: ")
        await send_report(user_id)
        await asyncio.sleep(5)  # Интервал между отправкой жалоб (5 секунд)

with client:
    client.loop.run_until_complete(main())
