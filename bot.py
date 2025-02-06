import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.utils.executor import start_webhook
from dotenv import load_dotenv
import requests

# Загрузка переменных окружения
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
RENDER_DOMAIN = os.getenv("RENDER_DOMAIN")

WEBHOOK_PATH = f"/webhook/{TOKEN}"
WEBHOOK_URL = f"{RENDER_DOMAIN}{WEBHOOK_PATH}"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Хэндлер для получения обновлений от вебхука
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message):
    await message.answer("Привет! Я бот, с которым ты можешь взаимодействовать.")

@dp.message_handler(commands=["game"])
async def start_game(message):
    await message.answer("Начинаем игру!")

# Хэндлер для команды /weather
@dp.message_handler(commands=["weather"])
async def weather(message):
    # Пример получения данных о погоде
    city = "Moscow"
    api_key = os.getenv("WEATHER_API_KEY")  # Убедитесь, что API ключ для погоды прописан в .env
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=ru"
    
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        temp = data['main']['temp']
        description = data['weather'][0]['description']
        await message.answer(f"Погода в {city}: {temp}°C, {description}")
    else:
        await message.answer("Не удалось получить данные о погоде.")

# Функция для поддержания живости (используем keep-alive запрос)
def keep_alive():
    url = f"{RENDER_DOMAIN}/"
    try:
        requests.get(url)
    except Exception as e:
        print(f"Error during keep alive: {e}")

# Хэндлер для webhook
async def on_start(webhook: str, update: Update):
    print(f"Получен новый запрос: {update}")
    await bot.process_update(update)

# Установка вебхука
async def set_webhook():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(WEBHOOK_URL)

# Основная функция для запуска бота
async def main():
    # Установка вебхука
    await set_webhook()

    # Запуск вебхука
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_start=on_start,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 10000)),
    )

    # Долгий запуск: keep-alive запросы
    while True:
        keep_alive()
        await asyncio.sleep(300)  # каждую 5 минут отправляется запрос, чтобы не было разрыва соединения

if __name__ == "__main__":
    asyncio.run(main())
