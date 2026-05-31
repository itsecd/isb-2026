import os
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

def generate_asymmetric():
    """
    Generate pair of RSA keys
    Returns:
        tuple: (private_key, public_key)
    """
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    private_key = keys
    public_key = keys.public_key()
    return private_key, public_key

def generate_symmetric_key(key_size):
    """
    Generate random key for symmetric algorithm (Cammelia)
    Args:
        key_size(int): Key size in bits
    Returns:
        bytes: symmetric key
    """
    return os.urandom(key_size // 8)

def encrypt_symmetric_key(symmetric_key, public_key):
    """
    Encrypt the key for symmetric algorithm
    Args:
        public_key: public RSA key
        symmetric_key(bytes): symmetric key
    Returns:
        encrypted_symmetric_ke(bytes): encrypted symmetric key
    """
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_symmetric_key

