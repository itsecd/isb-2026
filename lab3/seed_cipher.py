"""
Модуль симметричного шифрования на основе алгоритма SEED.

Реализует блочный шифр SEED в режиме CBC с дополнением ANSI X.923.
Ключ: 128 бит (16 байт). Размер блока: 128 бит (16 байт).
"""

import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.decrepit.ciphers.algorithms import SEED
from exceptions import EncryptionError, DecryptionError


class SEEDCipher:
    """
    Класс, инкапсулирующий симметричное шифрование алгоритмом SEED.

    Атрибуты класса:
        BLOCK_SIZE (int): Размер блока в битах (128).
        KEY_SIZE (int): Размер ключа в байтах (16,
         что соответствует 128 битам).
        IV_SIZE (int): Размер вектора инициализации в байтах (16).

    Атрибуты экземпляра:
        _key (bytes): Секретный ключ шифрования (приватный).
        _iv (bytes | None): Вектор инициализации для текущей сессии.
    """

    BLOCK_SIZE: int = 128
    KEY_SIZE: int = 16
    IV_SIZE: int = 16

    def __init__(self, key: bytes) -> None:
        """
        Инициализирует шифр SEED с указанным ключом.

        Аргументы:
            key: Ключ шифрования длиной ровно KEY_SIZE байт.

        Исключения:
            ValueError: Если ключ имеет неверную длину.
        """
        if len(key) != self.KEY_SIZE:
            raise ValueError(
                f"Ключ SEED должен быть длиной {self.KEY_SIZE} байт "
                f"({self.KEY_SIZE * 8} бит). Получено: {len(key)} байт."
            )
        self._key = key
        self._iv = None

    @classmethod
    def generate_key(cls) -> bytes:
        """
        Генерирует криптографически безопасный случайный ключ SEED.

        Использует os.urandom,
         который получает энтропию от операционной системы.

        Возвращает:
            bytes: Случайный ключ длиной KEY_SIZE байт.
        """
        print(f"Генерация ключа SEED ({cls.KEY_SIZE * 8} бит)")
        return os.urandom(cls.KEY_SIZE)

    def set_iv(self, iv: bytes = None) -> bytes:
        """
        Устанавливает вектор инициализации для следующего шифрования.

        Если IV не передан, генерирует новый случайный.

        Аргументы:
            iv: Вектор инициализации (опционально). Если None, генерируется.

        Возвращает:
            bytes: Установленный IV.
        """
        if iv is None:
            iv = os.urandom(self.IV_SIZE)
        self._iv = iv
        return iv

    def _pad(self, data: bytes) -> bytes:
        """
        Дополняет данные до размера, кратного блоку, по стандарту ANSI X.923.

        Аргументы:
            data: Исходные данные.

        Возвращает:
            bytes: Дополненные данные.
        """
        padder = padding.ANSIX923(self.BLOCK_SIZE).padder()
        return padder.update(data) + padder.finalize()

    def _unpad(self, padded_data: bytes) -> bytes:
        """
        Удаляет дополнение ANSI X.923 из данных.

        Аргументы:
            padded_data: Данные с дополнением.

        Возвращает:
            bytes: Исходные данные без дополнения.
        """
        unpadder = padding.ANSIX923(self.BLOCK_SIZE).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()

    def encrypt(self, plaintext: bytes) -> bytes:
        """
        Шифрует данные алгоритмом SEED в режиме CBC.

        Требует предварительной установки IV через set_iv().

        Аргументы:
            plaintext: Открытый текст для шифрования.

        Возвращает:
            bytes: Зашифрованные данные.

        Исключения:
            EncryptionError: Если IV не установлен
             или произошла ошибка шифрования.
        """
        if self._iv is None:
            raise EncryptionError(
                "Вектор инициализации (IV) не установлен. "
                "Вызовите set_iv() перед шифрованием."
            )
        try:
            padded = self._pad(plaintext)
            cipher = Cipher(SEED(self._key), modes.CBC(self._iv))
            encryptor = cipher.encryptor()
            ciphertext = encryptor.update(padded) + encryptor.finalize()
            return ciphertext
        except Exception as exc:
            raise EncryptionError(
                f"Ошибка при шифровании SEED: {exc}"
            )

    def decrypt(self, ciphertext: bytes, iv: bytes) -> bytes:
        """
        Расшифровывает данные алгоритмом SEED в режиме CBC.

        Аргументы:
            ciphertext: Зашифрованные данные.
            iv: Вектор инициализации, использованный при шифровании.

        Возвращает:
            bytes: Расшифрованные данные (открытый текст).

        Исключения:
            DecryptionError: Если произошла ошибка расшифрования.
        """
        try:
            cipher = Cipher(SEED(self._key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded = decryptor.update(ciphertext) + decryptor.finalize()
            return self._unpad(padded)
        except Exception as exc:
            raise DecryptionError(
                f"Ошибка при расшифровании SEED: {exc}"
            )