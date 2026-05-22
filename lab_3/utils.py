
"""
Модуль вспомогательных функций и обработки ошибок
"""

import os
import json
import traceback
from datetime import datetime


class CryptoError(Exception):
    """Базовый класс для ошибок криптосистемы."""
    pass


class KeyGenerationError(CryptoError):
    """Ошибка при генерации ключей."""
    pass


class EncryptionError(CryptoError):
    """Ошибка при шифровании."""
    pass


class DecryptionError(CryptoError):
    """Ошибка при дешифровании."""
    pass


class FileOperationError(CryptoError):
    """Ошибка при работе с файлами."""
    pass


def handle_error(error: Exception, context: str = "") -> str:
    """
    Обрабатывает ошибку и возвращает сообщение.
    
    Args:
        error: Исключение.
        context: Контекст возникновения ошибки.
    
    Returns:
        Отформатированное сообщение об ошибке.
    """
    error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] "
    
    if context:
        error_msg += f"{context}: "
    
    if isinstance(error, FileNotFoundError):
        error_msg += f"Файл не найден: {error.filename}"
    elif isinstance(error, PermissionError):
        error_msg += f"Нет прав доступа к файлу: {error.filename}"
    elif isinstance(error, ValueError):
        error_msg += f"Ошибка валидации: {str(error)}"
    elif isinstance(error, CryptoError):
        error_msg += str(error)
    else:
        error_msg += f"Неожиданная ошибка: {str(error)}"
    
    return error_msg


def log_operation(operation: str, details: str = "") -> None:
    """
    Логирует операцию в консоль.
    
    Args:
        operation: Название операции.
        details: Детали операции.
    """
    timestamp = datetime.now().strftime('%H:%M:%S')
    print(f"[{timestamp}] [{operation}] {details}")


def save_settings(settings: dict, filepath: str) -> None:
    """Сохраняет настройки в JSON файл."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(settings, f, indent=4, ensure_ascii=False)


def load_settings(filepath: str) -> dict:
    """Загружает настройки из JSON файла."""
    if not os.path.exists(filepath):
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def validate_file_exists(filepath: str) -> bool:
    """Проверяет существование файла."""
    return os.path.exists(filepath)


def get_file_size_mb(filepath: str) -> float:
    """Возвращает размер файла в мегабайтах."""
    if os.path.exists(filepath):
        return os.path.getsize(filepath) / (1024 * 1024)
    return 0.0


def ensure_directory_exists(filepath: str) -> None:
    """Создает директорию для файла, если её нет."""
    directory = os.path.dirname(filepath)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)