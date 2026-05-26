import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def generate_key():
    """
    Генерирует случайный 128-битный ключ для IDEA.

    Выходные данные:
        bytes: 16 байт ключа.
    """
    return os.urandom(16)

def encrypt_data(key, plaintext):
    """
    Шифрует данные с использованием IDEA в режиме CBC с PKCS7 паддингом.

    Входные данные:
        key (bytes): Ключ шифрования (16 байт).
        plaintext (bytes): Открытые данные.

    Выходные данные:
        bytes: Зашифрованные данные (IV + шифротекст).
    """
    iv = os.urandom(8)  
    padder = padding.PKCS7(64).padder()  
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def decrypt_data(key, encrypted_data):
    """
    Расшифровывает данные, зашифрованные encrypt_data.

    Входные данные:
        key (bytes): Ключ шифрования (16 байт).
        encrypted_data (bytes): Зашифрованные данные (IV + шифротекст).

    Выходные данные:
        bytes: Расшифрованные открытые данные.
    """
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded_plaintext) + unpadder.finalize()