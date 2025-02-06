import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = '8043275462:AAH7nY9QOojLTutdI_yIs7fn6G_H-gmLsmA'

# Создаем бота и диспетчер
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Используйте /connect, чтобы подключиться.")

# Команда /stop для завершения работы бота
@dp.message(Command("stop"))
async def stop(message: Message):
    await message.reply("Бот завершает свою работу...")
    # Останавливаем polling и закрываем соединение с ботом
    await dp.stop_polling()
    await bot.close()

# Запуск бота
async def main():
    print("Бот работает!")
    try:
        # Запускаем polling
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        # Закрываем соединение с ботом, если он был открыт
        await bot.close()
        print("Бот завершил свою работу!")

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Запускаем бота
    except KeyboardInterrupt:
        print("Бот завершен вручную.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
