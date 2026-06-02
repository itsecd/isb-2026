"""
Модуль для работы с асимметричным шифрованием алгоритмом RSA.

RSA (Rivest-Shamir-Adleman) - один из первых алгоритмов асимметричного
шифрования, опубликованный в 1977 году. Основан на вычислительной
сложности задачи факторизации больших целых чисел.

Характеристики:
- Размер ключа: 2048 бит (рекомендуемый минимум)
- Публичная экспонента: 65537 (стандартное значение)
- Схема шифрования: OAEP с SHA-256
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from typing import Tuple

from .io_utils import read_binary_file, write_binary_file


def generate_rsa_keypair(key_size: int = 2048, public_exponent: int = 65537) -> Tuple:
    """
    Генерирует пару ключей RSA (приватный и публичный).
    
    Args:
        key_size: Размер ключа в битах (по умолчанию 2048).
        public_exponent: Публичная экспонента (по умолчанию 65537).
        
    Returns:
        Tuple: Кортеж, содержащий (private_key, public_key).
        
    Note:
        Использует стандартную публичную экспоненту 65537 и 
        размер ключа 2048 бит.
    """
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_private_key(private_key, password: bytes = None) -> bytes:
    """
    Сериализует приватный RSA ключ в формат PEM.
    
    Args:
        private_key: Приватный ключ для сериализации.
        password: Пароль для шифрования ключа (опционально).
        
    Returns:
        bytes: Сериализованный ключ в формате PEM.
    """
    encryption_algorithm = (
        serialization.BestAvailableEncryption(password)
        if password
        else serialization.NoEncryption()
    )
    
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=encryption_algorithm
    )


def serialize_public_key(public_key) -> bytes:
    """
    Сериализует публичный RSA ключ в формат PEM.
    
    Args:
        public_key: Публичный ключ для сериализации.
        
    Returns:
        bytes: Сериализованный ключ в формате PEM.
    """
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def load_private_key(path: str, password: bytes = None):
    """
    Загружает приватный RSA ключ из PEM файла.
    
    Args:
        path: Путь к файлу с приватным ключом.
        password: Пароль для расшифровки ключа (если зашифрован).
        
    Returns:
        Приватный RSA ключ.
    """
    pem_data = read_binary_file(path)
    return serialization.load_pem_private_key(
        pem_data,
        password=password,
        backend=default_backend()
    )


def load_public_key(path: str):
    """
    Загружает публичный RSA ключ из PEM файла.
    
    Args:
        path: Путь к файлу с публичным ключом.
        
    Returns:
        Публичный RSA ключ.
    """
    pem_data = read_binary_file(path)
    return serialization.load_pem_public_key(
        pem_data,
        backend=default_backend()
    )


def rsa_encrypt(public_key, plaintext: bytes) -> bytes:
    """
    Шифрует данные с использованием RSA-OAEP.
    
    Args:
        public_key: Публичный ключ для шифрования.
        plaintext: Данные для шифрования.
        
    Returns:
        bytes: Зашифрованные данные.
        
    Note:
        Использует схему OAEP с MGF1 и хеш-функцией SHA-256.
        Максимальный размер данных зависит от размера ключа.
    """
    return public_key.encrypt(
        plaintext,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def rsa_decrypt(private_key, ciphertext: bytes) -> bytes:
    """
    Расшифровывает данные с использованием RSA-OAEP.
    
    Args:
        private_key: Приватный ключ для расшифрования.
        ciphertext: Зашифрованные данные.
        
    Returns:
        bytes: Расшифрованные данные.
        
    Note:
        Использует схему OAEP с MGF1 и хеш-функцией SHA-256.
    """
    return private_key.decrypt(
        ciphertext,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def encrypt_symmetric_key(public_key, symmetric_key: bytes) -> bytes:
    """
    Шифрует симметричный ключ с использованием публичного RSA ключа.
    
    Args:
        public_key: Публичный RSA ключ.
        symmetric_key: Симметричный ключ для шифрования.
        
    Returns:
        bytes: Зашифрованный симметричный ключ.
    """
    return rsa_encrypt(public_key, symmetric_key)


def decrypt_symmetric_key(private_key, encrypted_key: bytes) -> bytes:
    """
    Расшифровывает симметричный ключ с использованием приватного RSA ключа.
    
    Args:
        private_key: Приватный RSA ключ.
        encrypted_key: Зашифрованный симметричный ключ.
        
    Returns:
        bytes: Расшифрованный симметричный ключ.
    """
    return rsa_decrypt(private_key, encrypted_key)