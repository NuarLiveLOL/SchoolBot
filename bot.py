import os
import asyncio
import requests
import threading
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from flask import Flask

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

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Используйте /connect, чтобы подключиться.")

# Команда /connect
@dp.message(Command("connect"))
async def connect_pc(message: Message):
    pc_id = str(message.from_user.id)

    if pc_id in connected_pcs:
        return await message.reply(f"Этот ПК уже подключен как {connected_pcs[pc_id]}.")

    args = message.text.split(maxsplit=1)
    pc_name = args[1] if len(args) > 1 else f"PC_{pc_id}"

    connected_pcs[pc_id] = pc_name
    await message.reply(f"ПК {pc_name} ({pc_id}) успешно подключен!")

# Команда /list
@dp.message(Command("list"))
async def list_pcs(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("Нет доступа.")

    if not connected_pcs:
        return await message.reply("Нет подключенных ПК.")

    text = "Подключенные ПК:\n" + "\n".join(
        f"{pc_name} (ID: {pc})" for pc, pc_name in connected_pcs.items()
    )
    await message.reply(text)

# 🔥 Поддержание активности Render через HTTP-запросы 🔥
app = Flask(__name__)

@app.route("/")
def home():
    return "Бот работает!"

def run_flask():
    app.run(host="0.0.0.0", port=10000)

# 🔥 Периодический запрос на сервер погоды 🔥
async def keep_alive():
    while True:
        try:
            requests.get("https://api.weatherapi.com/v1/current.json?key=8428519cf2904ddaae4123314250602&q=London")
            print("Keep-alive запрос отправлен!")
        except Exception as e:
            print(f"Ошибка Keep-alive: {e}")
        await asyncio.sleep(300)  # Запрос каждые 5 минут

# 🔥 Запуск бота и Flask в одном потоке 🔥
async def main():
    threading.Thread(target=run_flask, daemon=True).start()
    asyncio.create_task(keep_alive())
    print("Бот запущен!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
