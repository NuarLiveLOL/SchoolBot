import logging
import aiohttp
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler

API_TOKEN = '7511733020:AAHTjBOd87NB8awXCH6OUHGAHqFGZ0QPWuI'  # Замените на ваш токен
PING_URL = 'https://schoolbot-x1xt.onrender.com'  # Замените на URL вашего приложения на Render

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

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
scheduler.add_job(self_ping, 'interval', minutes=5)
scheduler.start()

# Обработка команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я Telegram-бот.")

# Обработка команды /help
@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply("Вот как я могу помочь!")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler.start())  # Запуск планировщика
    executor.start_polling(dp, skip_updates=True)
