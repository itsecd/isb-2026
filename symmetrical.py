import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, modes, algorithms
from cryptography.hazmat.primitives.ciphers.algorithms import SEED


def generate_sym_key() -> bytes:
    """
    Генерирует случайный 128-битный ключ для алгоритма SEED.

    Returns:
        bytes: Симметричный ключ длиной 16 байт.
    """
    print("Ключ для симметричного шифрования создан")
    return os.urandom(16)


def encryption_data(data: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом SEED в режиме CBC с использованием PKCS7 padding.

    Args:
        data (bytes): Исходные данные для шифрования.
        key (bytes): Симметричный ключ (16 байт).

    Returns:
        bytes: Конкатенация вектора инициализации (IV) и зашифрованных данных.
    """
    iv = os.urandom(16)
    cipher = Cipher(SEED(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    pad_data = padder.update(data) + padder.finalize()

    e_data = encryptor.update(pad_data) + encryptor.finalize()

    print("Данные при помощи симметричного ключа успешно зашифрованы")
    return iv + e_data


def decryption_data(data: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные, защищенные алгоритмом SEED в режиме CBC.

    Args:
        data (bytes): Зашифрованные данные, начинающиеся с 16-байтного IV.
        key (bytes): Симметричный ключ, использованный при шифровании.

    Returns:
        bytes: Исходные расшифрованные данные без дополнения (padding).

    Raises:
        ValueError: Если дополнение (padding) некорректно или данные повреждены.
    """
    iv = data[:16]
    cipher_data = data[16:]

    cipher = Cipher(SEED(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    d_data = decryptor.update(cipher_data) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    unpad_d_data = unpadder.update(d_data) + unpadder.finalize()

    print("Данные при помощи симметричного ключа успешно дешифрованы")
    return unpad_d_data
