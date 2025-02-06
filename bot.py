import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = '8043275462:AAH7nY9QOojLTutdI_yIs7fn6G_H-gmLsmA'
ALLOWED_DEVICES = ['PC_001', 'PC_002', 'PC_003']  # Список разрешенных устройств
ADMIN_ID = 5492942922  # ID администратора

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    if message.from_user.id == ADMIN_ID:  # ID администратора
        await message.reply("Привет! Используйте /connect <DEVICE_ID>, чтобы подключиться.")
    else:
        await message.reply("У вас нет прав для использования этой команды.")

# Команда для подключения устройства
@dp.message(Command("connect"))
async def connect(message: Message):
    if message.from_user.id == ADMIN_ID:  # Проверка прав администратора
        device_id = message.get_args()
        if device_id in ALLOWED_DEVICES:
            await message.reply(f"Устройство {device_id} подключено.")
        else:
            await message.reply(f"Устройство с ID {device_id} не найдено или не имеет доступа.")
    else:
        await message.reply("У вас нет прав для выполнения этой команды.")

# Команда для открытия блокнота
@dp.message(Command("open_txt"))
async def open_txt(message: Message):
    if message.from_user.id == ADMIN_ID:  # Проверка прав администратора
        device_id = message.get_args()
        if device_id in ALLOWED_DEVICES:
            # Отправляем команду на соответствующий клиент
            await message.reply(f"Команда на открытие блокнота отправлена устройству {device_id}.")
            # Здесь можно добавить логику для отправки команды на устройство, чтобы оно открыло блокнот
        else:
            await message.reply(f"Устройство с ID {device_id} не найдено или не имеет доступа.")
    else:
        await message.reply("У вас нет прав для выполнения этой команды.")

# Запуск бота
async def main():
    print("Бот работает!")
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        pass
    finally:
        await bot.close()
        print("Бот завершил свою работу!")

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Запускаем бота
    except KeyboardInterrupt:
        print("Бот завершен вручную.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
