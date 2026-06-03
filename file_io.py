"""Модуль для работы с файлами: чтение, запись, JSON."""

import json
from typing import Any, Dict


def read_bytes(file_path: str) -> bytes:
    """Читает файл и возвращает его содержимое в виде байтов.

    Args:
        file_path: Путь к файлу.

    Returns:
        bytes: Содержимое файла.
    """
    with open(file_path, 'rb') as f:
        return f.read()


def write_bytes(file_path: str, data: bytes) -> None:
    """Записывает байтовые данные в файл.

    Args:
        file_path: Путь к файлу.
        data: Данные для записи.
    """
    with open(file_path, 'wb') as f:
        f.write(data)


def read_json(file_path: str) -> Dict[str, Any]:
    """Читает JSON-файл и возвращает словарь.

    Args:
        file_path: Путь к JSON-файлу.

    Returns:
        Dict[str, Any]: Данные из файла.
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def write_json(file_path: str, data: Dict[str, Any]) -> None:
    """Записывает словарь в JSON-файл.

    Args:
        file_path: Путь к файлу.
        data: Данные для записи.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
