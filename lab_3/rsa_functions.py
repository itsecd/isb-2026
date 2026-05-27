import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from typing import Tuple
from cryptography.exceptions import InvalidSignature, UnsupportedAlgorithm

from file_utils import write_bin_file, read_bin_file


def gen_rsa_keys(key_size: int, public_exponent: int) -> Tuple[rsa.RSAPrivateKey, rsa.RSAPublicKey]:
    """
    Generate public and private keys for RSA

    args:
        key_size: size of RSA key in bits
        public_exponent: RSA public exponent

    return:
        pair of public and private RSA keys
    """
    try:
        keys = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=key_size
        )
        private_key = keys
        public_key = keys.public_key()
        return private_key, public_key
    except ValueError as e:
        raise ValueError(f"RSA parameter error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Failed to create RSA keys: {e}") from e


def serialize_public_key(public_key, public_key_path: str) -> None:
    """
    Save public key in PEM format

    args:
        public_key: public RSA key
        public_key_path: path to save PEM public key
    """
    try:
        os.makedirs(os.path.dirname(public_key_path), exist_ok=True)
        pem_key = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        write_bin_file(public_key_path, pem_key)
    except OSError as e:
        raise OSError(f"Failed to save public key: {e}") from e
    except TypeError as e:
        raise TypeError(f"Invalid key type: {e}") from e


def serialize_private_key(private_key, private_key_path: str) -> None:
    """
    Save private key in PEM format

    args:
        private_key: private RSA key
        private_key_path: path to save PEM private key
    """
    try:
        os.makedirs(os.path.dirname(private_key_path), exist_ok=True)
        pem_key = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        write_bin_file(private_key_path, pem_key)
    except OSError as e:
        raise OSError(f"Failed to save private key: {e}") from e
    except TypeError as e:
        raise TypeError(f"Invalid key type: {e}") from e


def deserialize_public_key(public_key_path: str) -> rsa.RSAPublicKey:
    """
    Load public key from PEM file

    args:
        public_key_path: path to PEM public key file

    return:
        public RSA key
    """
    try:
        pem_data = read_bin_file(public_key_path)
        public_key = load_pem_public_key(pem_data)
        return public_key
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Key file not found: {public_key_path}") from e
    except ValueError as e:
        raise ValueError(f"Error loading PEM key: {e}") from e


def deserialize_private_key(private_key_path: str) -> rsa.RSAPrivateKey:
    """
    Load private key from PEM file

    args:
        private_key_path: path to PEM private key file

    return:
        private RSA key
    """
    try:
        pem_data = read_bin_file(private_key_path)
        private_key = load_pem_private_key(pem_data, password=None)
        return private_key
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Key file not found: {private_key_path}") from e
    except ValueError as e:
        raise ValueError(f"Error loading private key: {e}") from e


def encrypt_data_rsa(text: bytes, public_key) -> bytes:
    """
    Encrypt data with RSA public key

    args:
        text: data to encrypt
        public_key: public RSA key
    
    return:
        encrypted data
    """
    try: 
        c_text = public_key.encrypt(text, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        return c_text
    except ValueError as e:
        raise ValueError(f"RSA encryption error: {e}") from e
    except TypeError as e:
        raise TypeError(f"Invalid key type: {e}") from e
    except (InvalidSignature, UnsupportedAlgorithm) as e:
        raise RuntimeError(f"Cryptographic error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e


def decrypt_data_rsa(text: bytes, private_key) -> bytes:
    """
    Decrypt data with RSA private key

    args:
        text: data to decrypt
        private_key: private RSA key
    
    return:
        decrypted data
    """
    try:
        dc_text = private_key.decrypt(text, padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))
        return dc_text
    except ValueError as e:
        raise ValueError(f"RSA decryption error: {e}") from e
    except TypeError as e:
        raise TypeError(f"Invalid key type: {e}") from e
    except (InvalidSignature, UnsupportedAlgorithm) as e:
        raise RuntimeError(f"Cryptographic error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e