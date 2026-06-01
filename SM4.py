import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

BLOCK_SIZE = 16


def generate_sm4_key() -> bytes:
        """
        Генерирует случайный ключ для SM4 длиной BLOCK_SIZE (16 байт).

        Returns:
            bytes: случайный ключ.
        """
        return os.urandom(BLOCK_SIZE)

def sm4_encrypt(key: bytes, text: bytes) -> tuple:
        """
        Шифрует текст алгоритмом SM4 в режиме CBC с паддингом ANSIX923.

        Args:
            key (bytes): ключ шифрования, должен быть длиной 16 байт.
            text (bytes): открытый текст в виде байтов.

        Returns:
            tuple: (iv, ciphertext), где iv — вектор инициализации (16 байт),
                   ciphertext — зашифрованные данные.
        """

        iv = os.urandom(BLOCK_SIZE)
        cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
        padder = padding.ANSIX923(128).padder()
        padded_text = padder.update(text) + padder.finalize()
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_text) + encryptor.finalize()
        return iv,c_text

def sm4_decrypt(key: bytes, c_text: bytes, iv: bytes ) -> bytes:
        """
        Расшифровывает данные, зашифрованные SM4 в режиме CBC.

        Args:
            key (bytes): ключ шифрования (16 байт).
            c_text (bytes): зашифрованные данные.
            iv (bytes): вектор инициализации (16 байт).

        Returns:
            bytes: расшифрованный открытый текст.
        """

        cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))

        decryptor = cipher.decryptor()
        dc_text = decryptor.update(c_text) + decryptor.finalize()
        unpadder = padding.ANSIX923(128).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        return unpadded_dc_text
