from typing import Tuple

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from utils import load_config, read_bytes, write_bytes


def generate_keys() -> Tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Генерирует RSA ключевую пару.

    Parameters
    ----------
    None

    Returns
    -------
    Tuple[RSAPrivateKey, RSAPublicKey]
        Приватный и публичный RSA ключи.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def save_private_key(private_key: RSAPrivateKey, path: str) -> None:
    """
    Сохраняет RSA приватный ключ в PEM формате.

    Parameters
    ----------
    private_key : RSAPrivateKey
        Приватный RSA ключ.
    path : str
        Путь для сохранения.
    """
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )


def save_public_key(public_key: RSAPublicKey, path: str) -> None:
    """
    Сохраняет RSA публичный ключ в PEM формате.

    Parameters
    ----------
    public_key : RSAPublicKey
        Публичный RSA ключ.
    path : str
        Путь для сохранения.
    """
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def load_private_key(path: str) -> RSAPrivateKey:
    """
    Загружает RSA приватный ключ из PEM файла.

    Parameters
    ----------
    path : str
        Путь к PEM-файлу.

    Returns
    -------
    RSAPrivateKey
        Загруженный приватный ключ.
    """
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


def encrypt(data: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Шифрует данные RSA-OAEP.

    Parameters
    ----------
    data : bytes
        Данные для шифрования.
    public_key : RSAPublicKey
        Публичный RSA ключ.

    Returns
    -------
    bytes
        Зашифрованные данные.
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt(data: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Расшифровывает данные RSA-OAEP.

    Parameters
    ----------
    data : bytes
        Зашифрованные данные.
    private_key : RSAPrivateKey
        Приватный RSA ключ.

    Returns
    -------
    bytes
        Исходные данные.
    """
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )