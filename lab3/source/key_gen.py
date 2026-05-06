import json
import os
import argparse
from typing import Any, Dict

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from utils import load_config, write_bytes
from RSA import generate_rsa_keys
from CAST5 import generate_symmetric_key

def save_private_key(private_key, path: str) -> None:
    """
    Сохраняет RSA приватный ключ в PEM формате.

    Parameters
    ----------
    private_key : rsa.RSAPrivateKey
        Приватный ключ.
    path : str
        Путь для сохранения.
    """
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def save_public_key(public_key, path: str) -> None:
    """
    Сохраняет RSA публичный ключ в PEM формате.

    Parameters
    ----------
    public_key : rsa.RSAPublicKey
        Публичный ключ.
    path : str
        Путь для сохранения.
    """
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def encrypt_symmetric_key(sym_key: bytes, public_key) -> bytes:
    """
    Шифрует симметричный ключ RSA-OAEP.

    Parameters
    ----------
    sym_key : bytes
        Симметричный ключ.
    public_key : rsa.RSAPublicKey
        Публичный RSA ключ.

    Returns
    -------
    bytes
        Зашифрованный симметричный ключ.
    """
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def generate_keys_pipeline(config: Dict[str, Any]) -> None:
    """
    Полный пайплайн генерации ключей гибридной криптосистемы.

    Parameters
    ----------
    config : Dict[str, Any]
        Конфигурация:
        - key_size: размер симметрического ключа (в байтах)
        - secret_key: путь к приватному RSA ключу
        - public_key: путь к публичному RSA ключу
        - symmetric_key: путь к зашифрованному симметрическому ключу

    Returns
    -------
    None
    """
    print("[*] Генерация ключей")

    sym_key = generate_symmetric_key(config["key_size"])

    private_key, public_key = generate_rsa_keys()

    save_private_key(private_key, config["secret_key"])
    save_public_key(public_key, config["public_key"])

    encrypted_sym_key = encrypt_symmetric_key(sym_key, public_key)

    write_bytes(config["symmetric_key"], encrypted_sym_key)

    print("[+] Готово")