"""
Сериализация и десериализация RSA-ключей (PEM-формат).
"""

import os

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)


def _ensure_dir(path: str) -> None:
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)


def save_public_key(public_key, path: str) -> None:
    """Сохраняет открытый RSA-ключ в PEM-файл."""
    _ensure_dir(path)
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(path, "wb") as f:
        f.write(pem)


def save_private_key(private_key, path: str) -> None:
    """Сохраняет закрытый RSA-ключ в PEM-файл (без парольной защиты)."""
    _ensure_dir(path)
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(path, "wb") as f:
        f.write(pem)


def load_public_key(path: str):
    """Загружает открытый RSA-ключ из PEM-файла."""
    with open(path, "rb") as f:
        return load_pem_public_key(f.read())


def load_private_key(path: str):
    """Загружает закрытый RSA-ключ из PEM-файла."""
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)
