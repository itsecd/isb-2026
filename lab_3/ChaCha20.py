import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def generate_chacha20_key():
    """
    Создание 256-битного симметричного ключа.

    Returns:
        Случайная последовательность из 32 байт.
    """
    return os.urandom(32)


def generate_nonce():
    """
    Создание 128-битного одноразового номера nonce.

    Returns:
        Случайная последовательность из 16 байт.
    """
    return os.urandom(16)
 

def encrypt_with_chacha20_cipher(data: bytes, key: bytes, nonce: bytes):
    """
    Шифрование данных с использованием потокового шифра ChaCha20.

    Args:
        data: Исходные данные в байтах.
        key: Симметричный ключ (32 байта).
        nonce: Одноразовый номер (16 байт).

    Returns:
        Зашифрованные данные в байтах.

    Raises:
        RuntimeError: Ошибка в процессе шифрования.
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        encryptor = cipher.encryptor()
        return encryptor.update(data)
    except Exception as e:
        raise RuntimeError(f"ChaCha20 encryption error: {e}")


def decrypt_with_chacha20_cipher(data: bytes, key: bytes, nonce: bytes):
    """
    Расшифровка данных с использованием потокового шифра ChaCha20.

    Args:
        data: Зашифрованные данные в байтах.
        key: Симметричный ключ (32 байта).
        nonce: Одноразовый номер (16 байт).

    Returns:
        Расшифрованные данные в байтах.

    Raises:
        RuntimeError: Ошибка в процессе расшифровки.
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        decryptor = cipher.decryptor()
        return decryptor.update(data)
    except Exception as e:
        raise RuntimeError(f"ChaCha20 decryption error: {e}")