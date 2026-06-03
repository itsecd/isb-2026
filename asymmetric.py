"""Модуль для работы с асимметричным алгоритмом RSA."""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_rsa_key_pair() -> tuple:
    """Генерирует пару ключей RSA-2048.

    Returns:
        tuple: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def serialize_public_key(public_key) -> bytes:
    """Преобразует открытый ключ в формат PEM."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )


def serialize_private_key(private_key) -> bytes:
    """Преобразует закрытый ключ в формат PEM (PKCS8)."""
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )


def encrypt_session_key(public_key, session_key: bytes) -> bytes:
    """Шифрует симметричный сессионный ключ с помощью RSA-OAEP."""
    return public_key.encrypt(
        session_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_session_key(private_key_bytes: bytes, enc_session_key: bytes) -> bytes:
    """Десериализует закрытый ключ и расшифровывает сессионный ключ Camellia."""
    private_key = load_pem_private_key(private_key_bytes, password=None)
    return private_key.decrypt(
        enc_session_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )