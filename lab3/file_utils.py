"""
Модуль для работы с файлами.

Содержит функции для чтения/записи бинарных и текстовых файлов,
а также для генерации случайных байтов.
"""

import os

class FileOperationError(Exception):
    """Базовое исключение для ошибок операций с файлами."""
    pass

def read_binary_file(path):
    """
    Читает бинарные данные из файла.
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {path}")
    except Exception as e:
        raise FileOperationError(f"Ошибка при чтении файла {path}: {e}")

def write_binary_file(path, data):
    """
    Записывает бинарные данные в файл.
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except PermissionError:
        raise PermissionError(f"Нет прав на запись в файл: {path}")
    except Exception as e:
        raise FileOperationError(f"Ошибка при записи в файл {path}: {e}")

def read_text_file(path, encoding='utf-8'):
    """
    Читает текстовые данные из файла.
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл не найден: {path}")
    except UnicodeDecodeError:
        raise FileOperationError(f"Ошибка кодировки в файле: {path}")
    except Exception as e:
        raise FileOperationError(f"Ошибка при чтении текстового файла {path}: {e}")

def write_text_file(path, text, encoding='utf-8'):
    """
    Записывает текстовые данные в файл.
    """
    try:
        with open(path, 'w', encoding=encoding) as f:
            f.write(text)
    except Exception as e:
        raise FileOperationError(f"Ошибка при записи текстового файла {path}: {e}")

def generate_random_bytes(n):
    """
    Генерирует n случайных байтов.
    """
    return os.urandom(n)
