import asyncio
from telethon import TelegramClient, functions, types

# Входные данные для вашего аккаунта
api_id = '23169896'
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'
phone_number = '+7 776 6349341'

# Создаем клиент Telethon
client = TelegramClient('report_bot', api_id, api_hash)

async def main():
    await client.start()

    user_input = input("Введите ID или username пользователя, на которого хотите отправить жалобу: ")

    while True:
        try:
            # Получаем entity для пользователя
            user_entity = await client.get_input_entity(user_input)

            # Отправляем жалобу на пользователя
            await client(functions.messages.ReportRequest(
                peer=user_entity,  # Теперь user_input может быть ID или username
                id=[],  # Обычно можно оставить пустым для жалобы на весь чат
                reason=types.InputReportReasonSpam(),  # Тип жалобы (в данном случае - спам)
                message='Спам'  # Причина жалобы
            ))
            print(f"Жалоба на пользователя {user_input} отправлена!")
            
            # Ожидание перед отправкой следующей жалобы
            await asyncio.sleep(5)  # Отправка жалобы каждые 5 секунд

        except Exception as e:
            print(f"Ошибка при отправке жалобы: {e}")

# Запуск клиента
if __name__ == "__main__":
    asyncio.run(main())
