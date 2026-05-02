import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def encrypt_AES(text: str, key: bytes) -> bytes:
    """
    Шифрует текст алгоритмом AES в режиме CBC с паддингом ANSIX923._
    """
    if len(key) not in (16, 24, 32):
        raise ValueError("Длина ключа AES должна быть 16, 24 или 32 байта.")
    text_bytes = text.encode("utf-8")
    padder = padding.ANSIX923(128).padder()
    padded_text = padder.update(text_bytes) + padder.finalize()
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_text) + encryptor.finalize()
    return iv + ciphertext


def decrypt_aes_cbc(encrypted_data: bytes, key: bytes) -> str:
    """
    Расшифровывает текст, зашифрованный AES с паддингом ANSIX923.

    """
    if len(key) not in (16, 24, 32):
        raise ValueError("Длина ключа AES должна быть 16, 24 или 32 байта.")
    iv = encrypted_data[:16]
    c_text = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(c_text) + decryptor.finalize()
    unpadder = padding.ANSIX923(128).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    return unpadded_dc_text.decode("utf-8")
