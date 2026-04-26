
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    load_pem_public_key,
)
from file_utils import save_bytes, load_bytes


def generate_rsa_keys():
    """
    Генерирует пару RSA-ключей (2048 бит).

    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    print("[OK] Пара RSA-ключей (2048 бит) сгенерирована")
    return private_key, public_key


def serialize_public_key(public_key, path: str) -> None:
    """
    Сохраняет открытый RSA-ключ в PEM-формате.

    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    save_bytes(pem, path)
    print(f"[OK] Открытый RSA-ключ сохранён: {path}")


def serialize_private_key(private_key, path: str) -> None:
    """
    Сохраняет закрытый RSA-ключ в PEM-формате (без шифрования).

    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    save_bytes(pem, path)
    print(f"[OK] Закрытый RSA-ключ сохранён: {path}")


def load_public_key(path: str):
    """
    Загружает открытый RSA-ключ из PEM-файла.

    """
    pem = load_bytes(path)
    key = load_pem_public_key(pem)
    print(f"[OK] Открытый RSA-ключ загружен: {path}")
    return key


def load_private_key(path: str):
    """
    Загружает закрытый RSA-ключ из PEM-файла.

    """
    pem = load_bytes(path)
    key = load_pem_private_key(pem, password=None)
    print(f"[OK] Закрытый RSA-ключ загружен: {path}")
    return key


def rsa_encrypt(data: bytes, public_key) -> bytes:
    """
    Шифрует данные открытым RSA-ключом (OAEP).

    """
    ciphertext = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    print("[OK] Данные зашифрованы RSA (OAEP)")
    return ciphertext


def rsa_decrypt(data: bytes, private_key) -> bytes:
    """
    Дешифрует данные закрытым RSA-ключом.

    """
    plaintext = private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )
    print("[OK] Данные расшифрованы RSA (OAEP)")
    return plaintext