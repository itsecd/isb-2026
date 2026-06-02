"""
Модуль для симметричного шифрования алгоритмом Blowfish.

Blowfish - блочный криптографический алгоритм, разработанный Брюсом Шнайером в 1993 году.
Использует режим CBC (Cipher Block Chaining) с PKCS7 padding.

Характеристики:
- Размер блока: 64 бита (8 байт)
- Размер ключа: 32-448 бит
- Вектор инициализации (IV): 64 бита
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os


def encrypt_message(encryption_key: bytes, plaintext: str) -> bytes:
    """
    Шифрование сообщения алгоритмом Blowfish.
    
    Args:
        encryption_key: Ключ шифрования (от 4 до 56 байт).
        plaintext: Исходное сообщение для шифрования.
        
    Returns:
        bytes: Зашифрованные данные (IV + ciphertext).
        
    Note:
        Возвращает конкатенацию вектора инициализации (IV) и зашифрованного текста.
        IV необходим для расшифровки и занимает первые 8 байт результата.
    """
    initialization_vector = os.urandom(8)
    blowfish_cipher = Cipher(
        algorithms.Blowfish(encryption_key),
        modes.CBC(initialization_vector),
        backend=default_backend()
    )
    
    message_bytes = plaintext.encode("utf-8")
    padder = padding.PKCS7(64).padder()
    padded_message = padder.update(message_bytes) + padder.finalize()
    encryptor = blowfish_cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    return initialization_vector + ciphertext


def decrypt_message(decryption_key: bytes, encrypted_data: bytes) -> str:
    """
    Расшифровка сообщения алгоритмом Blowfish.
    
    Args:
        decryption_key: Ключ расшифровки (должен совпадать с ключом шифрования).
        encrypted_data: Зашифрованные данные (IV + ciphertext).
        
    Returns:
        str: Расшифрованное сообщение.
        
    Note:
        Первые 8 байт encrypted_data интерпретируются как вектор инициализации (IV).
    """
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    blowfish_cipher = Cipher(
        algorithms.Blowfish(decryption_key), 
        modes.CBC(iv),
        backend=default_backend()
    )
    decryptor = blowfish_cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
    return plaintext_bytes.decode("utf-8")