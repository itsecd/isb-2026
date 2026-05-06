import os
from file_utils import read_file
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


def generate_symmetric_key(key_size: int) -> bytes:
    if key_size % 8 != 0:
        raise ValueError("key_size must be multiple of 8")
    if not 32 <= key_size <= 448:
        raise ValueError("Key size must be between 32 and 448 bits")
    return os.urandom(key_size//8)


def generate_rsa_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def save_symmetric_key(key: bytes, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as key_file:
        key_file.write(key)


def save_public_key(pub_key: RSAPublicKey, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as public_out:
        public_out.write(pub_key.public_bytes(encoding=serialization.Encoding.PEM,
            format = serialization.PublicFormat.SubjectPublicKeyInfo))


def load_public_key(filepath: str) -> RSAPublicKey:
    return serialization.load_pem_public_key(read_file(filepath))


def save_private_key(priv_key: RSAPrivateKey, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as private_out:
        private_out.write(priv_key.private_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()))


def load_private_key(filepath: str) -> RSAPrivateKey:
    return serialization.load_pem_private_key(read_file(filepath), password=None)