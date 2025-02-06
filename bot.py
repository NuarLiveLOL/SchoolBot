import os
import asyncio
import requests
import logging
import threading
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
RENDER_DOMAIN = os.getenv("RENDER_DOMAIN")

if not TOKEN or not ADMIN_ID or not RENDER_DOMAIN:
    print("Ошибка: не указан TOKEN, ADMIN_ID или RENDER_DOMAIN в .env")
    exit(1)

ADMIN_ID = int(ADMIN_ID)

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Flask-сервер для Webhook
app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Бот работает!"

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

# 🔥 Keep-Alive процесс 🔥
def keep_alive():
    while True:
        try:
            requests.get("https://api.weatherapi.com/v1/current.json?key=8428519cf2904ddaae4123314250602&q=London")
            print("Keep-alive запрос отправлен!")
        except Exception as e:
            print(f"Ошибка Keep-alive: {e}")
        asyncio.run(asyncio.sleep(300))  # Запрос каждые 5 минут

# 🚀 **КОМАНДЫ БОТА** 🚀

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Привет! Я твой игровой бот. Введи /help, чтобы узнать команды.")

@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer("🎮 Доступные команды:\n"
                         "/start - Начать\n"
                         "/game - Начать игру\n"
                         "/coin - Подбросить монету\n"
                         "/dice - Кинуть кубик\n"
                         "/weather - Узнать погоду")

@dp.message(Command("game"))
async def game_cmd(message: Message):
    await message.answer("🕹 Начинаем игру! Введи команду /dice или /coin.")

@dp.message(Command("coin"))
async def coin_cmd(message: Message):
    result = "Орел" if os.urandom(1)[0] % 2 == 0 else "Решка"
    await message.answer(f"🪙 Монета упала на {result}!")

@dp.message(Command("dice"))
async def dice_cmd(message: Message):
    dice_roll = (os.urandom(1)[0] % 6) + 1
    await message.answer(f"🎲 Ты выбросил {dice_roll}!")

@dp.message(Command("weather"))
async def weather_cmd(message: Message):
    try:
        response = requests.get("https://api.weatherapi.com/v1/current.json?key=8428519cf2904ddaae4123314250602&q=London")
        data = response.json()
        temp = data["current"]["temp_c"]
        condition = data["current"]["condition"]["text"]
        await message.answer(f"🌦 Погода в Лондоне: {temp}°C, {condition}")
    except Exception as e:
        await message.answer("Ошибка при получении погоды.")

# 🚀 **Запуск бота** 🚀
async def main():
    # Устанавливаем Webhook
    webhook_url = f"https://{RENDER_DOMAIN}/{TOKEN}"
    await bot.set_webhook(webhook_url)

    # Запускаем Keep-Alive в отдельном потоке
    threading.Thread(target=keep_alive, daemon=True).start()

    # Запускаем Flask в фоне
    app.run(host="0.0.0.0", port=10000, threaded=True)

if __name__ == "__main__":
    asyncio.run(main())
