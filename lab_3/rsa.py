from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def generate_key_pair() -> tuple:
    """
    Generate RSA keypair.
    :return: private key, public key
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    return private_key, private_key.public_key()


def save_public_key(public_key, path: str) -> None:
    """
    Serialize public key.
    :param public_key: public key
    :param path: path where to save public key
    """
    with open(path, 'wb') as public_out:
        public_out.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))


def save_private_key(private_key, path: str) -> None:
    """
    Serialize private key.
    :param private_key: private key
    :param path: path where to save public key
    """
    with open(path, 'wb') as private_out:
        private_out.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))


def load_private_key(path: str):
    """
    Deserialize private key.
    :param path: private key path
    :return: private key
    """
    with open(path, 'rb') as private_file:
        return load_pem_private_key(private_file.read(), password=None)


def encrypt_rsa(public_key, data: bytes) -> bytes:
    """
    Encrypt data using RSA.
    :param public_key: public key
    :param data: data to encrypt
    :return: encrypted data
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def decrypt_rsa(private_key, data: bytes) -> bytes:
    """
    Decrypt data using RSA.
    :param private_key: private key
    :param data: data to decrypt
    :return: decrypted data
    """
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
