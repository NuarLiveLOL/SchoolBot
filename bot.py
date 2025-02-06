import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Настройки
TOKEN = '7511733020:AAHTjBOd87NB8awXCH6OUHGAHqFGZ0QPWuI'  # Замените на ваш токен
ADMIN_ID = 5492942922  # Замените на ваш ID администратора
PING_URL = 'https://your-url.onrender.com'  # Замените на ваш URL

if not TOKEN or not ADMIN_ID or not PING_URL:
    print("Ошибка: не указан TOKEN, ADMIN_ID или PING_URL.")
    exit(1)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для отправки самопинга
async def self_ping():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(PING_URL) as response:
                if response.status == 200:
                    logging.info('Self-ping successful!')
                else:
                    logging.error(f'Self-ping failed with status code {response.status}')
        except Exception as e:
            logging.error(f'Error during self-ping: {e}')

# Планировщик для самопинга каждые 5 минут
scheduler = AsyncIOScheduler()

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Я бот с самопингом.")

# Запуск бота
async def main():
    logging.basicConfig(level=logging.INFO)
    print("Бот работает!")

# Запуск планировщика
    scheduler.add_job(self_ping, 'interval', minutes=5)
    scheduler.start()
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем бота
