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
        bytes: Содержимое файла в виде байтов
        
    Raises:
        FileNotFoundError: Если файл не найден.
        PermissionError: Если нет прав на чтение.
        OSError: При других системных ошибках.
    """
    try:
        with open(path, 'rb') as file:
            data = file.read()
    except FileNotFoundError as e:
        print(f"Ошибка чтения: файл '{path}' не найден.")
        raise
    except PermissionError as e:
        print(f"Ошибка чтения: нет прав доступа к '{path}'.")
        raise
    except OSError as e:
        print(f"Ошибка чтения '{path}': {e}")
        raise
    else:
        return data
    finally:
        pass


def write_binary_file(path: str, data: bytes) -> None:
    """
    Записывает данные в файл в бинарном режиме.
    
    Args:
        path: Путь к файлу для записи.
        data: Данные для записи в файл.
        
    Raises:
        PermissionError: Если нет прав на запись.
        OSError: При других системных ошибках.
    """
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as file:
            file.write(data)
    except PermissionError as e:
        print(f"Ошибка записи: нет прав на создание/запись '{path}'.")
        raise
    except OSError as e:
        print(f"Ошибка записи '{path}': {e}")
        raise
    else:
        print(f"Данные успешно записаны в '{path}'.")


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
        OSError: При других ошибках чтения.
    """
    try:
        with open(path, 'r', encoding='utf-8') as file:
            config = json.load(file)
    except FileNotFoundError as e:
        print(f"Ошибка конфигурации: файл '{path}' не найден.")
        raise
    except json.JSONDecodeError as e:
        print(f"Ошибка конфигурации: некорректный JSON в '{path}'. Строка {e.lineno}, столбец {e.colno}.")
        raise
    except OSError as e:
        print(f"Ошибка конфигурации: {e}")
        raise
    else:
        required_keys = ['initial_file', 'encrypted_file', 'decrypted_file', 'symmetric_key', 'encrypted_symmetric_key', 'public_key', 'private_key', 'rsa_key_size', 'rsa_public_exponent', 'sm4_key_size', 'block_size']
        missing = [k for k in required_keys if k not in config]
        if missing:
            raise ValueError(f"В конфигурации '{path}' отсутствуют обязательные параметры: {missing}")
        return config