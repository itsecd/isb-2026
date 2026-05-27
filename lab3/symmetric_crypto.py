"""
Модуль для работы с файлами.

Содержит функции для чтения/записи бинарных и текстовых файлов,
а также для генерации случайных байтов.
"""

import os
import errno

# Опционально: можно определить пользовательские исключения для этого модуля
class FileOperationError(Exception):
    """Базовое исключение для ошибок операций с файлами."""
    pass

def read_binary_file(path):
    """
    Читает бинарные данные из файла.

    Args:
        path (str): Путь к файлу для чтения.

    Returns:
        bytes: Содержимое файла в виде байтов.

    Raises:
        FileNotFoundError: Если файл не найден.
        PermissionError: Если нет прав на чтение.
        FileOperationError: Для других ошибок ввода-вывода.
    """
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        raise # Переподнимаем исключение, чтобы main мог его обработать
    except PermissionError:
        raise # Переподнимаем исключение
    except OSError as e:
        if e.errno == errno.ENAMETOOLONG:
             raise FileOperationError(f"Слишком длинный путь к файлу '{path}'.")
        # Можно добавить другие проверки errno
        raise FileOperationError(f"Ошибка ввода-вывода при чтении файла '{path}': {e}")
    except Exception as e:
        raise FileOperationError(f"Неожиданная ошибка при чтении файла '{path}': {e}")

def write_binary_file(path, data):
    """
    Записывает бинарные данные в файл.

    Args:
        path (str): Путь к файлу для записи.
        data (bytes): Данные для записи.

    Raises:
        PermissionError: Если нет прав на запись.
        FileOperationError: Для других ошибок ввода-вывода.
    """
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except PermissionError:
        raise # Переподнимаем исключение
    except OSError as e:
        if e.errno == errno.ENOSPC:
            raise FileOperationError(f"Недостаточно места на диске для записи в '{path}'.")
        elif e.errno == errno.ENAMETOOLONG:
             raise FileOperationError(f"Слишком длинный путь к файлу '{path}' для записи.")
        # Можно добавить другие проверки errno
        raise FileOperationError(f"Ошибка ввода-вывода при записи файла '{path}': {e}")
    except Exception as e:
        raise FileOperationError(f"Неожиданная ошибка при записи файла '{path}': {e}")

def read_text_file(path, encoding='utf-8'):
    """
    Читает текстовые данные из файла с заданной кодировкой.

    Args:
        path (str): Путь к файлу для чтения.
        encoding (str): Кодировка файла (по умолчанию utf-8).

    Returns:
        str: Содержимое файла в виде строки.

    Raises:
        FileNotFoundError: Если файл не найден.
        PermissionError: Если нет прав на чтение.
        UnicodeDecodeError: Если данные не соответствуют указанной кодировке.
        FileOperationError: Для других ошибок ввода-вывода.
    """
    try:
        with open(path, 'r', encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        raise
    except PermissionError:
        raise
    except UnicodeDecodeError as e:
        raise FileOperationError(f"Ошибка декодирования текста в файле '{path}' с кодировкой {encoding}: {e}")
    except OSError as e:
        raise FileOperationError(f"Ошибка ввода-вывода при чтении текстового файла '{path}': {e}")
    except Exception as e:
        raise FileOperationError(f"Неожиданная ошибка при чтении текстового файла '{path}': {e}")

def write_text_file(path, text, encoding='utf-8'):
    """
    Записывает текстовые данные в файл с заданной кодировкой.

    Args:
        path (str): Путь к файлу для записи.
        text (str): Текст для записи.
        encoding (str): Кодировка файла (по умолчанию utf-8).
    Raises:
        PermissionError: Если нет прав на запись.
        FileOperationError: Для других ошибок ввода-вывода.
    """
    try:
        with open(path, 'w', encoding=encoding) as f:
            f.write(text)
    except PermissionError:
        raise
    except OSError as e:
        raise FileOperationError(f"Ошибка ввода-вывода при записи текстового файла '{path}': {e}")
    except Exception as e:
        raise FileOperationError(f"Неожиданная ошибка при записи текстового файла '{path}': {e}")

def generate_random_bytes(n):
    """
    Генерирует n случайных байтов.

    Args:
        n (int): Количество байтов для генерации.

    Returns:
        bytes: Объект bytes, содержащий n случайных байтов.
    """
    # os.urandom не выбрасывает исключений в обычных условиях
    return os.urandom(n)
