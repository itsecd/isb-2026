import json
import os
from typing import Any, Dict, Optional


class FileOperationError(Exception):
    """Исключение для ошибок при работе с файлами."""
    pass


def read_json_file(file_path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """Читает и парсит json файл."""
    try:
        with open(file_path, "r", encoding=encoding) as f:
            return json.load(f)
    except FileNotFoundError as e:
        raise FileOperationError(f"Файл не найден: {file_path}") from e
    except json.JSONDecodeError as e:
        raise FileOperationError(f"Ошибка парсинга json в файле {file_path}: {e}") from e
    except UnicodeDecodeError as e:
        raise FileOperationError(f"Ошибка кодировки файла {file_path}: {e}. Ожидается {encoding}") from e
    except Exception as e:
        raise FileOperationError(f"Неожиданная ошибка при чтении {file_path}: {e}") from e


def read_binary_file(file_path: str) -> bytes:
    """Читает бинарный файл."""
    try:
        with open(file_path, "rb") as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileOperationError(f"Файл не найден: {file_path}") from e
    except PermissionError as e:
        raise FileOperationError(f"Нет прав на чтение файла: {file_path}") from e
    except Exception as e:
        raise FileOperationError(f"Ошибка чтения файла {file_path}: {e}") from e


def write_binary_file(file_path: str, data: bytes, create_dirs: bool = True) -> None:
    """Записывает бинарные данные в файл."""
    try:
        if create_dirs:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, "wb") as f:
            f.write(data)
    except PermissionError as e:
        raise FileOperationError(f"Нет прав на запись в файл: {file_path}") from e
    except OSError as e:
        raise FileOperationError(f"Ошибка при записи файла {file_path}: {e}") from e
    except Exception as e:
        raise FileOperationError(f"Неожиданная ошибка при записи {file_path}: {e}") from e


def file_exists(file_path: str) -> bool:
    """Проверяет существование файла."""
    return os.path.exists(file_path)