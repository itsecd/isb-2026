from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def generate_rsa_keypair() -> tuple:
    """Генерирует пару RSA-ключей (2048 бит)."""
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()

def save_private_key(private_key, path: str) -> None:
    """Сохраняет приватный RSA-ключ в PEM-файл."""
    with open(path, 'wb') as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

def save_public_key(public_key, path: str) -> None:
    """Сохраняет публичный RSA-ключ в PEM-файл."""
    with open(path, 'wb') as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def load_private_key(path: str):
    """Загружает приватный RSA-ключ из PEM-файла."""
    with open(path, 'rb') as f:
        return serialization.load_pem_private_key(f.read(), password=None)

def load_public_key(path: str):
    """Загружает публичный RSA-ключ из PEM-файла."""
    with open(path, 'rb') as f:
        return serialization.load_pem_public_key(f.read())

def encrypt_symmetric_key(public_key, sym_key: bytes) -> bytes:
    """Шифрует симметричный ключ открытым RSA-ключом (OAEP)."""
    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_symmetric_key(private_key, encrypted_key: bytes) -> bytes:
    """Расшифровывает симметричный ключ закрытым RSA-ключом."""
    return private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )