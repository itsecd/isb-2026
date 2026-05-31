import os
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


def validate_blowfish_key_length(key_length: int) -> None:
    """
    Проверяет корректность длины ключа Blowfish.
    
    Args:
        key_length: Длина ключа в битах
    
    Raises:
        ValueError: Если длина ключа не соответствует требованиям
    """
    if not (32 <= key_length <= 448 and key_length % 8 == 0):
        raise ValueError(f"Длина ключа Blowfish должна быть от 32 до 448 бит и кратна 8, получено {key_length}")


def generate_blowfish_key(key_length: int) -> bytes:
    """
    Генерирует симметричный ключ для алгоритма Blowfish.
    
    Args:
        key_length: Длина ключа в битах (должна быть от 32 до 448 и кратна 8)
    
    Returns:
        bytes: Сгенерированный симметричный ключ
    """
    validate_blowfish_key_length(key_length)
    return os.urandom(key_length // 8)


def encrypt_blowfish(key: bytes, data: bytes) -> bytes:
    """
    Шифрует данные с использованием алгоритма Blowfish в режиме CBC.
    
    Args:
        key: Симметричный ключ Blowfish
        data: Данные для шифрования
    
    Returns:
        bytes: Зашифрованные данные с добавленным вектором инициализации в начале
    """
    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    iv = os.urandom(8)
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cipher_text = encryptor.update(padded_data) + encryptor.finalize()
    return iv + cipher_text


def decrypt_blowfish(key: bytes, encrypted_data: bytes) -> bytes:
    """
    Дешифрует данные с использованием алгоритма Blowfish.
    
    Args:
        key: Симметричный ключ Blowfish
        encrypted_data: Зашифрованные данные (IV + шифротекст)
    
    Returns:
        bytes: Расшифрованные исходные данные
    """
    iv = encrypted_data[:8]
    cipher_text = encrypted_data[8:]
    
    cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(cipher_text) + decryptor.finalize()
    
    unpadder = padding.PKCS7(64).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()
