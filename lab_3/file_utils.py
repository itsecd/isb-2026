import os
import json
from typing import Any, Dict


def load_config(config_path: str) -> Dict[str, Any]:
    """
    Загружает JSON-конфиг из файла с проверкой существования файла.

    Args:
        config_path (str): Путь к JSON-файлу с настройками.

    Returns:
        Dict[str, Any]: Словарь с данными из JSON-файла.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {config_path}: {e}")


def save_bytes(data: bytes, file_path: str) -> None:
    """
    Сохраняет байтовые данные в файл. Автоматически создаёт промежуточные директории.

    Args:
        data (bytes): Байтовые данные для сохранения.
        file_path (str): Путь, по которому нужно сохранить файл.

    Returns:
        None
    """
    if not data:
        raise ValueError("Нет данных для сохранения")

    # Создаём директорию, если её нет
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    with open(file_path, 'wb') as f:
        f.write(data)


def load_bytes(file_path: str) -> bytes:
    """
    Загружает байтовые данные из файла.

    Args:
        file_path (str): Путь к файлу для чтения.

    Returns:
        bytes: Содержимое файла в виде байтовой строки.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, 'rb') as f:
        return f.read()


def file_exists(file_path: str) -> bool:
    """
    Проверяет существование файла.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        bool: True если файл существует, False в противном случае.
    """
    return os.path.exists(file_path)


def get_file_size(file_path: str) -> int:
    """
    Возвращает размер файла в байтах.

    Args:
        file_path (str): Путь к файлу.

    Returns:
        int: Размер файла в байтах. Возвращает 0, если файл не существует.
    """
    if not os.path.exists(file_path):
        return 0
    return os.path.getsize(file_path)