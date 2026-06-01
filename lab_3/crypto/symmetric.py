"""
Симметричное шифрование: SM4-CBC (128-битный ключ).
Вариант 7 — алгоритм SM4.
"""

import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


BLOCK_SIZE_BITS = None
KEY_SIZE_BYTES = None
IV_SIZE_BYTES = None


def set_parameters(block_size_bits: int, key_size_bytes: int, iv_size_bytes: int) -> None:
    """
    Устанавливает параметры криптографии из конфигурации.
    
    Args:
        block_size_bits: Размер блока SM4 в битах.
        key_size_bytes: Размер ключа SM4 в байтах.
        iv_size_bytes: Размер IV в байтах.
    """
    global BLOCK_SIZE_BITS, KEY_SIZE_BYTES, IV_SIZE_BYTES
    BLOCK_SIZE_BITS = block_size_bits
    KEY_SIZE_BYTES = key_size_bytes
    IV_SIZE_BYTES = iv_size_bytes


def generate_symmetric_key() -> bytes:
    """Генерирует случайный ключ SM4 (128 бит)."""
    if KEY_SIZE_BYTES is None:
        raise RuntimeError("Параметры SM4 не заданы. Проверьте файл настроек.")
    try:
        return os.urandom(KEY_SIZE_BYTES)
    except ValueError as e:
        raise RuntimeError(f"Неверный размер ключа SM4: {e}")


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом SM4-CBC с PKCS7-паддингом.
    
    Args:
        plaintext: Открытый текст для шифрования.
        key: Ключ SM4 размером 16 байт.
    
    Returns:
        IV (16 байт) + зашифрованный текст.
    """
    if IV_SIZE_BYTES is None or BLOCK_SIZE_BITS is None:
        raise RuntimeError("Параметры SM4 не заданы. Проверьте файл настроек.")
    try:
        iv = os.urandom(IV_SIZE_BYTES)
        padder = padding.PKCS7(BLOCK_SIZE_BITS).padder()
        padded = padder.update(plaintext) + padder.finalize()

        cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded) + encryptor.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании SM4: {e}")

    return iv + ciphertext


def decrypt(data: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные алгоритмом SM4-CBC.
    
    Args:
        data: Данные в формате IV (16 байт) + шифртекст.
        key: Ключ SM4 размером 16 байт.
    
    Returns:
        Расшифрованный открытый текст.
    """
    if IV_SIZE_BYTES is None or BLOCK_SIZE_BITS is None:
        raise RuntimeError("Параметры SM4 не заданы. Проверьте файл настроек.")
    try:
        iv = data[:IV_SIZE_BYTES]
        ciphertext = data[IV_SIZE_BYTES:]

        cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = padding.PKCS7(BLOCK_SIZE_BITS).unpadder()
        return unpadder.update(padded) + unpadder.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка при расшифровке SM4: {e}")
