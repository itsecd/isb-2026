import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives import hashes, serialization
from file_utils import read_file


def generate_rsa_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Generates RSA key pair.

    Returns:
        tuple[RSAPrivateKey, RSAPublicKey]: private and public keys
    """
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return private_key, private_key.public_key()


def _get_oaep_padding():
    """
    Returns OAEP padding configuration.

    Returns:
        padding.OAEP: configured padding object
    """
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )


def encrypt_symmetric_key(sym_key: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Encrypts symmetric key using RSA public key.

    Args:
        sym_key (bytes): symmetric key
        public_key (RSAPublicKey): RSA public key

    Returns:
        bytes: encrypted symmetric key
    """
    if not sym_key:
        raise ValueError("Symmetric key cannot be empty")

    return public_key.encrypt(sym_key, _get_oaep_padding())


def decrypt_symmetric_key(encrypted_key_path: str, private_key: RSAPrivateKey) -> bytes:
    """
    Decrypts symmetric key using RSA private key.

    Args:
        encrypted_key_path (str): path to encrypted key file
        private_key (RSAPrivateKey): RSA private key

    Returns:
        bytes: decrypted symmetric key
    """
    encrypted_key = read_file(encrypted_key_path)

    sym_key = private_key.decrypt(encrypted_key, _get_oaep_padding())

    if len(sym_key) != 32:
        raise ValueError("Decrypted symmetric key must be 32 bytes for ChaCha20")

    return sym_key


def save_symmetric_key(key: bytes, filepath: str) -> None:
    """
    Saves binary symmetric key to file.

    Args:
        key (bytes): symmetric key
        filepath (str): output path

    Returns:
        None
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        f.write(key)


def save_public_key(pub_key: RSAPublicKey, filepath: str) -> None:
    """
    Saves RSA public key to PEM file.

    Args:
        pub_key (RSAPublicKey): public key
        filepath (str): output path

    Returns:
        None
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(
            pub_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def load_public_key(filepath: str) -> RSAPublicKey:
    """
    Loads RSA public key from PEM file.

    Args:
        filepath (str): path to file

    Returns:
        RSAPublicKey: loaded public key
    """
    return serialization.load_pem_public_key(read_file(filepath))


def save_private_key(priv_key: RSAPrivateKey, filepath: str) -> None:
    """
    Saves RSA private key to PEM file.

    Args:
        priv_key (RSAPrivateKey): private key
        filepath (str): output path

    Returns:
        None
    """
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    with open(filepath, 'wb') as f:
        f.write(
            priv_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )


def load_private_key(filepath: str) -> RSAPrivateKey:
    """
    Loads RSA private key from PEM file.

    Args:
        filepath (str): path to private key file

    Returns:
        RSAPrivateKey: loaded private key
    """
    return serialization.load_pem_private_key(read_file(filepath), password=None)