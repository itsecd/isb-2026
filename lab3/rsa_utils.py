from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

from config_loader import load_crypto_config


CONFIG = load_crypto_config()

RSA_KEY_SIZE = CONFIG["rsa_key_size"]

RSA_PUBLIC_EXPONENT = CONFIG[
    "rsa_public_exponent"
]

from file_utils import (
    read_bytes,
    write_bytes,
)


def generate_private_key():
    """
    Generate RSA private key.

    return:
        RSA private key object
    """

    return rsa.generate_private_key(
        public_exponent=RSA_PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )


def save_private_key(private_key, private_key_path):
    """
    Save RSA private key to PEM file.

    args:
        private_key:
            RSA private key object

        private_key_path:
            path to PEM private key file
    """

    write_bytes(
        private_key_path,
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ),
    )


def save_public_key(public_key, public_key_path):
    """
    Save RSA public key to PEM file.

    args:
        public_key:
            RSA public key object

        public_key_path:
            path to PEM public key file
    """

    write_bytes(
        public_key_path,
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ),
    )


def load_public_key(public_key_path):
    """
    Load RSA public key from PEM file.

    args:
        public_key_path:
            path to PEM public key file

    return:
        RSA public key object
    """

    return serialization.load_pem_public_key(
        read_bytes(public_key_path)
    )


def load_private_key(private_key_path):
    """
    Load RSA private key from PEM file.

    args:
        private_key_path:
            path to PEM private key file

    return:
        RSA private key object
    """

    return serialization.load_pem_private_key(
        read_bytes(private_key_path),
        password=None,
    )


def rsa_oaep_padding():
    """
    Create RSA-OAEP padding object.

    return:
        RSA-OAEP padding configuration
    """

    return padding.OAEP(
        mgf=padding.MGF1(
            algorithm=hashes.SHA256()
        ),
        algorithm=hashes.SHA256(),
        label=None,
    )


def generate_rsa_keys(public_key_path, private_key_path):
    """
    Generate RSA key pair and save keys.

    args:
        public_key_path:
            path to PEM public key file

        private_key_path:
            path to PEM private key file

    return:
        generated RSA key pair
    """

    private_key = generate_private_key()
    public_key = private_key.public_key()

    save_private_key(
        private_key,
        private_key_path,
    )

    save_public_key(
        public_key,
        public_key_path,
    )

    return private_key, public_key


def encrypt_symmetric_key(
    sym_key,
    public_key_path,
    encrypted_key_path,
):
    """
    Encrypt symmetric key using RSA public key.

    args:
        sym_key:
            symmetric encryption key

        public_key_path:
            path to RSA public key

        encrypted_key_path:
            path to encrypted symmetric key file
    """

    public_key = load_public_key(public_key_path)

    encrypted_key = public_key.encrypt(
        sym_key,
        rsa_oaep_padding(),
    )

    write_bytes(
        encrypted_key_path,
        encrypted_key,
    )


def decrypt_symmetric_key(
    private_key_path,
    encrypted_key_path,
):
    """
    Decrypt symmetric key using RSA private key.

    args:
        private_key_path:
            path to RSA private key

        encrypted_key_path:
            path to encrypted symmetric key file

    return:
        decrypted symmetric key
    """

    private_key = load_private_key(
        private_key_path
    )

    encrypted_key = read_bytes(
        encrypted_key_path
    )

    return private_key.decrypt(
        encrypted_key,
        rsa_oaep_padding(),
    )
