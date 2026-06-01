"""
Симметричное шифрование: SM4-CBC (128-битный ключ).
Вариант 7 — алгоритм SM4.
"""

import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# Значения по умолчанию для SM4
SM4_BLOCK_SIZE_BITS = 128
SM4_KEY_SIZE_BYTES = 16
SM4_IV_SIZE_BYTES = 16

# Для обратной совместимости
BLOCK_SIZE_BITS = SM4_BLOCK_SIZE_BITS
KEY_SIZE_BYTES = SM4_KEY_SIZE_BYTES
IV_SIZE_BYTES = SM4_IV_SIZE_BYTES


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
    return os.urandom(KEY_SIZE_BYTES)


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом SM4-CBC с PKCS7-паддингом.
    
    Args:
        plaintext: Открытый текст для шифрования.
        key: Ключ SM4 размером 16 байт.
    
    Returns:
        IV (16 байт) + зашифрованный текст.
    """
    iv = os.urandom(IV_SIZE_BYTES)
    padder = padding.PKCS7(BLOCK_SIZE_BITS).padder()
    padded = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()

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
    iv = data[:IV_SIZE_BYTES]
    ciphertext = data[IV_SIZE_BYTES:]

    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(BLOCK_SIZE_BITS).unpadder()
    return unpadder.update(padded) + unpadder.finalize()
