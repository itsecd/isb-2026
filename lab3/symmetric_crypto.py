"""
Модуль для симметричного шифрования с использованием AES.

Содержит класс AESCipher для шифрования и дешифрования данных
в режиме CBC с использованием PKCS7 padding.
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from file_utils import generate_random_bytes


class SymmetricCryptoError(Exception):
    """Исключение для ошибок, связанных с симметричным шифрованием (AES)."""
    pass

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
        if len(key) not in [16, 24, 32]:  
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

        Raises:
            SymmetricCryptoError: При ошибках шифрования (например, неверный IV).
        """
        try:
            
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
            encryptor = cipher.encryptor()
            
            
            
            padder = padding.PKCS7(128).padder()
            padded_data = padder.update(plaintext) + padder.finalize()
            
            
            return encryptor.update(padded_data) + encryptor.finalize()
        except Exception as e:
            
            
            raise SymmetricCryptoError(f"Ошибка шифрования AES: {e}")

    def decrypt(self, ciphertext, iv):
        """
        Расшифровывает данные, зашифрованные с помощью AES-CBC.

        Args:
            ciphertext (bytes): Зашифрованный текст.
            iv (bytes): Вектор инициализации (IV), который использовался при шифровании.

        Returns:
            bytes: Расшифрованный открытый текст.

        Raises:
            SymmetricCryptoError: При ошибках дешифрования (например, поврежденный шифртекст, неверный IV).
        """
        try:
            
            cipher = Cipher(algorithms.AES(self.key), modes.CBC(iv))
            decryptor = cipher.decryptor()
            padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
            
            
            unpadder = padding.PKCS7(128).unpadder()
            plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
            return plaintext
        except ValueError as e: 
             
             raise SymmetricCryptoError(f"Ошибка дешифрования AES: {e}")
        except Exception as e:
             
             raise SymmetricCryptoError(f"Общая ошибка дешифрования AES: {e}")

def generate_aes_key(key_size_bits):
    """
    Генерирует случайный ключ AES заданного размера.

    Args:
        key_size_bits (int): Размер ключа в битах (128, 192 или 256).

    Returns:
        bytes: Сгенерированный ключ AES.

    Raises:
        ValueError: Если размер ключа недействителен.
    """
    valid_sizes = [128, 192, 256]
    if key_size_bits not in valid_sizes:
        raise ValueError(f"Недопустимый размер ключа AES: {key_size_bits}. Допустимые значения: {valid_sizes}")
    key_size_bytes = key_size_bits // 8
    return generate_random_bytes(key_size_bytes)
