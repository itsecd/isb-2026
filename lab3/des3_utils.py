import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_key(key_size: int = 192) -> bytes:
    '''Генерирует случайный ключ алгоритма 3DES.

    Args:
        key_size (int): Размер ключа в битах (64, 128 или 192).

    Returns:
        bytes: Случайный ключ 3DES.

    Raises:
        ValueError: Если key_size не равен 64, 128 или 192.
    '''
    if key_size not in (64, 128, 192):
        raise ValueError(f"Недопустимый размер ключа: {key_size}")
    return os.urandom(key_size // 8)


def pad_data(data: bytes) -> bytes:
    '''Дополняет данные до кратности блоку 8 байт по схеме ANSI X.923.

    Args:
        data (bytes): Исходные данные.

    Returns:
        bytes: Дополненные данные.
    '''
    padder = padding.ANSIX923(64).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(padded_data: bytes) -> bytes:
    '''Убирает дополнение ANSI X.923.

    Args:
        padded_data (bytes): Данные с дополнением.

    Returns:
        bytes: Исходные данные без дополнения.
    '''
    unpadder = padding.ANSIX923(64).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def encrypt(data: bytes, key: bytes) -> tuple:
    '''Шифрует данные алгоритмом 3DES в режиме CBC.

    Args:
        data (bytes): Открытый текст.
        key (bytes): Ключ 3DES.

    Returns:
        tuple: Кортеж (iv: bytes, шифротекст: bytes), где iv — вектор инициализации (8 байт).
    '''
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    return iv, encrypted


def decrypt(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    '''Расшифровывает данные алгоритмом 3DES в режиме CBC.

    Args:
        encrypted_data (bytes): Зашифрованные данные.
        key (bytes): Ключ 3DES.
        iv (bytes): Вектор инициализации (8 байт).

    Returns:
        bytes: Расшифрованные данные с паддингом.
    '''
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()