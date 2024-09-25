import asyncio
import logging
from telethon import TelegramClient, events

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Вставьте свои данные здесь
api_id = 23169896  # Ваш API ID
api_hash = 'c83d7ac378acfd5d69c2cf2e9b121e7f'  # Ваш API Hash
phone = '+77766349341'  # Ваш номер телефона

client = TelegramClient('session_name', api_id, api_hash)

# Ключевые слова для фильтрации
keywords = ["номер", "физ", "физуха", "сап", "ку", "привет", "салам", "цена"]

# Автоответное сообщение
auto_reply_message = "Вас приветствует Кристалл, за меня отвечает автоответчик. Если не отвечаю, значит занят/сплю/нахожусь в личной зоне. Просьба не спамить!"

@client.on(events.NewMessage(incoming=True))
async def my_event_handler(event):
    # Проверяем, что это личный чат
    if event.is_private:
        message_text = event.message.message.lower()  # Приводим к нижнему регистру для проверки
        logger.info(f"Получено сообщение от {event.sender_id}: {message_text}")
        
        # Проверяем наличие ключевых слов в сообщении
        if any(keyword in message_text for keyword in keywords):
            await event.respond(auto_reply_message)
            logger.info(f"Ответ отправлен пользователю {event.sender_id}")

async def main():
    await client.start()
    logger.info("Автоответчик запущен!")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
