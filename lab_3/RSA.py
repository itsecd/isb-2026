import json
from typing import Optional, Dict, Any

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey,
)
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def load_rsa_settings(config_path: str = "config.json") -> Dict[str, Any]:
    """
    Loads RSA settings from configuration file.
    """
    try:
        with open(config_path, "r", encoding="utf-8-sig") as f:
            config = json.load(f)
        return {
            "key_size": config.get("rsa_key_size", 2048),
            "public_exponent": config.get("rsa_public_exponent", 65537)
        }
    except Exception as e:
        print(f"Warning: Could not load RSA settings from config: {e}")
        return {"key_size": 2048, "public_exponent": 65537}


def generate_rsa_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    """
    Generates RSA key pair using settings from config file.
    """
    settings = load_rsa_settings()

    private_key = rsa.generate_private_key(
        public_exponent=settings["public_exponent"],
        key_size=settings["key_size"],
    )
    return private_key, private_key.public_key()


def load_private_key(path: str, password: Optional[bytes] = None) -> RSAPrivateKey:
    """
    Loads RSA private key from PEM file.
    """
    try:
        with open(path, "rb") as f:
            return load_pem_private_key(f.read(), password=password)
    except FileNotFoundError:
        raise FileNotFoundError(f"Private key file not found: {path}")
    except Exception as e:
        raise Exception(f"Failed to load private key: {e}")


def load_public_key(path: str):
    """
    Loads RSA public key from PEM file.
    """
    from cryptography.hazmat.primitives.serialization import load_pem_public_key

    try:
        with open(path, "rb") as f:
            return load_pem_public_key(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Public key file not found: {path}")
    except Exception as e:
        raise Exception(f"Failed to load public key: {e}")


def encrypt(data: bytes, public_key: RSAPublicKey) -> bytes:
    """
    Encrypts data using RSA-OAEP.
    """
    return public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def decrypt(data: bytes, private_key: RSAPrivateKey) -> bytes:
    """
    Decrypts data using RSA-OAEP.
    """
    return private_key.decrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )