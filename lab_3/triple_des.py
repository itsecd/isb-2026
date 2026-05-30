"""Симметричное шифрование 3DES в режиме CBC."""

from __future__ import annotations

import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes

try:
    from cryptography.hazmat.decrepit.ciphers.algorithms import TripleDES
except ImportError:
    from cryptography.hazmat.primitives.ciphers.algorithms import TripleDES


def allowed_key_bits() -> tuple[int, int, int]:
    """Возвращает размеры ключа 3DES, допустимые для варианта лабораторной."""
    return 64, 128, 192


def block_bits() -> int:
    """Возвращает размер блока 3DES в битах."""
    return 64


def iv_size() -> int:
    """Возвращает размер вектора инициализации CBC в байтах."""
    return 8


def generate_key(key_bits: int = 192) -> bytes:
    """Генерирует случайный ключ 3DES.

    Аргументы:
        key_bits: Длина ключа в битах. Допустимые значения: 64, 128 и 192.

    Возвращает:
        Случайные байты ключа.
    """
    match key_bits in allowed_key_bits():
        case True:
            return os.urandom(key_bits // 8)
        case False:
            allowed = ", ".join(str(value) for value in allowed_key_bits())
            raise ValueError(f"Для 3DES допустимы размеры ключа: {allowed} бит")


def pad_data(data: bytes) -> bytes:
    """Дополняет данные до размера блока 3DES по схеме ANSI X.923."""
    padder = padding.ANSIX923(block_bits()).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(padded_data: bytes) -> bytes:
    """Удаляет дополнение ANSI X.923 из расшифрованных данных."""
    unpadder = padding.ANSIX923(block_bits()).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Шифрует байты алгоритмом 3DES-CBC.

    В начало результата записывается IV, поэтому файл можно расшифровать
    независимо при наличии того же симметричного ключа.
    """
    iv = os.urandom(iv_size())
    cipher = Cipher(TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(pad_data(plaintext)) + encryptor.finalize()
    return iv + ciphertext


def decrypt(payload: bytes, key: bytes) -> bytes:
    """Расшифровывает данные, полученные функцией encrypt."""
    match len(payload) <= iv_size():
        case True:
            raise ValueError("Зашифрованный файл не содержит IV и шифротекст")
        case False:
            iv = payload[:iv_size()]
            ciphertext = payload[iv_size():]

    cipher = Cipher(TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad_data(padded_plaintext)
