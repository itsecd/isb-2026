"""
Модуль для работы с симметричным шифрованием алгоритмом SM4.

Характеристики:
- Размер блока: 128 бит
- Размер ключа: 128 бит
- Количество раундов: 32
- Структура: обобщенная сеть Фейстеля
"""

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from typing import Tuple

from .io_utils import read_binary_file, write_binary_file


SM4_KEY_SIZE = 16
BLOCK_SIZE = 128


def generate_symmetric_key() -> bytes:
    """
    Генерирует случайный ключ для алгоритма SM4.
    
    Returns:
        bytes: Случайный ключ длиной 128 бит (16 байт).
        
    Note:
        Использует криптографически стойкий генератор псевдослучайных
        чисел из модуля os.urandom().
    """
    return os.urandom(SM4_KEY_SIZE)


def encrypt_sm4(plaintext: bytes, key: bytes) -> Tuple[bytes, bytes]:
    """
    Шифрует данные с использованием алгоритма SM4 в режиме CBC.
    
    Args:
        plaintext: Исходные данные для шифрования.
        key: Ключ шифрования длиной 128 бит.
        
    Returns:
        Tuple[bytes, bytes]: Кортеж из (iv, ciphertext), где:
            - iv: Вектор инициализации (16 байт)
            - ciphertext: Зашифрованные данные
            
    Raises:
        ValueError: Если длина ключа не равна 16 байтам.
        
    Algorithm:
        1. Применяется паддинг ANSIX923 для выравнивания данных
        2. Генерируется случайный IV
        3. Выполняется шифрование в режиме CBC
    """
    if len(key) != SM4_KEY_SIZE:
        raise ValueError(f"Key must be {SM4_KEY_SIZE} bytes, got {len(key)}")
    
    padder = padding.ANSIX923(BLOCK_SIZE).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    iv = os.urandom(16)

    cipher = Cipher(
        algorithms.SM4(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv, ciphertext


def decrypt_sm4(iv: bytes, ciphertext: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные с использованием алгоритма SM4 в режиме CBC.
    
    Args:
        iv: Вектор инициализации (16 байт).
        ciphertext: Зашифрованные данные.
        key: Ключ расшифрования длиной 128 бит.
        
    Returns:
        bytes: Расшифрованные данные без паддинга.
        
    Raises:
        ValueError: Если длина ключа не равна 16 байтам.
        ValueError: Если длина IV не равна 16 байтам.
        
    Algorithm:
        1. Выполняется дешифрование в режиме CBC
        2. Удаляется паддинг ANSIX923
    """
    if len(key) != SM4_KEY_SIZE:
        raise ValueError(f"Key must be {SM4_KEY_SIZE} bytes, got {len(key)}")
    if len(iv) != 16:
        raise ValueError(f"IV must be 16 bytes, got {len(iv)}")
    
    cipher = Cipher(
        algorithms.SM4(key),
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.ANSIX923(BLOCK_SIZE).unpadder()
    plaintext = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    return plaintext


def encrypt_file_sm4(input_path: str, output_path: str, key: bytes) -> None:
    """
    Шифрует файл с использованием алгоритма SM4.
    
    Args:
        input_path: Путь к исходному файлу.
        output_path: Путь для сохранения зашифрованного файла.
        key: Ключ шифрования длиной 128 бит.
        
    Note:
        Формат выходного файла: [IV (16 байт)][Ciphertext]
    """
    plaintext = read_binary_file(input_path)
    iv, ciphertext = encrypt_sm4(plaintext, key)
    write_binary_file(output_path, iv + ciphertext)


def decrypt_file_sm4(input_path: str, output_path: str, key: bytes) -> None:
    """
    Расшифровывает файл с использованием алгоритма SM4.
    
    Args:
        input_path: Путь к зашифрованному файлу.
        output_path: Путь для сохранения расшифрованного файла.
        key: Ключ расшифрования длиной 128 бит.
        
    Note:
        Ожидается формат входного файла: [IV (16 байт)][Ciphertext]
    """
    data = read_binary_file(input_path)
    iv = data[:16]
    ciphertext = data[16:]
    plaintext = decrypt_sm4(iv, ciphertext, key)
    write_binary_file(output_path, plaintext)