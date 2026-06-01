"""
Симметричное шифрование: SM4-CBC (128-битный ключ).
Вариант 7 — алгоритм SM4.
"""

import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


# SM4: размер блока и ключа — 128 бит (16 байт)
BLOCK_SIZE_BITS = 128
KEY_SIZE_BYTES = 16
IV_SIZE_BYTES = 16


def generate_symmetric_key() -> bytes:
    """Генерирует случайный ключ SM4 (128 бит)."""
    return os.urandom(KEY_SIZE_BYTES)


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом SM4-CBC с PKCS7-паддингом.
    Возвращает IV (16 байт) + шифртекст.
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
    Ожидает формат: IV (16 байт) + шифртекст.
    """
    iv = data[:IV_SIZE_BYTES]
    ciphertext = data[IV_SIZE_BYTES:]

    cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(BLOCK_SIZE_BITS).unpadder()
    return unpadder.update(padded) + unpadder.finalize()
