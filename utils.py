"""
Модуль вспомогательных утилит для гибридной криптосистемы.

Содержит функции для безопасной работы с файловой системой,
загрузки настроек из JSON и определения путей с учетом приоритетов.
"""

import json
import os
from typing import Dict, Optional


def load_settings(json_path: str = "settings.json") -> Dict[str, str]:
    """
    Загружает конфигурацию из JSON-файла.

    Args:
        json_path: Путь к файлу настроек (по умолчанию 'settings.json').

    Returns:
        Словарь с настройками или пустой словарь, если файл отсутствует.

    Raises:
        json.JSONDecodeError: Если файл содержит некорректный JSON.
        PermissionError: Если нет прав на чтение файла.
    """
    if not os.path.exists(json_path):
        return {}
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[ERROR] Ошибка парсинга {json_path}: {e}")
        raise
    except PermissionError as e:
        print(f"[ERROR] Нет прав на чтение {json_path}: {e}")
        raise


def save_bin_data(data: bytes, path: str) -> None:
    """
    Сохраняет бинарные данные в файл.

    Args:
        data: Байты для записи.
        path: Целевой путь файла.

    Raises:
        OSError: При ошибке записи на диск.
        TypeError: Если data не является объектом bytes.
    """
    if not isinstance(data, bytes):
        raise TypeError(f"Ожидаются байты, получено {type(data)}")
    try:
        os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
        print(f"[INFO] Данные сохранены в: {path}")
    except OSError as e:
        print(f"[ERROR] Не удалось сохранить {path}: {e}")
        raise


def load_bin_data(path: str) -> bytes:
    """
    Загружает бинарные данные из файла.

    Args:
        path: Путь к файлу.

    Returns:
        Содержимое файла в виде байтов.

    Raises:
        FileNotFoundError: Если файл не существует.
        PermissionError: Если нет прав на чтение.
        OSError: При другой ошибке чтения.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Файл не найден: {path}")
    try:
        with open(path, "rb") as f:
            return f.read()
    except PermissionError as e:
        print(f"[ERROR] Нет прав на чтение {path}: {e}")
        raise
    except OSError as e:
        print(f"[ERROR] Ошибка чтения {path}: {e}")
        raise


def get_path(
    cli_arg: Optional[str],
    settings: Dict[str, str],
    setting_key: str,
    default_val: str
) -> str:
    """
    Определяет путь по приоритету: CLI > settings.json > default.

    Args:
        cli_arg: Аргумент командной строки.
        settings: Словарь настроек.
        setting_key: Ключ в словаре настроек.
        default_val: Значение по умолчанию.

    Returns:
       Resolved путь к файлу.
    """
    if cli_arg:
        return cli_arg
    if setting_key in settings:
        return settings[setting_key]
    return default_val