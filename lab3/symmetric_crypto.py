"""
Модуль для симметричного шифрования с использованием AES.

Содержит класс AESCipher для шифрования и дешифрования данных
в режиме CBC с использованием PKCS7 padding.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from file_utils import generate_random_bytes

class AESCipher:
    """
    Класс для шифрования и дешифрования данных с помощью AES в режиме CBC.
    """

    def __init__(self, key):
        """
        Инициализирует объект AESCipher с заданным ключом.

        Args:
            key (bytes): Ключ AES длиной 16, 24 или 32 байта (128, 192, 256 бит).

        Raises:
            ValueError: Если длина ключа недействительна.
        """
        if len(key) not in [16, 24, 32]:  # 128, 192, 256 бит
            raise ValueError("Неправильный размер ключа AES")
        self.key = key

    def encrypt(self, plaintext, iv):
        """
        Шифрует данные с использованием AES-CBC.

        Args:
            plaintext (bytes): Открытый текст для шифрования.
            iv (bytes): Вектор инициализации (IV), должен быть 16 байт.

        Returns:
            bytes: Зашифрованный текст.
        """
        # 1. Создаем шифратор
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        
        # 2. Добавляем Padding (PKCS7 - самый стандартный вариант)
        # Используем PKCS7 вместо ANSIX923 для большей совместимости
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext) + padder.finalize()
        
        # 3. Шифруем дополненные данные
        return encryptor.update(padded_data) + encryptor.finalize()

    def decrypt(self, ciphertext, iv):
        """
        Расшифровывает данные, зашифрованные с помощью AES-CBC.

        Args:
            ciphertext (bytes): Зашифрованный текст.
            iv (bytes): Вектор инициализации (IV), который использовался при шифровании.

        Returns:
            bytes: Расшифрованный открытый текст.
        """
        # 1. Расшифровываем
        cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        
        # 2. Убираем Padding
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_plaintext) + unpadder.finalize()

def generate_aes_key(key_size_bits):
    """
    Генерирует случайный ключ AES заданного размера.

    Args:
        key_size_bits (int): Размер ключа в битах (128, 192 или 256).

    Returns:
        bytes: Сгенерированный ключ AES.
    """
    key_size_bytes = key_size_bits // 8
    return generate_random_bytes(key_size_bytes)
