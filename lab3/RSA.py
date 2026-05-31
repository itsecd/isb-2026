import symmetric

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding

def serialize_public_key(public_key, public_pem_path: str):
    """
    Save public key as a .pem file
    Args:
        public_key(str): public key object
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

def deserialize_private_key(private_pem_path: str):
    """
    Read private key from a .pem file
    Args:
        private_pem_path(str): read path for the key 
    Raises:
        FileNotFoundError: file not found
    """
    try:
        with open(private_pem_path, "rb") as pem_in:
            private_bytes = pem_in.read()
        return load_pem_private_key(private_bytes,password=None)
    except OSError as e:
        raise OSError(f"Ошибка сохранения файла: {e}")

def encrypt_symmetric_key(public_key_path: str, symmetric_key: bytes) -> bytes:
    """
    Encrypt the symmetric key with RSA public key
    Args:
        public_key_path(str): Path to public key
        symmetric_key(bytes): symmetric key
    Returns: 
        encrypted_key(bytes): encrypted symmetric key
    """
    public_key = deserialize_public_key (public_key_path)
    encrypted_key = public_key.encrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
    return encrypted_key

def decrypt_symmetric_key(private_key_path: str, encrypted_key_path: str) -> bytes:
    """
    Decrypt the symmetric key with RSA private key
    Args:
        private_key_path(str): Path to private key
        encrypted_key_path(str): Path to encrypted symmetric key
    Returns: 
        decrypted_key(bytes): decrypted symmetric key
    """
    private_key = deserialize_private_key(private_key_path)
    encrypted_key = symmetric.deserialize_encrypted_key (encrypted_key_path)
    decrypted_key = private_key.decrypt(
        encrypted_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None))
    return decrypted_key