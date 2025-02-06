import os
import asyncio
import random
import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from dotenv import load_dotenv 

# Загружаем .env
load_dotenv()
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    print("Ошибка: не указан TOKEN в .env")
    exit(1)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 📌 Функция keep-alive (пингует API, чтобы Render не отключил бота)
async def keep_alive():
    while True:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London") as response:
                    data = await response.json()
                    print(f"Keep-alive: Температура в Лондоне {data['current']['temp_c']}°C")
        except Exception as e:
            print("Keep-alive ошибка:", e)

        await asyncio.sleep(60)  # Пинг каждую минуту

# 📌 Команда /start
@dp.message(Command("start"))
async def start(message: Message):
    await message.reply("Привет! Я игровой бот 🤖. Используй /help, чтобы узнать мои команды!")

# 📌 Команда /help
@dp.message(Command("help"))
async def help_cmd(message: Message):
    text = "🎮 Команды бота:\n"
    text += "/coin – Подбросить монетку 🪙\n"
    text += "/dice – Бросить кости 🎲\n"
    text += "/weather – Погода в Лондоне 🌦\n"
    text += "/joke – Случайная шутка 😂\n"
    await message.reply(text)

# 📌 Команда /coin – Монетка
@dp.message(Command("coin"))
async def coin(message: Message):
    result = random.choice(["Орёл 🦅", "Решка 🎭"])
    await message.reply(f"Монетка подброшена: {result}")

# 📌 Команда /dice – Кости 🎲
@dp.message(Command("dice"))
async def dice(message: Message):
    result = random.randint(1, 6)
    await message.reply(f"🎲 Вы бросили кости: {result}")

# 📌 Команда /weather – Запрос погоды
@dp.message(Command("weather"))
async def weather(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.weatherapi.com/v1/current.json?key=YOUR_API_KEY&q=London") as response:
                data = await response.json()
                temp = data["current"]["temp_c"]
                await message.reply(f"🌦 Температура в Лондоне: {temp}°C")
    except Exception as e:
        await message.reply("❌ Ошибка при запросе погоды.")

# 📌 Команда /joke – Случайная шутка
@dp.message(Command("joke"))
async def joke(message: Message):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("https://official-joke-api.appspot.com/jokes/random") as response:
                joke_data = await response.json()
                await message.reply(f"😂 {joke_data['setup']}\n{joke_data['punchline']}")
    except Exception as e:
        await message.reply("❌ Ошибка при запросе шутки.")

# 📌 Запуск бота
async def main():
    print("Бот запущен!")
    asyncio.create_task(keep_alive())  # Запуск keep-alive в фоне
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
