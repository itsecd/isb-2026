"""Сериализация и десериализация ключей"""
from cryptography.hazmat.primitives import serialization

import constants as const
from file_utils import write_binary_file, read_binary_file

#Симметричный ключ

def save_symmetric_key_to_file(key: bytes, filepath: str):
    """Сохраняет симметричный ключ в бинарный файл"""
    write_binary_file(filepath, key)
    print(f"[OK] Симметричный ключ сохранён в {filepath}")

# Nonce

def save_nonce_to_file(nonce: bytes, filepath: str):
    """Сохраняет nonce в бинарный файл"""
    write_binary_file(filepath, nonce)
    print(f"[OK] Nonce сохранён в {filepath}")


def load_nonce_from_file(filepath: str) -> bytes:
    """Загружает nonce из бинарного файла"""
    nonce = read_binary_file(filepath)
    if len(nonce) != const.NONCE_SIZE:
        raise ValueError(f"Неверный размер nonce: ожидается {const.NONCE_SIZE} байт")
    print(f"[OK] Nonce загружен из {filepath}")
    return nonce


# RSA ключи 

def save_public_key_to_file(public_key, filepath: str):
    """Сохраняет публичный ключ RSA в PEM-файл"""
    pem = public_key.public_bytes(encoding=serialization.Encoding.PEM, format=serialization.PublicFormat.SubjectPublicKeyInfo)
    write_binary_file(filepath, pem)
    print(f"[OK] Публичный ключ RSA сохранён в {filepath}")


def save_private_key_to_file(private_key, filepath: str):
    """Сохраняет приватный ключ RSA в PEM-файл (без шифрования)"""
    pem = private_key.private_bytes(encoding=serialization.Encoding.PEM, format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption())
    write_binary_file(filepath, pem)
    print(f"[OK] Приватный ключ RSA сохранён в {filepath}")


def load_private_key_from_file(filepath: str):
    """Загружает приватный ключ RSA из PEM-файла"""
    pem_data = read_binary_file(filepath)
    private_key = serialization.load_pem_private_key(pem_data, password=None)#не зашифрован паролем
    print(f"[OK] Приватный ключ RSA загружен из {filepath}")
    return private_key

#  Зашифрованные данные 

def save_encrypted_data_to_file(data: bytes, filepath: str):
    """Сохраняет зашифрованные данные (RSA-шифротекст) в файл"""
    write_binary_file(filepath, data)
    print(f"[OK] Зашифрованные данные сохранены в {filepath}")


def load_encrypted_data_from_file(filepath: str) -> bytes:
    """Загружает зашифрованные данные из файла"""
    data = read_binary_file(filepath)
    print(f"[OK] Зашифрованные данные загружены из {filepath}")
    return data