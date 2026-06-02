"""
Asymmetric encryption module using RSA (OAEP padding).

Provides complete RSA-2048 functionality including key pair generation,
serialization to/from PEM files, and OAEP-encrypted data transfer.
Used primarily to securely encrypt and decrypt symmetric keys.
"""

from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes, serialization
from config import config
from file_utils import save_bytes, load_bytes
from exceptions import KeyGenerationError, KeyLoadError, EncryptionError, DecryptionError


def rsa_oaep_padding():
    """
    Create RSA-OAEP padding configuration with SHA-256.

    OAEP (Optimal Asymmetric Encryption Padding) provides:
    - CPA/CCA security
    - Integrity protection
    - Using MGF1 mask generation function with SHA-256

    Returns:
        padding.OAEP: OAEP padding object configured for SHA-256.

    Example:
        >>> padding = rsa_oaep_padding()
        >>> encrypted = public_key.encrypt(data, padding)
    """
    return asym_padding.OAEP(
        mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None,
    )


def generate_asymmetric_keys():
    """
    Generate RSA key pair (private and public keys).

    Uses RSA_KEY_SIZE (2048 bits) and PUBLIC_EXPONENT (65537) from config.

    Returns:
        tuple: (private_key, public_key) where both are cryptography key objects.

    Raises:
        KeyGenerationError: If RSA key generation fails.

    Example:
        >>> private_key, public_key = generate_asymmetric_keys()
    """
    try:
        private_key = rsa.generate_private_key(
            public_exponent=config.rsa_public_exponent,
            key_size=config.rsa_key_size,
        )
        public_key = private_key.public_key()
        return private_key, public_key
    except Exception as e:
        raise KeyGenerationError(f"Failed to generate RSA keys: {e}")


def serialize_private_key(private_key, path):
    """
    Serialize RSA private key to PEM format and save to file.

    Output format: TraditionalOpenSSL (PKCS#1) PEM without encryption.

    Args:
        private_key: RSA private key object from cryptography.
        path (str): File path where PEM key will be saved.

    Raises:
        RuntimeError: If serialization or file write fails.
    """
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
    """
    Serialize RSA public key to PEM format and save to file.

    Output format: SubjectPublicKeyInfo (PKCS#8) PEM.

    Args:
        public_key: RSA public key object from cryptography.
        path (str): File path where PEM key will be saved.

    Raises:
        RuntimeError: If serialization or file write fails.
    """
    try:
        pem_data = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        save_bytes(pem_data, path)
    except Exception as e:
        raise RuntimeError(f"Failed to serialize public key: {e}")


def load_private_key(path):
    """
    Load RSA private key from PEM file.

    Args:
        path (str): Path to PEM file containing private key.

    Returns:
        RSA private key object ready for decryption.

    Raises:
        KeyLoadError: If file cannot be read or PEM parsing fails.

    Example:
        >>> private_key = load_private_key('private.pem')
    """
    try:
        pem_bytes = load_bytes(path)
        return serialization.load_pem_private_key(pem_bytes, password=None)
    except Exception as e:
        raise KeyLoadError(f"Failed to load private key: {e}")


def load_public_key(path):
    """
    Load RSA public key from PEM file.

    Args:
        path (str): Path to PEM file containing public key.

    Returns:
        RSA public key object ready for encryption.

    Raises:
        KeyLoadError: If file cannot be read or PEM parsing fails.

    Example:
        >>> public_key = load_public_key('public.pem')
    """
    try:
        pem_bytes = load_bytes(path)
        return serialization.load_pem_public_key(pem_bytes)
    except Exception as e:
        raise KeyLoadError(f"Failed to load public key: {e}")


def rsa_encrypt(public_key, data):
    """
    Encrypt data using RSA public key with OAEP padding.

    Maximum data size: RSA_KEY_SIZE/8 - 2*hash_size - 2
    For RSA-2048 and SHA-256: 256 - 2*32 - 2 = 190 bytes.

    Args:
        public_key: RSA public key object.
        data (bytes): Data to encrypt (must not exceed maximum payload size).

    Returns:
        bytes: Encrypted ciphertext.

    Raises:
        EncryptionError: If encryption fails (e.g., data too large).

    Example:
        >>> encrypted = rsa_encrypt(public_key, b'Symmetric key')
    """
    try:
        return public_key.encrypt(data, rsa_oaep_padding())
    except Exception as e:
        raise EncryptionError(f"RSA encryption failed: {e}")


def rsa_decrypt(private_key, ciphertext):
    """
    Decrypt RSA-OAEP encrypted ciphertext using private key.

    Args:
        private_key: RSA private key object.
        ciphertext (bytes): Encrypted data to decrypt.

    Returns:
        bytes: Decrypted plaintext.

    Raises:
        DecryptionError: If decryption fails (e.g., corrupted ciphertext).

    Example:
        >>> plaintext = rsa_decrypt(private_key, encrypted)
    """
    try:
        return private_key.decrypt(ciphertext, rsa_oaep_padding())
    except Exception as e:
        raise DecryptionError(f"RSA decryption failed: {e}")