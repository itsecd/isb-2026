"""
Модуль симметричного шифрования (SEED, 128 бит).
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class SymmetricCipher:
    """Класс для работы с алгоритмом SEED."""

    @staticmethod
    def encrypt(data: bytes, key: bytes, block_size: int, key_size: int) -> bytes:
        """
        Args:
            data: bytes - открытые данные
            key: bytes - ключ шифрования (key_size байт)
            block_size: int - размер блока в битах
            key_size: int - размер ключа в байтах

        Returns:
            bytes - iv (16 байт) + шифротекст

        Raises:
            TypeError: data не bytes
            ValueError: неверная длина ключа
            RuntimeError: ошибка шифрования
        """
        if not isinstance(data, bytes):
            raise TypeError("Данные должны быть в формате bytes.")

        if len(key) != key_size:
            raise ValueError(f"Ключ SEED должен быть длиной {key_size} байт.")

        try:
            iv = os.urandom(16)

            padder = padding.PKCS7(block_size).padder()
            padded = padder.update(data) + padder.finalize()

            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            ciphertext = encryptor.update(padded) + encryptor.finalize()
            return iv + ciphertext

        except Exception as exc:
            raise RuntimeError(f"Ошибка шифрования SEED: {exc}") from exc

    @staticmethod
    def decrypt(data: bytes, key: bytes, block_size: int, key_size: int) -> bytes:
        """
        Args:
            data: bytes - iv (16 байт) + шифротекст
            key: bytes - ключ шифрования (key_size байт)
            block_size: int - размер блока в битах
            key_size: int - размер ключа в байтах

        Returns:
            bytes - расшифрованные данные

        Raises:
            ValueError: неверная длина ключа или данных
            RuntimeError: ошибка дешифрования
        """
        if len(key) != key_size:
            raise ValueError(f"Ключ SEED должен быть длиной {key_size} байт.")

        if len(data) < 16:
            raise ValueError("Некорректно зашифрованные данные.")

        try:
            iv = data[:16]
            ciphertext = data[16:]

            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            padded = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(block_size).unpadder()
            return unpadder.update(padded) + unpadder.finalize()

        except Exception as exc:
            raise RuntimeError(f"Ошибка дешифрования SEED: {exc}") from exc