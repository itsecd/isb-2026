from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from config import RSA_KEY_SIZE, PUBLIC_EXPONENT
from file_utils import save_bytes, load_bytes


def generate_asymmetric_keys():
    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_private_key(private_key, path):
    try:
        pem_data = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        )
        save_bytes(pem_data, path)
    except Exception as e:
        raise RuntimeError(f"Failed to serialize private key: {e}")


def serialize_public_key(public_key, path):
    try:
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        save_bytes(pem_data, path)
    except Exception as e:
        raise RuntimeError(f"Failed to serialize public key: {e}")


def load_private_key(path):
    try:
        pem_bytes = load_bytes(path)
        return load_pem_private_key(pem_bytes, password=None)
    except Exception as e:
        raise RuntimeError(f"Failed to load private key: {e}")


def load_public_key(path):
    try:
        pem_bytes = load_bytes(path)
        return load_pem_public_key(pem_bytes)
    except Exception as e:
        raise RuntimeError(f"Failed to load public key: {e}")


def rsa_encrypt(public_key, data):
    try:
        return public_key.encrypt(
            data,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise RuntimeError(f"RSA encryption failed: {e}")


def rsa_decrypt(private_key, ciphertext):
    try:
        return private_key.decrypt(
            ciphertext,
            asym_padding.OAEP(
                mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
    except Exception as e:
        raise RuntimeError(f"RSA decryption failed: {e}")
