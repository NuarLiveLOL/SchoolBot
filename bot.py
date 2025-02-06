import asyncio
import os
import signal
import sys
import subprocess
from flask import Flask
from threading import Thread
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv

# Загрузка .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

if not TOKEN or not ADMIN_ID:
    print("Ошибка: не указан TOKEN или ADMIN_ID в .env")
    exit(1)

ADMIN_ID = int(ADMIN_ID)

# Создаем Flask сервер для Render
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Бот работает и поддерживается Flask!"

def run_flask():
    app.run(host="0.0.0.0", port=5000, debug=False, use_reloader=False)

# Функция для остановки всех старых процессов бота перед запуском нового
def kill_old_sessions():
    try:
        print("🛑 Завершаем старые сессии бота...")
        subprocess.run(["pkill", "-f", "bot.py"])  # Убивает все запущенные копии
        print("✅ Старые сессии остановлены!")
    except Exception as e:
        print(f"⚠ Ошибка при завершении старых сессий: {e}")

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Храним список подключенных ПК
connected_pcs = {}

# Флаг работы бота
running = True

# Функция для завершения бота корректно
async def shutdown():
    global running
    running = False
    print("🛑 Остановка бота...")
    await bot.session.close()  # Закрываем сессию бота
    sys.exit(0)

# Обработчик завершения процесса (CTRL+C, kill)
def stop_handler(signum, frame):
    asyncio.create_task(shutdown())

signal.signal(signal.SIGTERM, stop_handler)
signal.signal(signal.SIGINT, stop_handler)

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Используйте /connect, чтобы подключиться.")

# Команда /connect — подключение ПК
@dp.message(Command("connect"))
async def connect_pc(message: Message):
    pc_id = str(message.from_user.id)

    if pc_id in connected_pcs:
        return await message.reply(f"Этот ПК уже подключен как {connected_pcs[pc_id]}.")

    args = message.text.split(maxsplit=1)
    pc_name = args[1] if len(args) > 1 else f"PC_{pc_id}"
    connected_pcs[pc_id] = pc_name
    await message.reply(f"ПК {pc_name} ({pc_id}) успешно подключен!")

# Команда /list — список ПК
@dp.message(Command("list"))
async def list_pcs(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("Нет доступа.")

    if not connected_pcs:
        return await message.reply("Нет подключенных ПК.")

    text = "Подключенные ПК:\n" + "\n".join(f"{pc_name} (ID: {pc})" for pc, pc_name in connected_pcs.items())
    await message.reply(text)

# Запуск бота
async def main():
    print("✅ Бот работает!")

    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старые обновления
    await dp.start_polling(bot)


if __name__ == "__main__":
    kill_old_sessions()  # Завершаем старые сессии перед запуском новой
    flask_thread = Thread(target=run_flask)
    flask_thread.start()
    asyncio.run(main())
