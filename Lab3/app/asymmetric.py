from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


# генерация ключей
def generate_rsa_keys(key_size: int = 2048):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size
    )
    return private_key, private_key.public_key()


# работа с файлами (DRY)
def write_bytes(path: str, data: bytes):
    with open(path, "wb") as f:
        f.write(data)


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


# сериализация
def save_private_key(private_key, path: str):
    data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    write_bytes(path, data)


def save_public_key(public_key, path: str):
    data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    write_bytes(path, data)


# десериализация
def load_private_key(path: str):
    return serialization.load_pem_private_key(
        read_bytes(path),
        password=None
    )


def load_public_key(path: str):
    return serialization.load_pem_public_key(
        read_bytes(path)
    )


# RSA операции
def encrypt_symmetric_key(public_key, key: bytes) -> bytes:
    return public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_symmetric_key(private_key, encrypted_key: bytes) -> bytes:
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )