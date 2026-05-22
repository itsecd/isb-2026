
"""
Модуль симметричного шифрования (Blowfish)
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def validate_blowfish_key_length(key_length: int) -> int:
    """
    Проверяет корректность длины ключа для алгоритма Blowfish.
    
    Args:
        key_length: Длина ключа в битах.
    
    Returns:
        Проверенную длину ключа в байтах.
    
    Raises:
        ValueError: Если длина ключа не соответствует требованиям Blowfish.
    """
    if key_length < 32 or key_length > 448:
        raise ValueError(f"Длина ключа Blowfish должна быть от 32 до 448 бит, получено {key_length} бит")
    
    if key_length % 8 != 0:
        raise ValueError(f"Длина ключа Blowfish должна быть кратна 8 битам, получено {key_length} бит")
    
    return key_length // 8


def generate_symmetric_key(key_length_bits: int = 128) -> bytes:
    """
    Генерирует ключ для симметричного алгоритма Blowfish.
    
    Args:
        key_length_bits: Длина ключа в битах (от 32 до 448, кратно 8).
    
    Returns:
        Случайный ключ для алгоритма Blowfish.
    """
    key_length_bytes = validate_blowfish_key_length(key_length_bits)
    return os.urandom(key_length_bytes)


def encrypt_symmetric(symmetric_key: bytes, plaintext_bytes: bytes) -> tuple:
    """
    Шифрует данные симметричным алгоритмом Blowfish в режиме CBC.
    
    Args:
        symmetric_key: Ключ Blowfish.
        plaintext_bytes: Открытые данные для шифрования.
    
    Returns:
        Кортеж (iv, ciphertext).
    """
    if not plaintext_bytes:
        raise ValueError("Нет данных для шифрования")
    
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.ANSIX923(64).padder()
    padded_data = padder.update(plaintext_bytes) + padder.finalize()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext


def decrypt_symmetric(symmetric_key: bytes, iv: bytes, ciphertext_bytes: bytes) -> bytes:
    """
    Расшифровывает данные симметричным алгоритмом Blowfish в режиме CBC.
    
    Args:
        symmetric_key: Ключ Blowfish.
        iv: Вектор инициализации длиной 8 байт.
        ciphertext_bytes: Зашифрованные данные.
    
    Returns:
        Расшифрованные данные.
    """
    if len(iv) != 8:
        raise ValueError(f"IV для Blowfish должен быть 8 байт, получено {len(iv)} байт")
    
    if not ciphertext_bytes:
        raise ValueError("Нет данных для дешифрования")
    
    cipher = Cipher(algorithms.Blowfish(symmetric_key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    padded_plaintext = decryptor.update(ciphertext_bytes) + decryptor.finalize()
    
    unpadder = padding.ANSIX923(64).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext


def save_symmetric_key(key: bytes, filepath: str) -> None:
    """Сохраняет симметричный ключ в файл."""
    with open(filepath, 'wb') as f:
        f.write(key)


def load_symmetric_key(filepath: str) -> bytes:
    """Загружает симметричный ключ из файла."""
    with open(filepath, 'rb') as f:
        key = f.read()
    if not key:
        raise ValueError(f"Файл {filepath} пуст")
    return key