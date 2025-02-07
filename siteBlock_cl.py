import time
import pygetwindow as gw
import psutil
import pyautogui

# Список запрещённых слов в заголовке вкладок
BLOCKED_KEYWORDS = ["game", "игры", "игра"]

# Функция для закрытия окна по заголовку
def close_forbidden_tabs():
    for window in gw.getWindowsWithTitle(""):
        title = window.title.lower()
        if any(keyword in title for keyword in BLOCKED_KEYWORDS):
            print(f"Закрываю: {title}")
            pyautogui.hotkey('ctrl', 'w')
            time.sleep(0.5)  # Подождём, чтобы избежать двойного срабатывания

# Проверка, запущен ли браузер
def is_browser_running():
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] and proc.info['name'].lower() in ['chrome.exe', 'firefox.exe', 'msedge.exe']:  # Укажи свои браузеры
            return True
    return False

if __name__ == "__main__":
    print("Запущен контроль браузера...")
    while True:
        if is_browser_running():
            close_forbidden_tabs()
        time.sleep(2)
