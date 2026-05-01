import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms


def generate_chacha20_key():
    """
    Создание 256-битного симметричного ключа.
    """
    return os.urandom(32)


def generate_nonce():
    """
    Созданмие 128-битного одноразового номера nonce.
    """
    return os.urandom(16)
 

def encrypt_with_chacha20_cipher(data: bytes, key: bytes, nonce: bytes):
    """
    Шифрование данных с использованием потокового шифра ChaCha20.
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        encryptor = cipher.encryptor()
        return encryptor.update(data)
    except Exception as e:
        raise RuntimeError(f"ChaCha20 encryption error: {e}")


def decrypt_with_chacha20_cipher(data: bytes, key: bytes, nonce: bytes):
    """
    Расшифровка данных с использованием потокового шифра ChaCha20.
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        decryptor = cipher.decryptor()
        return decryptor.update(data)
    except Exception as e:
        raise RuntimeError(f"ChaCha20 decryption error: {e}")