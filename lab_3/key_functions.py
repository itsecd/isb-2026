import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from typing import Tuple


def generate_symmetric_key(aes_key_size: int = 256) -> bytes:
    """
    generates key for symmetric algorithm
    
    arguments: 
            aes_key_size: AES key size in bits (128, 192, 256)
    return: 
            key: random bytes of appropriate length
    """
    key_bytes = aes_key_size 
    key = os.urandom(key_bytes)
    return key


def generate_asymmetric_keys() -> Tuple:
    """
    generates keys for asymmetric algorithm
    
    arguments: -
    return: 
            tuple(private_key, public_key): tuple with objects of RSAPrivateKey and RSAPublicKey classes
    """
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key


def write_public_key(public_key, public_pem: str) -> None:
    """
    serializes public key to file
    
    arguments:
            public_key: object of RSAPublicKey class
            public_pem: path to file, where public_key is serialized, in str
    return: -
    """
    with open(public_pem, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def write_private_key(private_key, private_pem: str) -> None:
    """
    serializes private key to file
    
    arguments:
            private_key: object of RSAPrivateKey class
            private_pem: path to file, where private_key is serialized, in str
    return: -
    """
    with open(private_pem, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))


def encrypt_symmetric_key(key: bytes, public_key) -> bytes:
    """
    encrypts symmetric encryption key with public key
    
    arguments:
            key: random bytes of symmetric key
            public_key: object of RSAPublicKey class
    return:
            encrypt_key: bytes of encrypted symmetric key
    """
    encrypt_key = public_key.encrypt(
        key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypt_key


def write_symmetric_key(encrypt_key: bytes, file_name: str) -> None:
    """
    serializes encrypted symmetric algorithm key to file
    
    arguments: 
            encrypt_key: bytes of encrypted symmetric key
            file_name: path to file, where encrypt key is serialized, in str
    return: -
    """
    with open(file_name, 'wb') as key_file:
        key_file.write(encrypt_key)


def read_symmetric_key(symmetric_key_file: str) -> bytes:
    """
    reads encrypted symmetric key from file
    
    arguments: 
            symmetric_key_file: path to file, where encrypted symmetric key is stored, in str
    return:
            content: bytes of encrypted symmetric key
    """
    try:
        with open(symmetric_key_file, 'rb') as key_file:
            content = key_file.read()
        return content
    except FileNotFoundError:
        raise FileNotFoundError(f"{symmetric_key_file} file was not found")


def read_private_pem(private_pem: str):
    """
    reads private key from file
    
    arguments: 
            private_pem: path to file with private key, in str
    return:
            d_private_key: object of RSAPrivateKey class
    """
    try:
        with open(private_pem, 'rb') as pem_in:
            private_bytes = pem_in.read()
        d_private_key = load_pem_private_key(private_bytes, password=None)
        return d_private_key
    except FileNotFoundError:
        raise FileNotFoundError(f"{private_pem} file was not found")


def read_public_pem(public_pem: str):
    """
    reads public key from file
    
    arguments:
            public_pem: path to file with public key, in str
    return:
            d_public_key: object of RSAPublicKey class
    """
    try:
        with open(public_pem, 'rb') as pem_in:
            public_bytes = pem_in.read()
        d_public_key = load_pem_public_key(public_bytes)
        return d_public_key
    except FileNotFoundError:
        raise FileNotFoundError(f"{public_pem} file was not found")


def decrypt_symmetric_key(content: bytes, d_private_key) -> bytes:
    """
    with private key decrypts symmetric key that was encrypted with public key
    
    arguments: 
            content: bytes of encrypted symmetric key
            d_private_key: object of RSAPrivateKey class
    return:
            dc_key: decrypted symmetric key in bytes
    """
    dc_key = d_private_key.decrypt(
        content,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return dc_key