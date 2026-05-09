from typing import Optional

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.serialization import load_pem_private_key


RSA_KEY_SIZE = 2048
RSA_PUBLIC_EXPONENT = 65537


def generate_rsa_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    private_key = rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )
    return private_key, private_key.public_key()


def load_private_key(path: str, password: Optional[bytes] = None) -> RSAPrivateKey:
    with open(path, "rb") as f:
        return load_pem_private_key(f.read(), password=password)


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