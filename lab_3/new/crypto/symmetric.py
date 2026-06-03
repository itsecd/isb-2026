import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

BLOCK_SIZE = 64


def generate_key():
    try:
        return os.urandom(16)
    except Exception as e:
        raise RuntimeError(f"[SYM ERROR] Ошибка генерации ключа: {e}")


def encrypt(key: bytes, data: bytes):
    try:
        padder = padding.PKCS7(BLOCK_SIZE).padder()
        padded = padder.update(data) + padder.finalize()

        iv = os.urandom(8)

        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        enc = cipher.encryptor()

        return iv, enc.update(padded) + enc.finalize()

    except Exception as e:
        raise RuntimeError(f"[SYM ERROR] Ошибка шифрования: {e}")


def decrypt(key: bytes, iv: bytes, data: bytes):
    try:
        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        dec = cipher.decryptor()

        padded = dec.update(data) + dec.finalize()

        unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()
        return unpadder.update(padded) + unpadder.finalize()

    except ValueError:
        raise ValueError("[SYM ERROR] Ошибка padding (повреждённые данные)")
    except Exception as e:
        raise RuntimeError(f"[SYM ERROR] Ошибка расшифрования: {e}")
