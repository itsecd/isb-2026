import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_symmetric_key() -> bytes:
    """Генерирует случайный симметричный ключ SEED длиной 128 бит."""
    return os.urandom(16)


def encrypt_data(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    """
    Шифрует данные алгоритмом SEED.

    Args:
        data: данные для шифрования в байтах
        key: симметричный ключ длиной 16 байт
    """
    try:
        padder = padding.ANSIX923(128).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(16)
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_data) + encryptor.finalize()

        return iv, c_text
    except Exception as e:
        raise RuntimeError(f"Файл не зашифровался: {e}")


def decrypt_data(iv: bytes, c_text: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные алгоритмом SEED.

    Args:
        iv: вектор инициализации длиной 16 байт
        c_text: зашифрованные данные в байтах
        key: симметричный ключ длиной 16 байт
    """
    try:
        cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(c_text) + decryptor.finalize()

        unpadder = padding.ANSIX923(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
    except Exception as e:
        raise RuntimeError(f"Файл не расшифровался: {e}")