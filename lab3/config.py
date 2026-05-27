import json
from pathlib import Path


REQUIRED_KEYS = [
    'initial_file', 'encrypted_file', 'decrypted_file',
    'symmetric_key', 'public_key', 'private_key'
]


def load_config(config_path: str = "settings.json") -> dict:
    """Загружает конфигурацию из JSON и проверяет обязательные ключи."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            settings = json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл конфигурации '{config_path}' не найден")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка в JSON: {e}", e.doc, e.pos)

    missing = [k for k in REQUIRED_KEYS if k not in settings]
    if missing:
        raise KeyError(f"Отсутствуют обязательные ключи: {missing}")

    return settings


def ensure_directories(settings: dict) -> None:
    """Создаёт папки для всех файлов из конфигурации, если их нет."""
    for path in settings.values():
        Path(path).parent.mkdir(parents=True, exist_ok=True)