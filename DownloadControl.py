import os
import time
import shutil
import string

# Запрещённые слова в названиях файлов и папок
BLOCKED_KEYWORDS = ["this", "next"]

# Системные папки, которые нельзя удалять
EXCLUDED_FOLDERS = [
    "System Volume Information",
    "$Recycle.Bin",
    "Windows",
    "Microsoft",
    "Common Files",
    "ProgramData",
    "Users"
]

def get_all_drives():
    """Определяет все локальные диски в системе."""
    drives = []
    for letter in string.ascii_uppercase:  # A-Z
        path = f"{letter}:/"
        if os.path.exists(path):
            drives.append(path)
    return drives

def delete_forbidden_items():
    """Удаляет файлы и папки с запрещёнными словами на всех дисках."""
    # Получаем список всех дисков + "Загрузки"
    drives = get_all_drives()
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    check_paths = [downloads_path] + drives

    for path in check_paths:
        if not os.path.exists(path):
            continue  # Пропускаем, если путь не существует

        for item_name in os.listdir(path):
            lower_name = item_name.lower()  # Приводим к нижнему регистру
            item_path = os.path.join(path, item_name)

            # Проверяем, есть ли запрещённое слово в названии
            if any(keyword in lower_name for keyword in BLOCKED_KEYWORDS):
                try:
                    if os.path.isfile(item_path) or os.path.islink(item_path):
                        os.remove(item_path)  # Удаляем файл
                        print(f"🗑️ Удален файл: {item_name} из {path}")

                    elif os.path.isdir(item_path):
                        # Пропускаем системные папки
                        if item_name in EXCLUDED_FOLDERS:
                            print(f"⚠️ Пропущена системная папка: {item_name}")
                            continue

                        # Проверяем наличие запрещённого слова в названии папки
                        if any(keyword in lower_name for keyword in BLOCKED_KEYWORDS):
                            shutil.rmtree(item_path)  # Удаляем папку и её содержимое
                            print(f"🗂️ Удалена папка: {item_name} из {path}")

                except Exception as e:
                    print(f"❌ Ошибка при удалении {item_name}: {e}")

if __name__ == "__main__":
    print("🔍 Запущен контроль файлов и папок на всех дисках...")
    while True:
        delete_forbidden_items()
        time.sleep(5)  # Проверяем каждые 5 секунд
