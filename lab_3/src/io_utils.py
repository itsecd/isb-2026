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


class FileReadError(Exception):
    """Исключение, возникающее при ошибке чтения файла."""
    pass


class FileWriteError(Exception):
    """Исключение, возникающее при ошибке записи файла."""
    pass


class ConfigLoadError(Exception):
    """Исключение, возникающее при ошибке загрузки конфигурации."""
    pass


def read_binary_file(path: str) -> bytes:
    """
    Читает содержимое файла в бинарном режиме.
    
    Args:
        path: Путь к файлу для чтения.
        
    Returns:
        bytes: Содержимое файла в виде байтов.
        
    Raises:
        FileReadError: Если файл не найден или произошла ошибка чтения.
    """
    try:
        with open(path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        raise FileReadError(f"Файл не найден: {path}")
    except PermissionError:
        raise FileReadError(f"Нет прав на чтение файла: {path}")
    except IOError as e:
        raise FileReadError(f"Ошибка при чтении файла {path}: {e}")


def write_binary_file(path: str, data: bytes) -> None:
    """
    Записывает данные в файл в бинарном режиме.
    
    Args:
        path: Путь к файлу для записи.
        data: Данные для записи в файл.
        
    Raises:
        FileWriteError: Если произошла ошибка при записи файла.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            file.write(data)
    except PermissionError:
        raise FileWriteError(f"Нет прав на запись в файл: {path}")
    except IOError as e:
        raise FileWriteError(f"Ошибка при записи в файл {path}: {e}")


def read_text_file(path: str, encoding: str = 'utf-8') -> str:
    """
    Читает текстовый файл с указанной кодировкой.
    
    Args:
        path: Путь к файлу для чтения.
        encoding: Кодировка файла (по умолчанию 'utf-8').
        
    Returns:
        str: Содержимое файла в виде строки.
        
    Raises:
        FileReadError: Если файл не найден или произошла ошибка чтения.
    """
    try:
        with open(path, 'r', encoding=encoding) as file:
            return file.read()
    except FileNotFoundError:
        raise FileReadError(f"Файл не найден: {path}")
    except UnicodeDecodeError:
        raise FileReadError(f"Ошибка декодирования файла {path}. Проверьте кодировку.")
    except IOError as e:
        raise FileReadError(f"Ошибка при чтении файла {path}: {e}")


def write_text_file(path: str, content: str, encoding: str = 'utf-8') -> None:
    """
    Записывает строку в текстовый файл.
    
    Args:
        path: Путь к файлу для записи.
        content: Строка для записи.
        encoding: Кодировка файла (по умолчанию 'utf-8').
        
    Raises:
        FileWriteError: Если произошла ошибка при записи файла.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding=encoding) as file:
            file.write(content)
    except IOError as e:
        raise FileWriteError(f"Ошибка при записи в файл {path}: {e}")


def load_json_config(path: str) -> Dict[str, Any]:
    """
    Загружает конфигурацию из JSON файла.
    
    Args:
        path: Путь к JSON файлу конфигурации.
        
    Returns:
        Dict[str, Any]: Словарь с конфигурацией.
        
    Raises:
        ConfigLoadError: Если файл конфигурации не найден или содержит невалидный JSON.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        raise ConfigLoadError(f"Файл конфигурации не найден: {path}")
    except json.JSONDecodeError as e:
        raise ConfigLoadError(f"Ошибка в формате JSON файла {path}: {e}")
    except IOError as e:
        raise ConfigLoadError(f"Ошибка при чтении файла конфигурации {path}: {e}")


def ensure_directory(path: str) -> None:
    """
    Создает директорию для файла, если она не существует.
    
    Args:
        path: Путь к файлу, для которого нужно создать директорию.
        
    Raises:
        FileWriteError: Если не удалось создать директорию.
    """
    try:
        directory = os.path.dirname(path)
        if directory:
            os.makedirs(directory, exist_ok=True)
    except PermissionError:
        raise FileWriteError(f"Нет прав на создание директории для файла: {path}")
    except OSError as e:
        raise FileWriteError(f"Ошибка при создании директории для файла {path}: {e}")