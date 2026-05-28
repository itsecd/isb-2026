"""Модуль асимметричной криптографии (Ориса-2048)"""

import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

from file_utils import read_binary_file, write_binary_file


def generate_rsa_keys(key_size: int = 2048, public_exponent: int = 65537):
    """Генерирует пару RSA ключей."""
    try:
        private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
            backend=default_backend()
        )
        return private_key, private_key.public_key()
    except Exception as e:
        raise Exception(f"Ошибка генерации RSA ключей: {str(e)}")


def save_rsa_private_key(private_key, private_path: str) -> bool:
    """Сохраняет приватный ключ RSA в PEM файл."""
    try:
        os.makedirs(os.path.dirname(private_path), exist_ok=True)
        
        private_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        write_binary_file(private_path, private_bytes)
        return True
    except Exception as e:
        raise Exception(f"Ошибка сохранения приватного ключа: {str(e)}")


def save_rsa_public_key(public_key, public_path: str) -> bool:
    """Сохраняет публичный ключ RSA в PEM файл."""
    try:
        os.makedirs(os.path.dirname(public_path), exist_ok=True)
        
        public_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        write_binary_file(public_path, public_bytes)
        return True
    except Exception as e:
        raise Exception(f"Ошибка сохранения публичного ключа: {str(e)}")


def load_rsa_private_key(private_path: str):
    """Загружает приватный ключ RSA из PEM файла."""
    try:
        data = read_binary_file(private_path)
        return serialization.load_pem_private_key(
            data,
            password=None,
            backend=default_backend()
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл приватного ключа не найден: {private_path}")
    except Exception as e:
        raise Exception(f"Ошибка загрузки приватного ключа: {str(e)}")


def load_rsa_public_key(public_path: str):
    """Загружает публичный ключ RSA из PEM файла."""
    try:
        data = read_binary_file(public_path)
        return serialization.load_pem_public_key(
            data,
            backend=default_backend()
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл публичного ключа не найден: {public_path}")
    except Exception as e:
        raise Exception(f"Ошибка загрузки публичного ключа: {str(e)}")


def encrypt_with_rsa(data: bytes, public_key) -> bytes:
    """Шифрует данные с помощью RSA-OAEP (SHA256)."""
    try:
        max_size = 190
        match len(data):
            case n if n > max_size:
                raise ValueError(f"Данные слишком большие для RSA-2048: {len(data)} > {max_size} байт")
            case _:
                pass
        
        return public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except ValueError as e:
        raise ValueError(f"Ошибка при шифровании RSA: {str(e)}")
    except Exception as e:
        raise Exception(f"Ошибка при шифровании RSA: {str(e)}")


def decrypt_with_rsa(ciphertext: bytes, private_key) -> bytes:
    """Расшифровывает данные с помощью RSA-OAEP."""
    try:
        return private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
    except Exception as e:
        raise Exception(f"Ошибка при расшифровании RSA: {str(e)}")