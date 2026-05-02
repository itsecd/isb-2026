from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


def encrypt_symmetric_key(public_key: RSAPublicKey, symmetric_key: bytes) -> bytes:
    """
    Шифрует симметричный ключ с использованием открытого RSA-ключа.
    """
    encrypted_key: bytes = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return encrypted_key


def decrypt_symmetric_key(private_key: RSAPrivateKey, encrypted_key: bytes) -> bytes:
    """
    Расшифровывает симметричный ключ с использованием закрытого RSA-ключа.
    """
    symmetric_key: bytes = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    return symmetric_key
