import hashlib
import random
import json
import os
from typing import Optional

def load_config(config_path: str = "constants.json") -> dict:
    """Загружает конфигурацию из JSON файла.

    Args:
        config_path: Путь к конфигурационному файлу.

    Returns:
        dict: Словарь с параметрами конфигурации.
    """
    try:
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Конфигурационный файл '{config_path}' не найден.")
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"Ошибка парсинга JSON в '{config_path}': {e.msg}", e.doc, e.pos)
    except Exception as e:
        raise RuntimeError(f"Непредвиденная ошибка при загрузке конфигурации: {e}") from e

try:
    _CONFIG = load_config()
    CHARACTERS = _CONFIG["CHARACTERS"]
    MIN_LEN = _CONFIG["MIN_STRING_LENGTH"]
    MAX_LEN = _CONFIG["MAX_STRING_LENGTH"]
except Exception as e:
    raise RuntimeError(f"Не удалось инициализировать модуль hash_utils: {e}") from e

def generate_random_string(length: Optional[int] = None) -> str:
    """Генерирует случайную строку из предопределённого набора символов.

    Args:
        length: Желаемая длина строки. Если None, длина выбирается случайно
                в диапазоне [MIN_LEN, MAX_LEN].

    Returns:
        str: Сгенерированная случайная строка.
    """
    match length:
        case None:
            length = random.randint(MIN_LEN, MAX_LEN)
        case l if l > 0:
            pass
        case _:
            raise ValueError("Длина строки должна быть положительным числом или None.")

    try:
        return ''.join(random.choice(CHARACTERS) for _ in range(length))
    except Exception as e:
        raise RuntimeError(f"Ошибка генерации случайной строки: {e}") from e

def compute_full_hash(data: str, algorithm: str = "sha256") -> str:
    """Вычисляет полный криптографический хеш заданной строки.

    Args:
        data: Входная строка для хеширования.
        algorithm: Название алгоритма хеширования (по умолчанию 'sha256').

    Returns:
        str: Хеш-сумма в шестнадцатеричном формате.
    """
    if not isinstance(data, str):
        raise TypeError("Ожидается строка для хеширования.")
    try:
        return hashlib.new(algorithm, data.encode('utf-8')).hexdigest()
    except ValueError as e:
        raise ValueError(f"Неподдерживаемый алгоритм хеширования '{algorithm}': {e}") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка при вычислении хеша: {e}") from e

def truncate_hash(full_hash: str, bits: int) -> str:
    """Укорачивает полный хеш до заданного количества бит.

    Args:
        full_hash: Полный хеш в шестнадцатеричном представлении.
        bits: Требуемое количество бит (должно быть кратно 4: 8, 12, 16).

    Returns:
        str: Укороченный хеш.
    """
    match bits <= 0 or bits % 4 != 0:
        case True:
            raise ValueError("Количество бит должно быть положительным и кратным 4.")
        case False:
            pass

    hex_chars = bits // 4
    match hex_chars > len(full_hash):
        case True:
            raise ValueError(f"Требуемая длина ({hex_chars} hex) превышает длину полного хеша ({len(full_hash)} hex).")
        case False:
            pass

    return full_hash[:hex_chars]

def get_hash(data: str, bits: int) -> str:
    """Вычисляет укороченный хеш строки заданной битовой длины.

    Args:
        data: Входная строка.
        bits: Количество бит для обрезки хеша (например, 8, 12, 16).

    Returns:
        str: Укороченный хеш в шестнадцатеричном формате.
    """
    try:
        full_hash = compute_full_hash(data)
        return truncate_hash(full_hash, bits)
    except Exception as e:
        raise RuntimeError(f"Ошибка при получении укороченного хеша: {e}") from e