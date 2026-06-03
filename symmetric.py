"""Модуль для работы с симметричным шифром Camellia."""

import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

CAMELLIA_BLOCK_SIZE_BITS = 128
CAMELLIA_BLOCK_SIZE_BYTES = 16


def generate_camellia_key(key_size_bits: int) -> bytes:
    """Генерирует случайный ключ Camellia заданной длины."""
    return os.urandom(key_size_bits // 8)


def encrypt_bytes(data: bytes, key: bytes) -> bytes:
    """Выполняет паддинг и шифрует данные алгоритмом Camellia-CBC.

    Возвращает IV, склеенный с криптотекстом.
    """
    padder = padding.ANSIX923(CAMELLIA_BLOCK_SIZE_BITS).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(CAMELLIA_BLOCK_SIZE_BYTES)
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext


def decrypt_bytes(file_content: bytes, key: bytes) -> bytes:
    """Разделяет IV и криптотекст, расшифровывает Camellia и снимает паддинг."""
    if len(file_content) < CAMELLIA_BLOCK_SIZE_BYTES:
        raise ValueError("Зашифрованный файл поврежден или слишком мал.")

    iv = file_content[:CAMELLIA_BLOCK_SIZE_BYTES]
    ciphertext = file_content[CAMELLIA_BLOCK_SIZE_BYTES:]

    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    decrypted_padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.ANSIX923(CAMELLIA_BLOCK_SIZE_BITS).unpadder()
    return unpadder.update(decrypted_padded_data) + unpadder.finalize()