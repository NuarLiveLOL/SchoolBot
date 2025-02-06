import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import aiohttp
from aiohttp import ClientSession

TOKEN = '7511733020:AAHTjBOd87NB8awXCH6OUHGAHqFGZ0QPWuI'
WEBHOOK_URL = 'https://yourapp.onrender.com/webhook'  # Замените на свой URL
PORT = 8443  # Например, порт для Render

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Установка webhook
async def set_webhook():
    webhook = await bot.set_webhook(WEBHOOK_URL)
    if webhook:
        logging.info(f"Webhook установлен на {WEBHOOK_URL}")
    else:
        logging.error("Ошибка установки webhook!")

# Самопинг
async def self_ping():
    async with ClientSession() as session:
        try:
            async with session.get(WEBHOOK_URL) as response:
                if response.status == 200:
                    logging.info("Self-ping успешен!")
                else:
                    logging.error(f"Self-ping не удался с кодом {response.status}")
        except Exception as e:
            logging.error(f"Ошибка во время самопинга: {e}")

# Планировщик для самопинга каждые 5 минут
scheduler = AsyncIOScheduler()
scheduler.add_job(self_ping, 'interval', minutes=5)  # Пинг раз в 5 минут

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот с активным webhook.")

# Запуск бота с webhook
async def on_start():
    # Устанавливаем webhook и запускаем планировщик
    await set_webhook()
    scheduler.start()

# Запуск приложения
if __name__ == '__main__':
    from aiohttp import web

    # Определяем путь для webhook
    async def handle(request):
        update = await request.json()
        await dp.process_update(types.Update.to_object(update))
        return web.Response(status=200)

    app = web.Application()
    app.router.add_post('/webhook', handle)

    # Запуск aiohttp веб-сервера
    web.run_app(app, host='0.0.0.0', port=PORT)
