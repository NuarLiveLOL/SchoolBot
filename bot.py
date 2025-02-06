import logging
import requests
import time
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters

# Замените на ваш API ключ Telegram бота
API_TOKEN = '7511733020:AAHTjBOd87NB8awXCH6OUHGAHqFGZ0QPWuI'

# URL для пинга (замените на URL вашего проекта)
PING_URL = 'https://schoolbot-x1xt.onrender.com'

# Время между пингами (в секундах)
PING_INTERVAL = 300  # Пинговать каждые 5 минут

# Включение логирования для отладки
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Хранилище пользователей и их статистики
users = {}

# Функция пинга
def ping():
    try:
        response = requests.get(PING_URL)
        if response.status_code == 200:
            print("Проект доступен.")
        else:
            print(f"Ошибка при пинге: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при пинге: {e}")

# Команда /start для бота
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in users:
        users[user_id] = {'level': 1, 'hp': 100, 'attack': 10}
    
    update.message.reply_text(f'Привет, {update.message.from_user.first_name}! Добро пожаловать в игру! Введи /fight, чтобы сразиться с монстром.')

# Команда /fight для начала сражения
def fight(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in users:
        update.message.reply_text('Сначала начни игру с командой /start.')
        return
    
    user = users[user_id]
    monster_hp = random.randint(20, 50)  # Случайное количество здоровья монстра
    monster_attack = random.randint(5, 15)  # Случайный урон монстра

    update.message.reply_text(f'Ты встретил монстра с {monster_hp} HP! Начинаем бой!')
    
    while user['hp'] > 0 and monster_hp > 0:
        user_attack = random.randint(user['attack'] - 2, user['attack'] + 2)
        monster_hp -= user_attack
        update.message.reply_text(f'Ты атаковал монстра на {user_attack} урона! У монстра осталось {monster_hp} HP.')
        
        if monster_hp <= 0:
            update.message.reply_text(f'Монстр побежден! Ты победил в бою!')
            user['level'] += 1  # Увеличиваем уровень
            user['hp'] = 100  # Восстанавливаем здоровье
            user['attack'] += 5  # Увеличиваем атаку
            break
        
        monster_damage = random.randint(monster_attack - 2, monster_attack + 2)
        user['hp'] -= monster_damage
        update.message.reply_text(f'Монстр атакует тебя на {monster_damage} урона! У тебя осталось {user["hp"]} HP.')
        
        if user['hp'] <= 0:
            update.message.reply_text(f'Ты погиб в бою... Game Over!')
            break

# Команда /stats для просмотра статистики
def stats(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    if user_id not in users:
        update.message.reply_text('Сначала начни игру с командой /start.')
        return

    user = users[user_id]
    update.message.reply_text(f'Твоя статистика:\nУровень: {user["level"]}\nЗдоровье: {user["hp"]}\nАтака: {user["attack"]}')

# Функция для запуска пинга каждые 5 минут
def ping_loop(context: CallbackContext):
    ping()
    context.job_queue.run_once(ping_loop, PING_INTERVAL)

def main():
    updater = Updater(API_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрируем команды
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('fight', fight))
    dispatcher.add_handler(CommandHandler('stats', stats))

    # Запускаем пинг-процесс
    updater.job_queue.run_once(ping_loop, 0)  # Первый пинг сразу, затем через 5 минут

    # Запуск бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
