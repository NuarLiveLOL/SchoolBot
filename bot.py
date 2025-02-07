import socket

predefined_ips = [
    "192.168.1.95",
    "192.168.1.89",
    "192.168.1.90",
    "192.168.1.87",
    "192.168.1.67",
    "192.168.1.101",
    "192.168.1.61",
    "192.168.1.88",
    "192.168.1.167"

]

def connect_and_send_command(selected_ip, command_to_send):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((selected_ip, 5000))  # Подключаемся к порту клиента
            print(f"Подключено к клиенту: {selected_ip}")
            
            s.send(command_to_send.encode())
            print(f'Команда "{command_to_send}" отправлена на клиента {selected_ip}.')
            
            if command_to_send == "show_windows":
                response = s.recv(1024).decode()
                print("\nОткрытые окна на клиенте:")
                print(response)

    except (socket.timeout, ConnectionRefusedError):
        print(f"Не удалось подключиться к {selected_ip}. Возможно, порт закрыт.")

def manage_all_clients(command_to_send):
    for ip in predefined_ips:
        connect_and_send_command(ip, command_to_send)

while True:
    print("Список доступных устройств для подключения:")
    for idx, ip in enumerate(predefined_ips, 1):
        print(f"{idx}. {ip}")

    print("\nВыберите режим:")
    print("1. Управление одним ПК")
    print("2. Управление всеми ПК")

    mode = input("Введите номер режима (1 или 2): ")

    if mode == "1":
        try:
            choice = int(input("Выберите устройство для управления (введите номер): "))
            selected_ip = predefined_ips[choice - 1]
        except (ValueError, IndexError):
            print("Неверный выбор. Программа продолжит работу.")
            continue

        print("\nДоступные команды для выполнения:")
        print("1. open_notepad - открыть блокнот")
        print("2. close_notepad - закрыть блокнот")
        print("3. open_cmd - открыть командную строку")
        print("4. close_cmd - закрыть командную строку")
        print("5. shutdown - выключить ПК")
        print("6. show_windows - отобразить открытые окна")
        print("7. close_window - закрыть выбранное окно")
        print("8. install_module - установить Python-модуль")
        print("9. clear_downloads - очистить папку загрузок")
        print("10. clear_browser_history - очистить историю браузеров")

        command_to_send = input("Введите команду для выполнения на клиенте: ")

        if command_to_send == 'exit':
            print("Завершаем работу.")
            break

        connect_and_send_command(selected_ip, command_to_send)

    elif mode == "2":
        print("\nДоступные команды для выполнения на всех ПК:")
        print("1. open_notepad - открыть блокнот")
        print("2. close_notepad - закрыть блокнот")
        print("3. open_cmd - открыть командную строку")
        print("4. close_cmd - закрыть командную строку")
        print("5. shutdown - выключить ПК")
        print("6. show_windows - отобразить открытые окна")
        print("7. close_window - закрыть выбранное окно")
        print("8. install_module - установить Python-модуль")
        print("9. clear_downloads - очистить папку загрузок")
        print("10. clear_browser_history - очистить историю браузеров")

        command_to_send = input("Введите команду для выполнения на всех устройствах: ")

        if command_to_send == 'exit':
            print("Завершаем работу.")
            break

        manage_all_clients(command_to_send)

    else:
        print("Неверный выбор. Попробуйте снова.")
