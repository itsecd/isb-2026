from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from exceptions import KeyLoadError, KeyGenerationError, DecryptionError
from file_utils import read_bytes, write_bytes


def rsa_oaep_padding():
    """
    Create RSA-OAEP padding object.

    Returns:
        RSA-OAEP padding configuration.
    """
    return padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def generate_private_key(key_size, public_exponent):
    """
    Generate RSA private key.

    Args:
        key_size: RSA key size in bits.
        public_exponent: RSA public exponent.

    Returns:
        RSA private key object.

    Raises:
        KeyGenerationError: If key generation fails.
    """
    try:
        return rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size,
        )
    except Exception as exc:
        raise KeyGenerationError(f"Failed to generate RSA private key: {exc}") from exc


def save_private_key(private_key, private_key_path):
    """
    Save RSA private key to PEM file.

    Args:
        private_key: RSA private key object.
        private_key_path: Path to PEM private key file.

    Raises:
        FileOperationError: If file cannot be written.
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

    Args:
        public_key: RSA public key object.
        public_key_path: Path to PEM public key file.

    Raises:
        FileOperationError: If file cannot be written.
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

    Args:
        public_key_path: Path to PEM public key file.

    Returns:
        RSA public key object.

    Raises:
        KeyLoadError: If key cannot be loaded.
    """
    try:
        return serialization.load_pem_public_key(read_bytes(public_key_path))
    except Exception as exc:
        raise KeyLoadError(f"Failed to load public key from {public_key_path}: {exc}") from exc


def load_private_key(private_key_path):
    """
    Load RSA private key from PEM file.

    Args:
        private_key_path: Path to PEM private key file.

    Returns:
        RSA private key object.

    Raises:
        KeyLoadError: If key cannot be loaded.
    """
    try:
        return serialization.load_pem_private_key(
            read_bytes(private_key_path),
            password=None,
        )
    except Exception as exc:
        raise KeyLoadError(f"Failed to load private key from {private_key_path}: {exc}") from exc


def generate_rsa_keys(public_key_path, private_key_path, key_size, public_exponent):
    """
    Generate RSA key pair and save keys.

    Args:
        public_key_path: Path to PEM public key file.
        private_key_path: Path to PEM private key file.
        key_size: RSA key size in bits.
        public_exponent: RSA public exponent.

    Returns:
        Generated RSA key pair (private_key, public_key).

    Raises:
        KeyGenerationError: If key generation fails.
        FileOperationError: If files cannot be written.
    """
    private_key = generate_private_key(key_size, public_exponent)
    public_key = private_key.public_key()

    save_private_key(private_key, private_key_path)
    save_public_key(public_key, public_key_path)

    return private_key, public_key


def encrypt_symmetric_key(sym_key, public_key_path, encrypted_key_path):
    """
    Encrypt symmetric key using RSA public key.

    Args:
        sym_key: Symmetric encryption key.
        public_key_path: Path to RSA public key.
        encrypted_key_path: Path to encrypted symmetric key file.

    Raises:
        KeyLoadError: If public key cannot be loaded.
        FileOperationError: If encrypted key cannot be written.
    """
    public_key = load_public_key(public_key_path)
    encrypted_key = public_key.encrypt(sym_key, rsa_oaep_padding())
    write_bytes(encrypted_key_path, encrypted_key)


def decrypt_symmetric_key(private_key_path, encrypted_key_path):
    """
    Decrypt symmetric key using RSA private key.

    Args:
        private_key_path: Path to RSA private key.
        encrypted_key_path: Path to encrypted symmetric key file.

    Returns:
        Decrypted symmetric key.

    Raises:
        KeyLoadError: If private key cannot be loaded.
        FileOperationError: If encrypted key cannot be read.
        DecryptionError: If decryption fails.
    """
    private_key = load_private_key(private_key_path)
    encrypted_key = read_bytes(encrypted_key_path)

    try:
        return private_key.decrypt(encrypted_key, rsa_oaep_padding())
    except Exception as exc:
        raise DecryptionError(f"Failed to decrypt symmetric key: {exc}") from exc
