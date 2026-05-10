import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def generate_key(key_size: int = 192) -> bytes:
    if key_size not in (64, 128, 192):
        raise ValueError(f"Недопустимый размер ключа: {key_size}")
    return os.urandom(key_size // 8)


def pad_data(data: bytes) -> bytes:
    padder = padding.ANSIX923(64).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(padded_data: bytes) -> bytes:
    unpadder = padding.ANSIX923(64).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def encrypt(data: bytes, key: bytes) -> tuple:
    iv = os.urandom(8)
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()
    return iv, encrypted


def decrypt(encrypted_data: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = Cipher(algorithms.TripleDES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    return decryptor.update(encrypted_data) + decryptor.finalize()