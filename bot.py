import asyncio
import os
import signal
import sys
import subprocess
from flask import Flask, request
from threading import Thread
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook, SetWebhook
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    print("Ошибка: не указан TOKEN или ADMIN_ID в .env")
    exit(1)

ADMIN_ID = int(ADMIN_ID)

# Создаем Flask сервер
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает и поддерживается Flask!"

@app.route(f"/{TOKEN}", methods=["POST"])
async def webhook():
    update = Update(**request.get_json())
    await dp.feed_update(bot, update)
    return "OK", 200

# Запуск Flask в фоне
def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Завершаем старые сессии бота
def kill_old_sessions():
    try:
        print("🛑 Завершаем старые сессии бота...")
        subprocess.run(["pkill", "-f", "bot.py"], check=True)
        print("✅ Старые сессии остановлены!")
    except subprocess.CalledProcessError:
        print("⚠ Не найдено старых процессов.")

# Создаем бота и диспетчер
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

# Храним список подключенных ПК
connected_pcs = {}

# Глобальная переменная для управления потоком Flask
flask_thread = None

# Функция корректного завершения бота
async def shutdown():
    global flask_thread
    print("🛑 Остановка бота...")

    await bot.session.close()
    
    if flask_thread and flask_thread.is_alive():
        print("🛑 Остановка Flask...")
        flask_thread.join(timeout=5)  # Ждём завершения потока Flask
    sys.exit(0)

# Обработчик сигналов завершения
def stop_handler(signum, frame):
    loop = asyncio.get_event_loop()
    loop.create_task(shutdown())

signal.signal(signal.SIGTERM, stop_handler)
signal.signal(signal.SIGINT, stop_handler)

# Команда /start
@dp.message()
async def start(message):
    await message.reply("Привет! Используйте /connect, чтобы подключиться.")

# Команда /connect
@dp.message()
async def connect_pc(message):
    pc_id = str(message.from_user.id)

    if pc_id in connected_pcs:
        return await message.reply(f"Этот ПК уже подключен как {connected_pcs[pc_id]}.")

    args = message.text.split(maxsplit=1)
    pc_name = args[1] if len(args) > 1 else f"PC_{pc_id}"
    connected_pcs[pc_id] = pc_name
    await message.reply(f"ПК {pc_name} ({pc_id}) успешно подключен!")

# Команда /list
@dp.message()
async def list_pcs(message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("Нет доступа.")

    if not connected_pcs:
        return await message.reply("Нет подключенных ПК.")

    text = "Подключенные ПК:\n" + "\n".join(f"{pc_name} (ID: {pc})" for pc, pc_name in connected_pcs.items())
    await message.reply(text)

# Запуск бота
async def main():
    global flask_thread
    print("✅ Бот работает!")

    # Удаляем старые вебхуки
    await bot(DeleteWebhook(drop_pending_updates=True))

    # Устанавливаем новый вебхук
    webhook_url = f"https://your-app-name.onrender.com/{TOKEN}"
    await bot(SetWebhook(url=webhook_url))

    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=False)
    flask_thread.start()

if __name__ == "__main__":
    kill_old_sessions()  # Убиваем старые процессы
    asyncio.run(main())
