import asyncio
import platform
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command

TOKEN = '7120106958:AAF02qF_yExYRenX4ypPd6F5f5fWTIVdTT0'
ALLOWED_DEVICES = ['PC_001', 'PC_002', 'PC_003']  # Список разрешенных устройств

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Настройка логирования
logging.basicConfig(filename='bot_log.txt', level=logging.INFO)

def log_bot_start():
    system_info = platform.uname()
    ip_address = get_ip_address()
    logging.info(f"Бот запущен на {system_info.system} ({system_info.node}) с IP {ip_address}")
    logging.info(f"Архитектура: {system_info.machine}, Процессор: {system_info.processor}")
    logging.info(f"Дата и время запуска: {logging.Formatter('%(asctime)s').format(logging.LogRecord('', '', '', '', '', '', ''))}")

def get_ip_address():
    import socket
    ip_address = socket.gethostbyname(socket.gethostname())
    return ip_address

# Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Используйте /connect <DEVICE_ID>, чтобы подключиться.")

# Команда для подключения устройства
@dp.message(Command("connect"))
async def connect(message: Message):
    device_id = message.get_args()
    if device_id in ALLOWED_DEVICES:
        await message.reply(f"Устройство {device_id} подключено.")
    else:
        await message.reply(f"Устройство с ID {device_id} не найдено или не имеет доступа.")

# Команда для открытия блокнота
@dp.message(Command("open_txt"))
async def open_txt(message: Message):
    device_id = message.get_args()
    if device_id in ALLOWED_DEVICES:
        # Отправляем команду на соответствующий клиент
        await message.reply(f"Команда на открытие блокнота отправлена устройству {device_id}.")
        # Здесь можно добавить логику для отправки команды на устройство, чтобы оно открыло блокнот
    else:
        await message.reply(f"Устройство с ID {device_id} не найдено или не имеет доступа.")

# Запуск бота
async def main():
    log_bot_start()  # Логируем запуск бота
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
