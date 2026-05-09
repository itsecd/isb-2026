from typing import Any, Dict

from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization, hashes

from utils import write_bytes
from RSA import generate_rsa_keys
from AES import generate_symmetric_key


def save_private_key(private_key: rsa.RSAPrivateKey, path: str) -> None:
    """
    Сохраняет RSA приватный ключ в PEM формате.
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    with open(path, "wb") as f:
        f.write(pem)


def save_public_key(public_key: rsa.RSAPublicKey, path: str) -> None:
    """
    Сохраняет RSA публичный ключ в PEM формате.
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(path, "wb") as f:
        f.write(pem)


def encrypt_symmetric_key(sym_key: bytes, public_key: rsa.RSAPublicKey) -> bytes:
    """
    Шифрует симметричный AES ключ с помощью RSA-OAEP.
    """
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def generate_keys_pipeline(config: Dict[str, Any]) -> None:
    """
    Генерация ключей для гибридной криптосистемы (RSA + AES).

    config:
        key_size       — размер AES ключа (16/24/32 байта)
        secret_key     — путь к RSA private key
        public_key     — путь к RSA public key
        symmetric_key  — путь для зашифрованного AES ключа
    """
    print("[*] Key generation started")

    sym_key = generate_symmetric_key(config["key_size"])
    private_key, public_key = generate_rsa_keys()

    save_private_key(private_key, config["secret_key"])
    save_public_key(public_key, config["public_key"])

    encrypted_sym_key = encrypt_symmetric_key(sym_key, public_key)
    write_bytes(config["symmetric_key"], encrypted_sym_key)

    print("[+] Key generation completed")