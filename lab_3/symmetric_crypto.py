import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms

import constants as const


def generate_symmetric_key() -> bytes:
    """Генерирует случайный ключ для ChaCha20 (256 бит = 32 байта)"""
    return os.urandom(const.SYMMETRIC_KEY_SIZE)


def generate_nonce() -> bytes:
    """Генерирует случайное одноразовое число (nonce) для ChaCha20 (128 бит = 16 байт)"""
    return os.urandom(const.NONCE_SIZE)


def encrypt_symmetric(plaintext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Шифрование данных с помощью ChaCha20"""
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    encryptor = cipher.encryptor()
    return encryptor.update(plaintext) + encryptor.finalize()


def decrypt_symmetric(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    """Расшифрование данных с помощью ChaCha20"""
    cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()