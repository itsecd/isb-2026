"""
Модуль симметричного шифрования (SEED, 128 бит).
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


class SymmetricCipher:
    """Класс для работы с алгоритмом SEED."""

    BLOCK_SIZE = 128
    KEY_SIZE = 16

    @staticmethod
    def encrypt(data: bytes, key: bytes) -> bytes:
        """Шифрует данные алгоритмом SEED."""
        if not isinstance(data, bytes):
            raise TypeError("Данные должны быть в формате bytes.")

        if len(key) != SymmetricCipher.KEY_SIZE:
            raise ValueError("Ключ SEED должен быть длиной 16 байт.")

        try:
            iv = os.urandom(16)

            padder = padding.PKCS7(SymmetricCipher.BLOCK_SIZE).padder()
            padded = padder.update(data) + padder.finalize()

            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            encryptor = cipher.encryptor()

            ciphertext = encryptor.update(padded) + encryptor.finalize()
            return iv + ciphertext

        except Exception as exc:
            raise RuntimeError(f"Ошибка шифрования SEED: {exc}") from exc

    @staticmethod
    def decrypt(data: bytes, key: bytes) -> bytes:
        """Дешифрует данные алгоритмом SEED."""
        if len(key) != SymmetricCipher.KEY_SIZE:
            raise ValueError("Ключ SEED должен быть длиной 16 байт.")

        if len(data) < 16:
            raise ValueError("Некорректно зашифрованные данные.")

        try:
            iv = data[:16]
            ciphertext = data[16:]

            cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            padded = decryptor.update(ciphertext) + decryptor.finalize()

            unpadder = padding.PKCS7(SymmetricCipher.BLOCK_SIZE).unpadder()
            return unpadder.update(padded) + unpadder.finalize()

        except Exception as exc:
            raise RuntimeError(f"Ошибка дешифрования SEED: {exc}") from exc