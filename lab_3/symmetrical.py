import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

def generate_key() -> bytes:
    """Генерирует случайный 128-битный ключ IDEA."""
    return os.urandom(16)

def encrypt_data(key: bytes, plaintext: bytes) -> bytes:
    """Шифрует данные IDEA в режиме CBC (IV + шифротекст)."""
    iv = os.urandom(8)
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def decrypt_data(key: bytes, encrypted_data: bytes) -> bytes:
    """Расшифровывает данные, зашифрованные encrypt_data."""
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded_plaintext) + unpadder.finalize()