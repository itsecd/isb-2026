"""Генерация, сериализация RSA-ключей и шифрование ключа через RSA-OAEP."""

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding, rsa


def generate_private_key(key_size: int = 2048) -> rsa.RSAPrivateKey:
    """Генерирует закрытый RSA-ключ.

    Аргументы:
        key_size: Размер модуля RSA в битах.

    Возвращает:
        Сгенерированный закрытый RSA-ключ.
    """
    return rsa.generate_private_key(public_exponent=65537, key_size=key_size)


def serialize_public_key(public_key: rsa.RSAPublicKey) -> bytes:
    """Сериализует открытый RSA-ключ в PEM-формат."""
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )


def serialize_private_key(private_key: rsa.RSAPrivateKey) -> bytes:
    """Сериализует незашифрованный закрытый RSA-ключ в PEM-формат."""
    return private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )


def load_public_key(data: bytes) -> rsa.RSAPublicKey:
    """Загружает открытый RSA-ключ из PEM-байтов."""
    return serialization.load_pem_public_key(data)


def load_private_key(data: bytes) -> rsa.RSAPrivateKey:
    """Загружает закрытый RSA-ключ из PEM-байтов."""
    return serialization.load_pem_private_key(data, password=None)


def encrypt_key(symmetric_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """Шифрует симметричный ключ при помощи RSA-OAEP и SHA-256."""
    return public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt_key(encrypted_key: bytes, private_key: rsa.RSAPrivateKey) -> bytes:
    """Расшифровывает симметричный ключ при помощи RSA-OAEP и SHA-256."""
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
