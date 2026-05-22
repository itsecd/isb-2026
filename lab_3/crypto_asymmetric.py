
"""
Модуль асимметричного шифрования (RSA)
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend


def generate_rsa_keypair(key_size: int = 2048):
    """
    Генерирует пару RSA ключей.
    
    Args:
        key_size: Размер ключа в битах.
    
    Returns:
        Кортеж (private_key, public_key).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_rsa_private_key(private_key, filepath: str) -> None:
    """Сохраняет приватный RSA ключ в PEM файл."""
    with open(filepath, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))


def save_rsa_public_key(public_key, filepath: str) -> None:
    """Сохраняет публичный RSA ключ в PEM файл."""
    with open(filepath, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def load_rsa_private_key(filepath: str):
    """Загружает приватный RSA ключ из PEM файла."""
    with open(filepath, 'rb') as f:
        key_data = f.read()
    return serialization.load_pem_private_key(key_data, password=None, backend=default_backend())


def load_rsa_public_key(filepath: str):
    """Загружает публичный RSA ключ из PEM файла."""
    with open(filepath, 'rb') as f:
        key_data = f.read()
    return serialization.load_pem_public_key(key_data, backend=default_backend())


def encrypt_asymmetric(public_key, data: bytes) -> bytes:
    """
    Шифрует данные публичным RSA ключом (OAEP).
    
    Args:
        public_key: Публичный RSA ключ.
        data: Данные для шифрования.
    
    Returns:
        Зашифрованные данные.
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_asymmetric(private_key, encrypted_data: bytes) -> bytes:
    """
    Расшифровывает данные приватным RSA ключом.
    
    Args:
        private_key: Приватный RSA ключ.
        encrypted_data: Зашифрованные данные.
    
    Returns:
        Расшифрованные данные.
    """
    return private_key.decrypt(
        encrypted_data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )