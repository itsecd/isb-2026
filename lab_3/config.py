"""Загрузка и нормализация JSON-настроек приложения."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_config(path: str | None) -> dict[str, Any]:
    """Загружает настройки из JSON-файла.

    Аргументы:
        path: Необязательный путь к JSON-файлу настроек.

    Возвращает:
        Словарь с настройками. Если путь не задан, возвращается пустой словарь.
    """
    match path:
        case None:
            return {}
        case _:
            with Path(path).open("r", encoding="utf-8") as config_file:
                return normalize_config(json.load(config_file))


def normalize_config(config: dict[str, Any]) -> dict[str, Any]:
    """Приводит старые имена настроек к именам, которые использует CLI."""
    aliases = {
        "encrypted_key_file": "encrypted_symmetric_key",
        "public_key_file": "public_key",
        "private_key_file": "private_key",
        "encrypted_file": "output_file",
        "decrypted_file": "output_file",
        "key_size": "key_bits",
    }
    normalized = dict(config)
    for old_name, new_name in aliases.items():
        match old_name in normalized and new_name not in normalized:
            case True:
                normalized[new_name] = normalized[old_name]
            case False:
                pass
    return normalized


def pick_value(
    args: Any,
    config: dict[str, Any],
    name: str,
    *,
    required: bool = True,
    default: Any = None,
) -> Any:
    """Берет настройку из аргументов CLI, затем из JSON и затем из значения по умолчанию.

    Аргументы:
        args: Пространство имен, полученное после разбора аргументов argparse.
        config: Настройки из JSON-файла.
        name: Имя настройки.
        required: Признак обязательности значения.
        default: Значение по умолчанию.

    Возвращает:
        Найденное значение настройки.

    Исключения:
        ValueError: Если обязательная настройка не указана.
    """
    value = getattr(args, name, None)
    match value is None:
        case True:
            value = config.get(name, default)
        case False:
            pass

    match required and value is None:
        case True:
            raise ValueError(f"Не указан обязательный параметр: {name}")
        case False:
            return value
