"""
Модуль симметричного шифрования на основе алгоритма SEED.

Реализует блочный шифр SEED в режиме CBC с дополнением ANSI X.923.
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.decrepit.ciphers.algorithms import SEED
from exceptions import EncryptionError, DecryptionError


class SEEDCipher:
    """
    Класс, инкапсулирующий симметричное шифрование алгоритмом SEED.

    Все параметры (размер блока, ключа, IV) передаются извне
    при создании экземпляра. Никакие значения не захардкожены.

    Атрибуты экземпляра:
        _key (bytes): Секретный ключ шифрования.
        _iv (bytes | None): Вектор инициализации.
        _block_size (int): Размер блока в битах.
        _iv_size (int): Размер IV в байтах.
    """

    def __init__(self, key: bytes, block_size: int, iv_size: int) -> None:
        """
        Инициализирует шифр SEED.

        Аргументы:
            key: Ключ шифрования.
            block_size: Размер блока в битах.
            iv_size: Размер вектора инициализации в байтах.

        Исключения:
            ValueError: Если ключ имеет неверную длину.
        """
        expected_key_size = iv_size
        if len(key) != expected_key_size:
            raise EncryptionError(
                f"Ключ SEED должен быть длиной {expected_key_size} байт. "
                f"Получено: {len(key)} байт."
            )
        self._key = key
        self._iv = None
        self._block_size = block_size
        self._iv_size = iv_size

    @staticmethod
    def generate_key(key_size: int) -> bytes:
        """
        Генерирует случайный ключ SEED.

        Аргументы:
            key_size: Размер ключа в байтах.

        Возвращает:
            bytes: Случайный ключ.
        """
        print(f"Генерация ключа SEED ({key_size * 8} бит)")
        return os.urandom(key_size)

    @property
    def iv_size(self) -> int:
        """Возвращает размер IV в байтах."""
        return self._iv_size

    def set_iv(self, iv: bytes = None) -> bytes:
        """
        Устанавливает вектор инициализации.

        Если IV не передан, генерирует новый случайный.

        Аргументы:
            iv: Вектор инициализации. Если None, генерируется.

        Возвращает:
            bytes: Установленный IV.
        """
        if iv is None:
            iv = os.urandom(self._iv_size)
        self._iv = iv
        return iv

    def _pad(self, data: bytes) -> bytes:
        """Дополняет данные до размера, кратного блоку."""
        padder = padding.ANSIX923(self._block_size).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, padded_data: bytes) -> bytes:
        """Удаляет дополнение."""
        unpadder = padding.ANSIX923(self._block_size).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Шифрует данные алгоритмом SEED в режиме CBC.

        Аргументы:
            plaintext: Открытый текст.

        Возвращает:
            bytes: Зашифрованные данные.

        Исключения:
            EncryptionError: Если IV не установлен.
        """
        if self._iv is None:
            raise EncryptionError(
                "Вектор инициализации не установлен."
                " Вызовите set_iv() перед шифрованием."
            )
        try:
            padded = self._pad(plaintext)
            cipher = Cipher(SEED(self._key), modes.CBC(self._iv))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded) + encryptor.finalize()
            return ciphertext
        except Exception as exc:
            raise EncryptionError(f"Ошибка при шифровании SEED: {exc}")

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """
        Расшифровывает данные алгоритмом SEED в режиме CBC.

        Аргументы:
            ciphertext: Зашифрованные данные.
            iv: Вектор инициализации.

        Возвращает:
            bytes: Расшифрованные данные.

        Исключения:
            DecryptionError: При ошибке расшифрования.
        """
        try:
            cipher = Cipher(SEED(self._key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded = decryptor.update(ciphertext) + decryptor.finalize()
            return self._unpad(padded)
        except Exception as exc:
            raise DecryptionError(f"Ошибка при расшифровании SEED: {exc}")