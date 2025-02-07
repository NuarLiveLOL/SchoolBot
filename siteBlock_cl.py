import time
import pygetwindow as gw
import psutil
import pyautogui
import pyperclip #1

# Список запрещённых слов в заголовке вкладок
BLOCKED_KEYWORDS = ["game", "игры", "игра"]

# Белый список сайтов, где можно читать о играх
WHITELIST_SITES = ["wikipedia.org", "khanacademy.org", "coursera.org"]

# Функция для получения URL активной вкладки (Chrome)
def get_active_tab_url():
    pyautogui.hotkey('ctrl', 'l')  # Перейти в адресную строку
    time.sleep(0.05)
    pyautogui.hotkey('ctrl', 'c')  # Скопировать URL
    time.sleep(0.05)
    return pyperclip.paste().lower()

# Функция для закрытия окна по заголовку
def close_forbidden_tabs():
    for window in gw.getWindowsWithTitle(""):
        title = window.title.lower()
        if any(keyword in title for keyword in BLOCKED_KEYWORDS):
            url = get_active_tab_url()
            if any(site in url for site in WHITELIST_SITES):
                print(f"Разрешено: {title} ({url})")
                continue
            print(f"Закрываю: {title} ({url})")
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
