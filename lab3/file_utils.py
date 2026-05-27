"""
Модуль для работы с файлами.

Содержит функции для чтения/записи бинарных и текстовых файлов,
а также для генерации случайных байтов.
"""

import os

def read_binary_file(path):
    """
    Читает бинарные данные из файла.

    Args:
        path (str): Путь к файлу для чтения.

    Returns:
        bytes: Содержимое файла в виде байтов.
    """
    with open(path, 'rb') as f:
        return f.read()

def write_binary_file(path, data):
    """
    Записывает бинарные данные в файл.

    Args:
        path (str): Путь к файлу для записи.
        data (bytes): Данные для записи.
    """
    with open(path, 'wb') as f:
        f.write(data)

def read_text_file(path, encoding='utf-8'):
    """
    Читает текстовые данные из файла с заданной кодировкой.

    Args:
        path (str): Путь к файлу для чтения.
        encoding (str): Кодировка файла (по умолчанию utf-8).

    Returns:
        str: Содержимое файла в виде строки.
    """
    with open(path, 'r', encoding=encoding) as f:
        return f.read()

def write_text_file(path, text, encoding='utf-8'):
    """
    Записывает текстовые данные в файл с заданной кодировкой.

    Args:
        path (str): Путь к файлу для записи.
        text (str): Текст для записи.
        encoding (str): Кодировка файла (по умолчанию utf-8).
    """
    with open(path, 'w', encoding=encoding) as f:
        f.write(text)

def generate_random_bytes(n):
    """
    Генерирует n случайных байтов.

    Args:
        n (int): Количество байтов для генерации.

    Returns:
        bytes: Объект bytes, содержащий n случайных байтов.
    """
    return os.urandom(n)
