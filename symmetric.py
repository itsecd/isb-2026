import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


def encrypt_text(text: str, key: bytes) -> bytes:
    """
    Шифрование текста алгоритмом AES-CBC

    принимает:
        text: Исходный текст для шифрования
        key: Симметричный ключ AES (16, 24 или 32 байта)

    возвращает:
        bytes: Зашифрованные данные (IV + ciphertext)
    """
    data = text.encode('utf-8')
    
    padder = sym_padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    return iv + ciphertext


def decrypt_text(encrypt_data: bytes, key: bytes) -> str:
    """
    Дешифрование данных алгоритмом AES-CBC

    принимает:
        encrypt_data: Зашифрованные данные (IV + ciphertext)
        key: Симметричный ключ AES (16, 24 или 32 байта)

    возвращает:
        str: Расшифрованный текст
    """
    iv = encrypt_data[:16]
    ciphertext = encrypt_data[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data.decode('utf-8')