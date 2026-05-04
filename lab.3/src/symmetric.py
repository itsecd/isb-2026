import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from .utils import pad_data, unpad_data
from .config import BLOCK_SIZE


def generate_camellia_key(key_size: int = 32) -> bytes:
    """Генерация случайного ключа для Camellia"""
    return os.urandom(key_size)


def encrypt_with_camellia(data: bytes, key: bytes) -> bytes:
    """
    Шифрование данных алгоритмом Camellia
    Возвращает: IV + зашифрованные_данные
    """
    iv = os.urandom(BLOCK_SIZE)
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    padded_data = pad_data(data, BLOCK_SIZE)
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
    
    return iv + encrypted_data


def decrypt_with_camellia(encrypted_data_with_iv: bytes, key: bytes) -> bytes:
    """
    Расшифровка данных алгоритмом Camellia
    Первые 16 байт - инициализирующий вектор
    """
    iv = encrypted_data_with_iv[:BLOCK_SIZE]
    encrypted_data = encrypted_data_with_iv[BLOCK_SIZE:]
    
    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()
    return unpad_data(decrypted_padded, BLOCK_SIZE)