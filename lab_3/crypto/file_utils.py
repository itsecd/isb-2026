"""Утилиты для работы с файлами и конфигурацией.

Содержит функции для логирования, загрузки JSON-настроек,
чтения и записи байтов, а также создание необходимых каталогов.
"""

import json
import os


def log(msg: str) -> None:
    """Выводит информационное сообщение о ходе выполнения.

    Args:
        msg: Текст сообщения для вывода.
"""
    print(f"[*] {msg}")


def load_settings(path: str) -> dict:
    """Загружает данные настроек из указанного JSON-файла.

    При загрузке относительные пути в значениях словаря преобразуются
    в абсолютные, относительно директории файла настроек.

    Args:
        path: Путь к JSON-файлу с настройками.

    Returns:
        Словарь с загруженной конфигурацией.

    Raises:
        RuntimeError: Если файл не найден или JSON некорректен.
"""
    log(f"Загрузка настроек из {path}...")
    try:
        with open(path) as f:
            cfg = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise RuntimeError(f"Ошибка при загрузке настроек: {e}")

    base_dir = os.path.dirname(os.path.abspath(path))
    for key, value in cfg.items():
        if isinstance(value, str) and not os.path.isabs(value):
            cfg[key] = os.path.normpath(os.path.join(base_dir, value))
    return cfg


def _ensure_dir(path: str) -> None:
    """Создаёт родительские каталоги для указанного пути файла.

    Args:
        path: Путь к файлу, для которого нужно создать родительский каталог.
"""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def save_bytes(data: bytes, path: str) -> None:
    """Сохраняет байтовые данные в файл.

    Если для указанного файла не существует родительского каталога,
    он будет создан автоматически.

    Args:
        data: Байтовые данные для записи.
        path: Путь к файлу, в который нужно записать данные.

    Raises:
        RuntimeError: Если запись в файл не удалась.
"""
    _ensure_dir(path)
    try:
        with open(path, "wb") as f:
            f.write(data)
    except OSError as e:
        raise RuntimeError(f"Не удалось сохранить файл {path}: {e}")


def load_bytes(path: str) -> bytes:
    """Читает все байты из указанного файла.

    Args:
        path: Путь к файлу для чтения.

    Returns:
        Содержимое файла в виде байтовой строки.

    Raises:
        RuntimeError: Если файл не найден или чтение не удалось.
"""
    try:
        with open(path, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        raise RuntimeError(f"Файл не найден: {path}")
    except OSError as e:
        raise RuntimeError(f"Не удалось прочитать файл {path}: {e}")
