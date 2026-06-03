"""Модуль для работы с симметричным шифром Camellia."""

"""Модуль для работы с симметричным блочным шифром Camellia."""

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_camellia_key(key_size_bits: int) -> bytes:
    """Генерирует случайный ключ Camellia заданной длины.

    Args:
        key_size_bits: Размер ключа в битах (128, 192 или 256).

    Returns:
        bytes: Случайный ключ длиной key_size_bits // 8 байт.
    """
    if key_size_bits not in (128, 192, 256):
        raise ValueError("key_size_bits должен быть 128, 192 или 256")
    return os.urandom(key_size_bits // 8)


def encrypt_bytes(data: bytes, key: bytes, block_size_bits: int, block_size_bytes: int) -> bytes:
    """Шифрует данные с помощью Camellia-CBC с паддингом ANSIX923.

    Args:
        data: Открытые данные (байты) произвольной длины.
        key: Ключ Camellia (16, 24 или 32 байта).
        block_size_bits: Размер блока в битах (для Camellia всегда 128).
        block_size_bytes: Размер блока в байтах (16).

    Returns:
        bytes: IV (block_size_bytes) + зашифрованные данные.
    """
    padder = padding.ANSIX923(block_size_bits).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(block_size_bytes)
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext


def decrypt_bytes(file_content: bytes, key: bytes, block_size_bits: int, block_size_bytes: int) -> bytes:
    """Расшифровывает данные, извлекая IV из начала.

    Args:
        file_content: Байты вида IV (block_size_bytes) + криптотекст.
        key: Ключ Camellia (16, 24 или 32 байта).
        block_size_bits: Размер блока в битах.
        block_size_bytes: Размер блока в байтах.

    Returns:
        bytes: Расшифрованные открытые данные.
    """
    if len(file_content) < block_size_bytes:
        raise ValueError("Зашифрованный файл поврежден или слишком мал.")

    iv = file_content[:block_size_bytes]
    ciphertext = file_content[block_size_bytes:]

    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.ANSIX923(block_size_bits).unpadder()
    return unpadder.update(decrypted_padded_data) + unpadder.finalize()
