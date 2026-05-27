import os
import sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key


def generate_symmetric_key(bits: int = 256) -> bytes:
    """
    Генерирует случайный симметричный ключ заданной длины.

    Args:
        bits (int): длина ключа в битах (128, 192 или 256). По умолчанию 256.

    Returns:
        bytes: сгенерированный ключ в виде байтовой строки.

    Raises:
        ValueError: если длина ключа не равна 128, 192 или 256 бит.
    """
    if bits not in (128, 192, 256):
        raise ValueError(f"Недопустимая длина ключа AES: {bits} бит")
    
    key = os.urandom(bits // 8)
    print(f"Сгенерирован симметричный ключ AES ({bits} бит)")
    return key


def generate_asymmetric_keys(key_size: int = 2048, public_exponent: int = 65537) -> tuple:
    """
    Генерирует пару асимметричных ключей RSA.

    Args:
        key_size (int): размер ключа в битах. По умолчанию 2048.
        public_exponent (int): публичная экспонента. По умолчанию 65537.

    Returns:
        tuple: (private_key, public_key) - закрытый и открытый ключи RSA.

    Raises:
        Exception: если произошла ошибка при генерации ключей.
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size
        )
        public_key = private_key.public_key()
        print(f"Сгенерирована пара ключей RSA ({key_size} бит)")
        return private_key, public_key
    except Exception as e:
        print(f"Ошибка при генерации ключей RSA: {e}")
        raise


def save_private_key(private_key, path: str) -> None:
    """
    Сохраняет закрытый ключ RSA в файл в формате PEM без шифрования.

    Args:
        private_key: объект закрытого ключа RSA.
        path (str): путь для сохранения ключа.

    Raises:
        IOError: если произошла ошибка при записи файла.
    """
    try:
        with open(path, 'wb') as f:
            f.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            ))
        print(f"Закрытый ключ сохранён в {path}")
    except IOError as e:
        print(f"Ошибка при сохранении закрытого ключа в {path}: {e}")
        raise


def save_public_key(public_key, path: str) -> None:
    """
    Сохраняет открытый ключ RSA в файл в формате PEM.

    Args:
        public_key: объект открытого ключа RSA.
        path (str): путь для сохранения ключа.

    Raises:
        IOError: если произошла ошибка при записи файла.
    """
    try:
        with open(path, 'wb') as f:
            f.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
        print(f"Открытый ключ сохранён в {path}")
    except IOError as e:
        print(f"Ошибка при сохранении открытого ключа в {path}: {e}")
        raise


def load_private_key(path: str):
    """
    Загружает закрытый ключ RSA из PEM-файла.

    Args:
        path (str): путь к файлу с закрытым ключом.

    Returns:
        объект закрытого ключа RSA.

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если файл содержит некорректный ключ.
        Exception: при других ошибках загрузки.
    """
    try:
        with open(path, 'rb') as f:
            key_data = f.read()
        private_key = load_pem_private_key(key_data, password=None)
        print(f"Закрытый ключ загружен из {path}")
        return private_key
    except FileNotFoundError:
        print(f"Ошибка: файл {path} не найден.")
        raise
    except ValueError as e:
        print(f"Ошибка: некорректный формат закрытого ключа в {path}: {e}")
        raise
    except Exception as e:
        print(f"Ошибка при загрузке закрытого ключа из {path}: {e}")
        raise


def load_public_key(path: str):
    """
    Загружает открытый ключ RSA из PEM-файла.

    Args:
        path (str): путь к файлу с открытым ключом.

    Returns:
        объект открытого ключа RSA.

    Raises:
        FileNotFoundError: если файл не найден.
        ValueError: если файл содержит некорректный ключ.
        Exception: при других ошибках загрузки.
    """
    try:
        with open(path, 'rb') as f:
            key_data = f.read()
        public_key = load_pem_public_key(key_data)
        print(f"Открытый ключ загружен из {path}")
        return public_key
    except FileNotFoundError:
        print(f"Ошибка: файл {path} не найден.")
        raise
    except ValueError as e:
        print(f"Ошибка: некорректный формат открытого ключа в {path}: {e}")
        raise
    except Exception as e:
        print(f"Ошибка при загрузке открытого ключа из {path}: {e}")
        raise


def save_encrypted_symmetric_key(encrypted_key: bytes, path: str) -> None:
    """
    Сохраняет зашифрованный симметричный ключ в бинарный файл.

    Args:
        encrypted_key (bytes): зашифрованный симметричный ключ.
        path (str): путь для сохранения.

    Raises:
        IOError: если произошла ошибка при записи файла.
    """
    try:
        with open(path, 'wb') as f:
            f.write(encrypted_key)
        print(f"Зашифрованный симметричный ключ сохранён в {path}")
    except IOError as e:
        print(f"Ошибка при сохранении зашифрованного ключа в {path}: {e}")
        raise


def load_encrypted_symmetric_key(path: str) -> bytes:
    """
    Загружает зашифрованный симметричный ключ из бинарного файла.

    Args:
        path (str): путь к файлу.

    Returns:
        bytes: зашифрованный симметричный ключ.

    Raises:
        FileNotFoundError: если файл не найден.
        IOError: при ошибке чтения файла.
    """
    try:
        with open(path, 'rb') as f:
            encrypted_key = f.read()
        print(f"Зашифрованный симметричный ключ загружен из {path}")
        return encrypted_key
    except FileNotFoundError:
        print(f"Ошибка: файл {path} не найден.")
        raise
    except IOError as e:
        print(f"Ошибка при чтении файла {path}: {e}")
        raise