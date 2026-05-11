import os
import settings_loader
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def generate_symmetric_key(key_size):
    """
    Generates random key for sym algorythm(AES)
    Args:
        key_size(int): Key size in bits
    Returns:
        bytes: sym key
    """
    return os.urandom(key_size // 8)

def generate_asymmetric_keys():
    """
    Generates pair of RSA keys
    Returns:
        tuple: (private_key, public_key)
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def save_asymmetric_keys(private_key, public_key, private_path, public_path):
    """
    Serializing asym keys and saving them in .PEM files
    Args:
        private_key: object of private key
        public_key: object of public key
        private_path: path to save private key
        public_path: path to save public key
    """
    with open(private_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(public_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def encrypt_symmetric_key(sym_key, public_key, path):
    """
    Encrypting sym key with public RSA key and save result
    Args:
        sym_key(bytes): symmetric key
        public_key: object of public RSA key
        path(str): path to save encrypted sym key
    """
    encrypted_sym_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(path, "wb") as f:
        f.write(encrypted_sym_key)


def keygen(settings_path):
    """
    Key generation function
    Args:
        settings_path(str): path to JSON settings file
    Returns:
        str: message of successful generation
    """
    settings = settings_loader.load(settings_path)

    sym_key = generate_symmetric_key(int(settings['aes_key_size']))
    private_key, public_key = generate_asymmetric_keys()

    save_asymmetric_keys(private_key, public_key, settings['private_key'], settings['public_key'])
    encrypt_symmetric_key(sym_key, public_key, settings['symmetric_key'])
    return "Keys successfully generated and saved."