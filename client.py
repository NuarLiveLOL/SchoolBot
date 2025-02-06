import asyncio
import os
import sys
import time
from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import Command
import psutil
import subprocess

TOKEN = '7120106958:AAF02qF_yExYRenX4ypPd6F5f5fWTIVdTT0'
DEVICE_ID = 'PC_001'  # Уникальный ID устройства
ADMIN_ID = 5492942922  # ID администратора бота (для авторизации)

bot = Bot(token=TOKEN)

# Функция для проверки подключения к боту
async def connect_to_bot():
    while True:
        try:
            # Отправляем команду на подключение устройства
            await bot.send_message(ADMIN_ID, f"/connect {DEVICE_ID}")
            print(f"Устройство {DEVICE_ID} подключено.")
            break
        except Exception as e:
            print(f"Ошибка подключения: {e}. Повторная попытка...")
            time.sleep(5)

# Функция для выполнения команд (например, открытия блокнота)
async def execute_command(command: str):
    if command == "open_txt":
        subprocess.run("notepad.exe")  # Открыть блокнот (на Windows)
    # Добавьте другие команды по аналогии, например, для других программ

# Получение и обработка команд от бота
async def listen_for_commands():
    while True:
        try:
            # Слушаем сообщения от бота
            @dp.message(Command())
            async def handle_message(message: Message):
                if message.text.startswith("/open_txt"):
                    await execute_command("open_txt")
                    await message.reply(f"Команда {message.text} выполнена на устройстве {DEVICE_ID}.")
                else:
                    await message.reply(f"Неизвестная команда {message.text}.")

            await dp.start_polling()  # Запускаем прослушивание сообщений от бота

        except Exception as e:
            print(f"Ошибка при обработке команды: {e}. Повторная попытка...")
            time.sleep(5)

# Основная функция
async def main():
    await connect_to_bot()  # Подключаем устройство к боту
    await listen_for_commands()  # Ожидаем команд от бота

if __name__ == "__main__":
    try:
        asyncio.run(main())  # Запускаем клиента
    except KeyboardInterrupt:
        print("Клиент завершен вручную.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
