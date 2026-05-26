import os
import sys
import json

def read_json(path):
    """
    Читает и парсит JSON файл.

    Входные данные:
        path (str): Путь к JSON файлу.

    Выходные данные:
        dict: Словарь с данными из JSON, или None в случае ошибки.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
    except Exception as e:
        print(f"Ошибка чтения {path}: {e}")
    return None

def read_file(path):
    """
    Читает содержимое файла в бинарном режиме.

    Входные данные:
        path (str): Путь к файлу.

    Выходные данные:
        bytes: Содержимое файла, или None в случае ошибки.
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Ошибка: Файл не найден: {path}")
    except Exception as e:
        print(f"Ошибка чтения файла {path}: {e}")
    return None

def write_file(path, data):
    """
    Записывает данные в файл в бинарном режиме. Создает директории, если их нет.

    Входные данные:
        path (str): Путь для сохранения файла.
        data (bytes): Данные для записи.

    Выходные данные:
        bool: True если запись успешна, False иначе.
    """
    try:
        directory = os.path.dirname(path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

        with open(path, 'wb') as f:
            f.write(data)
        return True
    except Exception as e:
        print(f"Ошибка записи файла {path}: {e}")
    return False

def load_settings(settings_path='settings.json'):
    """
    Загружает настройки из JSON файла.

    Входные данные:
        settings_path (str): Путь к файлу настроек (по умолчанию 'settings.json').

    Выходные данные:
        dict: Словарь настроек. Если файл не найден или невалиден, программа завершается с кодом 1.
    """
    settings = read_json(settings_path)
    if settings is None:
        sys.exit(1)
    return settings