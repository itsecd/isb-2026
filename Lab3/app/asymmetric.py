
"""
Модуль асимметричной криптографии RSA.
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from app.file_utils import write_bytes, read_bytes

def generate_rsa_keys(key_size: int = 2048):
    """
    Генерирует пару RSA-ключей.

    :param key_size: размер RSA-ключа
    :return: приватный и публичный ключ
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size
        )

        return private_key, private_key.public_key()

    except Exception as error:
        print(f"Ошибка генерации RSA-ключей: {error}")
        raise


def save_private_key(private_key, path: str) -> None:
    """
    Сохраняет приватный ключ.

    :param private_key: приватный RSA-ключ
    :param path: путь сохранения
    """
    try:
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        write_bytes(path, pem)

    except Exception as error:
        print(f"Ошибка сохранения приватного ключа: {error}")
        raise


def save_public_key(public_key, path: str) -> None:
    """
    Сохраняет публичный ключ.

    :param public_key: публичный RSA-ключ
    :param path: путь сохранения
    """
    try:
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        write_bytes(path, pem)

    except Exception as error:
        print(f"Ошибка сохранения публичного ключа: {error}")
        raise


def load_private_key(path: str):
    """
    Загружает приватный RSA-ключ.

    :param path: путь к ключу
    :return: приватный ключ
    """
    try:
        data = read_bytes(path)

        return serialization.load_pem_private_key(
            data,
            password=None
        )

    except Exception as error:
        print(f"Ошибка загрузки приватного ключа: {error}")
        raise


def load_public_key(path: str):
    """
    Загружает публичный RSA-ключ.

    :param path: путь к ключу
    :return: публичный ключ
    """
    try:
        data = read_bytes(path)

        return serialization.load_pem_public_key(data)

    except Exception as error:
        print(f"Ошибка загрузки публичного ключа: {error}")
        raise


def encrypt_symmetric_key(public_key, symmetric_key: bytes) -> bytes:
    """
    Шифрует симметричный ключ RSA.

    :param public_key: публичный RSA-ключ
    :param symmetric_key: симметричный ключ
    :return: зашифрованный ключ
    """
    try:
        return public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    except Exception as error:
        print(f"Ошибка шифрования симметричного ключа: {error}")
        raise


def decrypt_symmetric_key(private_key, encrypted_key: bytes) -> bytes:
    """
    Дешифрует симметричный ключ RSA.

    :param private_key: приватный RSA-ключ
    :param encrypted_key: зашифрованный симметричный ключ
    :return: расшифрованный ключ
    """
    try:
        return private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

    except Exception as error:
        print(f"Ошибка дешифрования симметричного ключа: {error}")
        raise
