import key_generation

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)

def serialize_public_key(public_key, public_pem_path: str):
    """
    Save public key as a .pem file
    Args:
        public_key(str): public key
        public_pem_path(str): save path for the key 
    Raises:
        OSError: Error writing data
    """
    try:
        with open(public_pem_path, "wb") as public_out:
            public_out.write(
                public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo,
                )
            )
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")


def serialize_private_key(private_key, private_pem_path: str):
    """
    Save private key as a .pem file
    Args:
        public_key(str): private key
        public_pem_path(str): save path for the key 
    Raises:
        OSError: Error writing data
    """
    try:
        with open(private_pem_path, "wb") as private_out:
            private_out.write(
                private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.TraditionalOpenSSL,
                    encryption_algorithm=serialization.NoEncryption(),
                )
            )
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")

def deserialize_public_key(public_pem_path: str):
    """
    Read public key from a .pem file
    Args:
        public_pem_path(str): read path for the key 
    Raises:
        FileNotFoundError: file not found
    """
    try:
        with open(public_pem_path, "rb") as pem_in:
            public_bytes = pem_in.read()
        return load_pem_public_key(public_bytes)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Ошибка сохранения файла: {e}")

def deserialize_private_key(private_key, private_pem_path: str):
    """
    Save private key as a .pem file
    Args:
        public_key(str): private key
        public_pem_path(str): save path for the key 
    Raises:
        OSError: Error writing data
    """
    try:
        with open(private_pem_path, "rb") as pem_in:
            private_bytes = pem_in.read()
        return load_pem_private_key(private_bytes)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")
