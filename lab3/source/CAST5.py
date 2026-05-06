import os

from cryptography.hazmat.primitives import padding as sym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_key(size_bytes: int) -> bytes:
    """
    Генерирует симметричный ключ CAST5.

    Parameters
    ----------
    size_bytes : int
        Размер ключа в байтах (допустимо 5–16).

    Returns
    -------
    bytes
        Случайный симметричный ключ.
    """
    if not (5 <= size_bytes <= 16):
        raise ValueError("CAST5 key must be 5–16 bytes")
    return os.urandom(size_bytes)


def encrypt(key: bytes, data: bytes) -> bytes:
    """
    Шифрует данные алгоритмом CAST5 в режиме CBC с PKCS7 padding.

    Parameters
    ----------
    key : bytes
        Симметричный ключ CAST5.
    data : bytes
        Исходные данные для шифрования.

    Returns
    -------
    bytes
        IV + ciphertext.
    """
    iv = os.urandom(8)

    padder = sym_padding.PKCS7(64).padder()
    padded = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    ciphertext = encryptor.update(padded) + encryptor.finalize()
    return iv + ciphertext


def decrypt(key: bytes, data: bytes) -> bytes:
    """
    Расшифровывает данные алгоритмом CAST5 в режиме CBC и удаляет PKCS7 padding.

    Parameters
    ----------
    key : bytes
        Симметричный ключ CAST5.
    data : bytes
        Данные формата IV + ciphertext.

    Returns
    -------
    bytes
        Исходные (расшифрованные) данные.
    """
    iv = data[:8]
    ciphertext = data[8:]

    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(64).unpadder()
    return unpadder.update(padded) + unpadder.finalize()