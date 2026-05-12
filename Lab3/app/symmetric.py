
"""
Модуль симметричной криптографии CAST5.
"""

import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from app.file_utils import write_bytes, read_bytes


def generate_cast5_key(key_size_bits: int) -> bytes:
    """
    Генерирует ключ CAST5.

    :param key_size_bits: длина ключа в битах
    :return: симметричный ключ
    """
    try:
        if key_size_bits < 40 or key_size_bits > 128 or key_size_bits % 8 != 0:
            raise ValueError("Неверная длина ключа CAST5")

        return os.urandom(key_size_bits // 8)

    except Exception as error:
        print(f"Ошибка генерации ключа CAST5: {error}")
        raise


def pad_data(data: bytes, block_size: int = 64) -> bytes:
    """
    Добавляет padding к данным.

    :param data: исходные данные
    :param block_size: размер блока
    :return: дополненные данные
    """
    try:
        padder = padding.PKCS7(block_size).padder()
        return padder.update(data) + padder.finalize()

    except Exception as error:
        print(f"Ошибка padding: {error}")
        raise


def unpad_data(data: bytes, block_size: int = 64) -> bytes:
    """
    Удаляет padding из данных.

    :param data: данные с padding
    :param block_size: размер блока
    :return: исходные данные
    """
    try:
        unpadder = padding.PKCS7(block_size).unpadder()
        return unpadder.update(data) + unpadder.finalize()

    except Exception as error:
        print(f"Ошибка unpadding: {error}")
        raise


def encrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Шифрует файл алгоритмом CAST5.

    :param input_path: путь к исходному файлу
    :param output_path: путь к зашифрованному файлу
    :param key: симметричный ключ
    """
    try:
        data = read_bytes(input_path)

        padded_data = pad_data(data)

        iv = os.urandom(8)

        cipher = Cipher(
            algorithms.CAST5(key),
            modes.CBC(iv)
        )

        encryptor = cipher.encryptor()

        encrypted = encryptor.update(padded_data) + encryptor.finalize()

        write_bytes(output_path, iv + encrypted)

    except Exception as error:
        print(f"Ошибка шифрования файла: {error}")
        raise


def decrypt_file(input_path: str, output_path: str, key: bytes) -> None:
    """
    Дешифрует файл алгоритмом CAST5.

    :param input_path: путь к зашифрованному файлу
    :param output_path: путь к расшифрованному файлу
    :param key: симметричный ключ
    """
    try:
        encrypted_data = read_bytes(input_path)

        iv = encrypted_data[:8]
        ciphertext = encrypted_data[8:]

        cipher = Cipher(
            algorithms.CAST5(key),
            modes.CBC(iv)
        )

        decryptor = cipher.decryptor()

        padded = decryptor.update(ciphertext) + decryptor.finalize()

        decrypted = unpad_data(padded)

        write_bytes(output_path, decrypted)

    except Exception as error:
        print(f"Ошибка дешифрования файла: {error}")
        raise
