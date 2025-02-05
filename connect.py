import requests
import socket
import os
from dotenv import load_dotenv

# Загружаем .env
load_dotenv()
TOKEN = os.getenv("TOKEN")
CHAT_ID = os.getenv("ADMIN_ID")  # ID админа, можно оставить пустым

# Имя ПК (по умолчанию берет hostname)
pc_name = socket.gethostname()

# Отправляем команду боту
message = f"/connect '{pc_name}'"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

data = {
    "chat_id": CHAT_ID,
    "text": message
}

response = requests.post(url, data=data)

if response.status_code == 200:
    print(f"✅ ПК {pc_name} подключен к боту!")
else:
    print("❌ Ошибка при подключении ПК.")
