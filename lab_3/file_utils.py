import os
import json


def load_config(config_path):
    """Загружает JSON-конфиг с проверкой существования файла."""
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {config_path}: {e}")


def save_bytes(data, file_path):
    """Сохраняет байтовые данные в файл."""
    if not data:
        raise ValueError("Нет данных для сохранения")
    
    # Создаём директорию, если её нет
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    with open(file_path, 'wb') as f:
        f.write(data)


def load_bytes(file_path):
    """Загружает байтовые данные из файла."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    with open(file_path, 'rb') as f:
        return f.read()


def file_exists(file_path):
    """Проверяет существование файла."""
    return os.path.exists(file_path)


def get_file_size(file_path):
    """Возвращает размер файла в байтах."""
    if not os.path.exists(file_path):
        return 0
    return os.path.getsize(file_path)