"""
Асимметричное шифрование: RSA-2048 с OAEP-паддингом (SHA-256).
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes


def generate_rsa_keys():
    """
    Генерирует пару RSA-2048 ключей.
    Возвращает (private_key, public_key).
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def _oaep_padding():
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def encrypt(data: bytes, public_key) -> bytes:
    """Шифрует данные открытым RSA-ключом (OAEP/SHA-256)."""
    return public_key.encrypt(data, _oaep_padding())


def decrypt(data: bytes, private_key) -> bytes:
    """Расшифровывает данные закрытым RSA-ключом (OAEP/SHA-256)."""
    return private_key.decrypt(data, _oaep_padding())
