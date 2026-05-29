import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from exceptions import (
    KeyGenerationError,
    EncryptionError,
    DecryptionError
)
from file_utils import read_bytes, write_bytes


def generate_cast5_key(
        key_size_bits: int,
        min_key_size: int,
        max_key_size: int,
        key_step: int
) -> bytes:
    """
    Генерирует случайный ключ для алгоритма CAST5.

    :param key_size_bits: Размер ключа в битах.
    :param min_key_size: Минимальный размер ключа.
    :param max_key_size: Максимальный размер ключа.
    :param key_step: Шаг изменения размера ключа.
    :return: Ключ в виде байтов.
    :raises KeyGenerationError: Если размер ключа некорректен.
    """
    try:
        match key_size_bits:
            case size if (
                min_key_size <= size <= max_key_size
                and size % key_step == 0
            ):
                return os.urandom(size // 8)

            case _:
                raise ValueError(
                    "Некорректный размер ключа CAST5"
                )

    except Exception as error:
        raise KeyGenerationError(
            f"Ошибка генерации ключа: {error}"
        ) from error


def encrypt_file_cast5(
        input_path: str,
        output_path: str,
        key: bytes,
        block_size: int,
        iv_size: int
) -> None:
    """
    Шифрует файл с помощью CAST5 в режиме CBC с PKCS7.

    :param input_path: Путь к исходному файлу.
    :param output_path: Путь к зашифрованному файлу.
    :param key: Ключ CAST5.
    :param block_size: Размер блока.
    :param iv_size: Размер IV.
    :raises EncryptionError: При ошибке шифрования.
    """
    try:
        data = read_bytes(input_path)

        padder = padding.PKCS7(block_size).padder()
        padded_data = (
            padder.update(data)
            + padder.finalize()
        )

        iv = os.urandom(iv_size)

        cipher = Cipher(
            algorithms.CAST5(key),
            modes.CBC(iv)
        )
        encryptor = cipher.encryptor()

        encrypted_data = (
            encryptor.update(padded_data)
            + encryptor.finalize()
        )

        write_bytes(
            output_path,
            iv + encrypted_data
        )

    except Exception as error:
        raise EncryptionError(
            f"Ошибка шифрования файла: {error}"
        ) from error


def decrypt_file_cast5(
        input_path: str,
        output_path: str,
        key: bytes,
        block_size: int,
        iv_size: int
) -> None:
    """
    Расшифровывает файл, зашифрованный CAST5.

    :param input_path: Путь к зашифрованному файлу.
    :param output_path: Путь к расшифрованному файлу.
    :param key: Ключ CAST5.
    :param block_size: Размер блока.
    :param iv_size: Размер IV.
    :raises DecryptionError: При ошибке дешифрования.
    """
    try:
        content = read_bytes(input_path)

        iv = content[:iv_size]
        encrypted_data = content[iv_size:]

        cipher = Cipher(
            algorithms.CAST5(key),
            modes.CBC(iv)
        )
        decryptor = cipher.decryptor()

        decrypted_padded = (
            decryptor.update(encrypted_data)
            + decryptor.finalize()
        )

        unpadder = padding.PKCS7(
            block_size
        ).unpadder()

        decrypted_data = (
            unpadder.update(decrypted_padded)
            + unpadder.finalize()
        )

        write_bytes(
            output_path,
            decrypted_data
        )

    except Exception as error:
        raise DecryptionError(
            f"Ошибка дешифрования: {error}"
        ) from error
