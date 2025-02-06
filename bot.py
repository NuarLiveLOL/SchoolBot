import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv
from keep_alive import keep_alive  # Импортируем поддержку активности

# Загружаем .env
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

# Храним список подключенных ПК {telegram_id: pc_name}
connected_pcs = {}

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Используйте /connect, чтобы подключиться.")

@dp.message(Command("Nuar"))
async def start(message: Message):
    await message.reply("Тут был NuarLite")

# Команда /connect — подключение ПК
@dp.message(Command("connect"))
async def connect_pc(message: Message):
    pc_id = str(message.from_user.id)  # Telegram ID = ID ПК

    if pc_id in connected_pcs:
        return await message.reply(
            f"Этот ПК уже подключен как {connected_pcs[pc_id]}.")

    # Берем имя ПК из сообщения (если отправлено)
    args = message.text.split(maxsplit=1)
    pc_name = args[1] if len(
        args
    ) > 1 else f"PC_{pc_id}"  # Если имя не указано, даем ID по умолчанию

    connected_pcs[pc_id] = pc_name
    await message.reply(f"ПК {pc_name} ({pc_id}) успешно подключен!")

# Команда /list — список ПК
@dp.message(Command("list"))
async def list_pcs(message: Message):
    if message.from_user.id != ADMIN_ID:
        return await message.reply("Нет доступа.")

    if not connected_pcs:
        return await message.reply("Нет подключенных ПК.")

    text = "Подключенные ПК:\n" + "\n".join(
        f"{pc_name} (ID: {pc})" for pc, pc_name in connected_pcs.items())
    await message.reply(text)

# Запуск бота
async def main():
    keep_alive()  # Запуск Flask-сервера для поддержания активности
    print("✅ Бот работает и не отключается!")
    await bot.delete_webhook(drop_pending_updates=True)  # Удаляем старые запросы
    await dp.start_polling(bot)  # Запускаем Long Polling

if __name__ == "__main__":
    asyncio.run(main())  # Запускаем бота
