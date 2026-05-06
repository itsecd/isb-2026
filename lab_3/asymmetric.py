import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives import hashes, serialization
from file_utils import read_file

def generate_rsa_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def decrypt_symmetric_key(encrypted_key_path: str, private_key) -> bytes:
    encrypted_key = read_file(encrypted_key_path)

    sym_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    if len(sym_key) != 32:
        raise ValueError("Decrypted symmetric key must be 32 bytes for ChaCha20")
    
    return sym_key

def encrypt_symmetric_key(sym_key: bytes, public_key: RSAPublicKey) -> bytes:
    if len(sym_key) == 0:
        raise ValueError("Symmetric key cannot be empty")

    return public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

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