"""
Модуль для операций ввода-вывода и работы с файлами.

Предоставляет функции для:
- Чтения и записи бинарных файлов
- Загрузки и сохранения ключей
- Работы с конфигурацией
"""

import json
import os
from typing import Any, Dict


def read_binary_file(path: str) -> bytes:
    """
    Читает содержимое файла в бинарном режиме.
    
    Args:
        path: Путь к файлу для чтения.
        
    Returns:
        bytes: Содержимое файла в виде байтов.
        
    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: Если произошла ошибка при чтении файла.
    """
    with open(path, 'rb') as file:
        return file.read()


def write_binary_file(path: str, data: bytes) -> None:
    """
    Записывает данные в файл в бинарном режиме.
    
    Args:
        path: Путь к файлу для записи.
        data: Данные для записи в файл.
        
    Raises:
        IOError: Если произошла ошибка при записи файла.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'wb') as file:
        file.write(data)


def read_text_file(path: str, encoding: str = 'utf-8') -> str:
    """
    Читает текстовый файл с указанной кодировкой.
    
    Args:
        path: Путь к файлу для чтения.
        encoding: Кодировка файла (по умолчанию 'utf-8').
        
    Returns:
        str: Содержимое файла в виде строки.
    """
    with open(path, 'r', encoding=encoding) as file:
        return file.read()


def write_text_file(path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    Записывает строку в текстовый файл.
    
    Args:
        path: Путь к файлу для записи.
        content: Строка для записи.
        encoding: Кодировка файла (по умолчанию 'utf-8').
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding=encoding) as file:
        file.write(content)


def load_json_config(path: str) -> Dict[str, Any]:
    """
    Загружает конфигурацию из JSON файла.
    
    Args:
        path: Путь к JSON файлу конфигурации.
        
    Returns:
        Dict[str, Any]: Словарь с конфигурацией.
        
    Raises:
        FileNotFoundError: Если файл конфигурации не найден.
        json.JSONDecodeError: Если файл содержит невалидный JSON.
    """
    with open(path, 'r', encoding='utf-8') as file:
        return json.load(file)


def ensure_directory(path: str) -> None:
    """
    Создает директорию для файла, если она не существует.
    
    Args:
        path: Путь к файлу, для которого нужно создать директорию.
    """
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)