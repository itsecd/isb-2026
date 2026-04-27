import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def generate_idea_key():
    """
    Генерирует ключ IDEA (16 байт)

    Returns:
        bytes
    """
    return os.urandom(16)


def encrypt_data(key, data):
    """
    Шифрует данные IDEA

    Returns:
        bytes
    """
    iv = os.urandom(8)

    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    return iv + encryptor.update(padded_data) + encryptor.finalize()


def decrypt_data(key, encrypted_data):
    """
    Дешифрует данные IDEA

    Returns:
        bytes
    """
    iv = encrypted_data[:8]
    data = encrypted_data[8:]

    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded = decryptor.update(data) + decryptor.finalize()

    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded) + unpadder.finalize()
