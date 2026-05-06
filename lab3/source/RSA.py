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
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def save_private_key(private_key: RSAPrivateKey, path: str) -> None:
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                serialization.Encoding.PEM,
                serialization.PrivateFormat.TraditionalOpenSSL,
                serialization.NoEncryption(),
            )
        )


def save_public_key(public_key: RSAPublicKey, path: str) -> None:
    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                serialization.Encoding.PEM,
                serialization.PublicFormat.SubjectPublicKeyInfo,
            )
        )


def load_private_key(path: str) -> RSAPrivateKey:
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=None)


def encrypt(data: bytes, public_key: RSAPublicKey) -> bytes:
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt(data: bytes, private_key: RSAPrivateKey) -> bytes:
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )