import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives import serialization


def _read_file(filepath: str) -> bytes:
    try:
        with open(filepath, 'rb') as f:
            return f.read()
    except FileNotFoundError as e:
        raise FileNotFoundError(f"File not found: {filepath}") from e


def generate_symmetric_key(key_size: int) -> bytes:
    if key_size % 8 != 0:
        raise ValueError("key_len must be multiple of 8")
    key = os.urandom(key_size//8)
    return key


def generate_rsa_keys() -> RSAPrivateKey:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def save_symmetric_key(key: bytes, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as key_file:
        key_file.write(key)


def load_symmetric_key(filepath: str) -> bytes:
    return _read_file(filepath)


def save_public_key(pub_key: RSAPublicKey, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as public_out:
        public_out.write(pub_key.public_bytes(encoding=serialization.Encoding.PEM,
                format = serialization.PublicFormat.SubjectPublicKeyInfo))


def load_public_key(filepath: str) -> RSAPublicKey:
    return serialization.load_pem_public_key(_read_file(filepath))


def save_private_key(priv_key: RSAPrivateKey, filepath: str) -> None:
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as private_out:
        private_out.write(priv_key.private_bytes(encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()))


def load_private_key(filepath: str) -> RSAPrivateKey:
    return serialization.load_pem_private_key(_read_file(filepath), password=None)