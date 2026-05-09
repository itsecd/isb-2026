import os
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key


def generate_symmetric_key():
    """
    generates key for symmetric algorithm

    arguments: -
    return: 
            key: 16 random bytes
    """

    key = os.urandom(16)
    return key


def generate_asymmetric_keys():
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


def write_public_key(public_key, public_pem):
    """
    serializes public key to file

    arguments:
            public_key: object of RSAPublicKey class
            public_pem: path to file, where public_key is serialized, in str
    return: -
    """

    with open(public_pem, 'wb') as public_out:
        public_out.write(public_key.public_bytes(encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo))


def write_private_key(private_key, private_pem):
    """
    serializes private key to file

    arguments:
            private_key: object of RSAPrivateKey class
            private_pem: path to file, where private_key is serialized, in str
    return: -
    """

    with open(private_pem, 'wb') as private_out:
        private_out.write(private_key.private_bytes(encoding=serialization.Encoding.PEM,
              format=serialization.PrivateFormat.TraditionalOpenSSL,
              encryption_algorithm=serialization.NoEncryption()))


def encrypt_symmetric_key(key, public_key):
    """
    encrypts symmetric encryption key with public key

    arguments:
            key: 16 random bytes
            public_key: object of RSAPublicKey class
    return:
            encrypt_key: bytes of encrypted symmetric key
    """

    encrypt_key = public_key.encrypt(key, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return encrypt_key


def write_symmetric_key(encrypt_key, file_name):
    """
    serializes encrypt symmetric algorithm key to file

    arguments: 
            encrypt_key: bytes of encrypted symmetric key
            file_name: path to file, where encrypt key is serialized, in str
    return: -
    """
    
    with open(file_name, 'wb') as key_file:
        key_file.write(encrypt_key)


def read_symmetric_key(symmetric_key_file):
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


def read_private_pem(private_pem):
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
        d_private_key = load_pem_private_key(private_bytes,password=None,)
        return d_private_key
    
    except FileNotFoundError:
        raise FileNotFoundError(f"{private_pem} file was not found")


def decrypt_symmetric_key(content, d_private_key):
    """
    with private key decrypts symmetric key that was encrypted with public key

    arguments: 
            content: bytes of encrypted symmetric key
            d_private_key: object of RSAPrivateKey class
    return:
            dc_key: decrypted symmetric key in form of 16 bytes
    """

    dc_key = d_private_key.decrypt(content,padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),algorithm=hashes.SHA256(),label=None))
    return dc_key