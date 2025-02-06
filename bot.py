import os
import asyncio
import requests
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message, Update
from aiogram.filters import Command
from dotenv import load_dotenv
from flask import Flask, request

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    print("Ошибка: не указан TOKEN или ADMIN_ID в .env")
    exit(1)

ADMIN_ID = int(ADMIN_ID)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Подключенные ПК
connected_pcs = {}

# Flask-сервер для Webhook
app = Flask(__name__)

# Главная страница (Render требует открытую страницу)
@app.route("/", methods=["GET"])
def home():
    return "Бот работает!"

# Webhook обработка сообщений
@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    try:
        data = request.json
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return "OK", 200
    except Exception as e:
        logging.error(f"Ошибка обработки Webhook: {e}")
        return "Internal Server Error", 500

# 🔥 Keep-Alive запросы 🔥
async def keep_alive():
    while True:
        try:
            requests.get("https://api.weatherapi.com/v1/current.json?key=8428519cf2904ddaae4123314250602&q=London")
            print("Keep-alive запрос отправлен!")
        except Exception as e:
            print(f"Ошибка Keep-alive: {e}")
        await asyncio.sleep(300)  # Запрос каждые 5 минут

# 🚀 Запуск бота 🚀
async def main():
    # Устанавливаем Webhook
    webhook_url = f"https://{os.getenv('RENDER_DOMAIN')}/{TOKEN}"
    await bot.set_webhook(webhook_url)

    # Запускаем Keep-Alive
    asyncio.create_task(keep_alive())

    # Запускаем Flask
    app.run(host="0.0.0.0", port=10000)

if __name__ == "__main__":
    asyncio.run(main())
