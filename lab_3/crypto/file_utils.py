"""
Утилиты: логирование, чтение/запись файлов, загрузка настроек.
"""

import json
import os


def log(msg: str) -> None:
    """Выводит информационное сообщение о ходе выполнения."""
    print(f"[*] {msg}")


def load_settings(path: str) -> dict:
    """Загружает конфигурацию из JSON-файла."""
    log(f"Загрузка настроек из {path}...")
    with open(path) as f:
        cfg = json.load(f)

    base_dir = os.path.dirname(os.path.abspath(path))
    for key, value in cfg.items():
        if isinstance(value, str) and not os.path.isabs(value):
            cfg[key] = os.path.normpath(os.path.join(base_dir, value))
    return cfg


def _ensure_dir(path: str) -> None:
    """Создаёт родительские папки для файла, если они не существуют."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def save_bytes(data: bytes, path: str) -> None:
    """Сохраняет байты в файл, создавая папки при необходимости."""
    _ensure_dir(path)
    with open(path, "wb") as f:
        f.write(data)


def load_bytes(path: str) -> bytes:
    """Читает байты из файла."""
    with open(path, "rb") as f:
        return f.read()
