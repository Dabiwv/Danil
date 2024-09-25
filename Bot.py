import asyncio
from telethon import TelegramClient, events

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+7 776 6349341'

# Создаем клиент Telethon для вашего аккаунта
user_client = TelegramClient('user', api_id, api_hash)

# Токен вашего бота
bot_token = '6423641572:AAFx8dMJaahZBOgm8GRItFhkRlB3_vMa3c0'
bot_client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

async def send_report(username):
    try:
        user = await user_client.get_entity(username)  # Получаем пользователя по юзернейму
        await user_client.report_user(user.id, 'spam')  # Используем report_user
        print(f"Жалоба на пользователя {username} отправлена.")
    except Exception as e:
        print(f"Ошибка при отправке жалобы: {e}")

@bot_client.on(events.NewMessage(pattern='/report (.*)'))
async def report(event):
    username = event.pattern_match.group(1)  # Получаем юзернейм из команды
    await send_report(username)
    await event.respond(f"Жалоба на пользователя {username} отправлена.")

async def main():
    # Запускаем авторизацию пользователя
    await user_client.start(phone_number)
    
    # Проверяем авторизацию и запрашиваем код подтверждения, если нужно
    if not await user_client.is_user_authorized():
        phone_code = input('Введите код подтверждения, который пришел на ваш телефон: ')
        await user_client.sign_in(phone_number, phone_code)
    
    print("Авторизация пользователя прошла успешно!")
    
    # Ожидаем события от бота
    await bot_client.run_until_disconnected()

# Запускаем асинхронную функцию в основном блоке программы
with user_client:
    user_client.loop.run_until_complete(main())
