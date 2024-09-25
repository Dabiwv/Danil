import asyncio
from telethon import TelegramClient
from telethon.errors import ChatAdminRequiredError, UserIdInvalidError

# Вставьте свои данные здесь
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone_number = '+77766349341'  # Ваш номер телефона

# Создаем клиент
client = TelegramClient('group_leaver', api_id, api_hash)

async def leave_chat(chat):
    try:
        await client(LeaveChannelRequest(chat))
        print(f"Успешно вышел из беседы: {chat.title} ({chat.id})")
    except ChatAdminRequiredError:
        print(f"Нет прав администратора для выхода из беседы: {chat.title} ({chat.id}).")
    except UserIdInvalidError:
        print(f"Недопустимый ID для чата: {chat.title} ({chat.id}).")
    except Exception as e:
        print(f"Ошибка при выходе из беседы: {chat.title} ({chat.id}): {e}")

async def main():
    await client.start()

    # Запрос ссылок на группы
    chat_links = input("Пожалуйста, введите сюда ссылки на группы, из которых вы хотите выйти (разделяйте запятыми): ")
    chat_links = chat_links.split(',')

    # Удаление чатов
    tasks = []
    for link in chat_links:
        try:
            chat = await client.get_entity(link.strip())
            tasks.append(leave_chat(chat))
        except Exception as e:
            print(f"Ошибка при получении чата по ссылке {link.strip()}: {e}")

    await asyncio.gather(*tasks)

# Запуск основного метода
with client:
    client.loop.run_until_complete(main())
