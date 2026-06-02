import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import IDEA
from cryptography.hazmat.primitives import padding


def generate_idea_key() -> bytes:
    """Генерирует IDEA ключ длиной 128 бит."""
    return os.urandom(16)


def encrypt_data_idea(text: bytes, idea_key: bytes) -> tuple[bytes, bytes]:
    """Зашифровывает данные с помощью IDEA ключа."""
    try:
        padder = padding.ANSIX923(64).padder()
        padded_text = padder.update(text) + padder.finalize()
        
        iv = os.urandom(8)
        cipher = Cipher(IDEA(idea_key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        cyph_text = encryptor.update(padded_text) + encryptor.finalize()
        
        return iv, cyph_text
    except Exception as e:
        raise RuntimeError(f"Ошибка при симметричном шифровании: {e}")


def decrypt_data_idea(actual_cyph_text: bytes, iv: bytes, idea_key: bytes) -> bytes:
    """Расшифровывает текст с помощью IDEA ключа."""
    try:
        cipher = Cipher(IDEA(idea_key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        dc_text = decryptor.update(actual_cyph_text) + decryptor.finalize()
        
        unpadder = padding.ANSIX923(64).unpadder()
        unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
        
        return unpadded_dc_text
    except ValueError:
        raise ValueError("Ошибка расшифровки данных.")