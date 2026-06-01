"""
Сериализация и десериализация RSA-ключей (PEM-формат).
"""

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from crypto.file_utils import save_bytes


def save_public_key(public_key, path: str) -> None:
    """
    Сохраняет открытый RSA-ключ в PEM-файл.
    
    Args:
        public_key: Открытый RSA-ключ для сохранения.
        path: Путь к файлу для сохранения.
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    save_bytes(pem, path)


def save_private_key(private_key, path: str) -> None:
    """
    Сохраняет закрытый RSA-ключ в PEM-файл (без парольной защиты).
    
    Args:
        private_key: Закрытый RSA-ключ для сохранения.
        path: Путь к файлу для сохранения.
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    save_bytes(pem, path)


def load_public_key(path: str):
    """
    Загружает открытый RSA-ключ из PEM-файла.
    
    Args:
        path: Путь к PEM-файлу с открытым ключом.
    
    Returns:
        Открытый RSA-ключ.
    """
    try:
        with open(path, "rb") as f:
            return load_pem_public_key(f.read())
    except FileNotFoundError:
        raise RuntimeError(f"Открытый ключ не найден: {path}")
    except ValueError as e:
        raise RuntimeError(f"Неверный PEM-формат открытого ключа: {path}: {e}")
    except OSError as e:
        raise RuntimeError(f"Не удалось прочитать открытый ключ {path}: {e}")


def load_private_key(path: str):
    """
    Загружает закрытый RSA-ключ из PEM-файла.
    
    Args:
        path: Путь к PEM-файлу с закрытым ключом.
    
    Returns:
        Закрытый RSA-ключ.
    """
    try:
        with open(path, "rb") as f:
            return load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        raise RuntimeError(f"Закрытый ключ не найден: {path}")
    except ValueError as e:
        raise RuntimeError(f"Неверный PEM-формат закрытого ключа: {path}: {e}")
    except OSError as e:
        raise RuntimeError(f"Не удалось прочитать закрытый ключ {path}: {e}")
