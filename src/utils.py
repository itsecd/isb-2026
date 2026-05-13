from cryptography.hazmat.primitives import padding
from typing import Optional


def read_binary_file(filepath: str) -> bytes:
    """
    Чтение бинарного файла.
    
    Args:
        filepath (str): Путь к файлу для чтения
    
    Returns:
        bytes: Содержимое файла в виде байтов
    
    Raises:
        FileNotFoundError: Если файл не существует
        PermissionError: Если нет прав на чтение файла
        IOError: При ошибках ввода-вывода
    
    Example:
        >>> data = read_binary_file('keys/symmetric.key')
        >>> len(data)
        32
    """
    with open(filepath, 'rb') as f:
        return f.read()


def write_binary_file(filepath: str, data: bytes) -> None:
    """
    Запись бинарного файла.
    
    Args:
        filepath (str): Путь для сохранения файла
        data (bytes): Данные для записи
    
    Returns:
        None
    
    Raises:
        PermissionError: Если нет прав на запись
        IOError: При ошибках ввода-вывода
    
    Example:
        >>> write_binary_file('output.bin', b'\\x00\\x01\\x02')
    """
    with open(filepath, 'wb') as f:
        f.write(data)


def read_text_file(filepath: str) -> bytes:
    """
    Чтение текстового файла в байтовом режиме.
    
    Файл читается в бинарном режиме для сохранения исходной кодировки.
    
    Args:
        filepath (str): Путь к текстовому файлу
    
    Returns:
        bytes: Содержимое файла в виде байтов
    
    Raises:
        FileNotFoundError: Если файл не существует
        PermissionError: Если нет прав на чтение
        IOError: При ошибках ввода-вывода
    
    Example:
        >>> content = read_text_file('data/plaintext.txt')
        >>> print(content.decode('utf-8'))
        Hello World
    """
    with open(filepath, 'rb') as f:
        return f.read()


def write_text_file(filepath: str, data: bytes) -> None:
    """
    Запись текстового файла из байтовых данных.
    
    Данные записываются в бинарном режиме для сохранения исходной кодировки.
    
    Args:
        filepath (str): Путь для сохранения файла
        data (bytes): Данные для записи
    
    Returns:
        None
    
    Raises:
        PermissionError: Если нет прав на запись
        IOError: При ошибках ввода-вывода
    
    Example:
        >>> write_text_file('output.txt', b'Hello World')
    """
    with open(filepath, 'wb') as f:
        f.write(data)


def pad_data(data: bytes, block_size: int = 16) -> bytes:
    """
    Дополнение данных до размера блока по стандарту ANSI X.923.
    
    ANSI X.923 заполняет блок нулями, а последний байт указывает количество байт дополнения.
    
    Args:
        data (bytes): Исходные данные для дополнения
        block_size (int): Размер блока в байтах. По умолчанию 16 (128 бит)
    
    Returns:
        bytes: Данные с добавленным дополнением
    
    Raises:
        ValueError: Если block_size <= 0
    
    Example:
        >>> padded = pad_data(b'Hello', 16)
        >>> len(padded) % 16
        0
        >>> padded[-1]  # последний байт содержит количество добавленных байт
        11
    """
    padder = padding.ANSIX923(block_size * 8).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(data: bytes, block_size: int = 16) -> bytes:
    """
    Удаление дополнения из данных по стандарту ANSI X.923.
    
    Args:
        data (bytes): Данные с дополнением
        block_size (int): Размер блока в байтах. По умолчанию 16 (128 бит)
    
    Returns:
        bytes: Исходные данные без дополнения
    
    Raises:
        ValueError: Если данные повреждены или имеют неверное дополнение
    
    Example:
        >>> original = b'Hello'
        >>> padded = pad_data(original, 16)
        >>> unpadded = unpad_data(padded, 16)
        >>> original == unpadded
        True
    """
    unpadder = padding.ANSIX923(block_size * 8).unpadder()
    return unpadder.update(data) + unpadder.finalize()