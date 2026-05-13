import os
from typing import Tuple
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes


def gen_assym_key() -> Tuple[RSAPublicKey, RSAPrivateKey]:
    '''
    Generates asymmetric keys using the RSA method.

    Returns:
        Tuple[bytes, bytes]: A tuple consisting of a public key and a private key.
    '''

    keys = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_key = keys
    public_key = keys.public_key()

    return public_key, private_key


def rsa_encryption(sym_key: bytes, public_key: RSAPublicKey) -> bytes:
    '''
    Asymmetrically encrypts a symmetric key.

    Args:
        sym_key (bytes): A symmetric key.
        public_key (RSAPublicKey): A public key for RSA method.

    Returns:
        bytes: Encrypted symmetric key.
    '''

    c_key = public_key.encrypt(
        sym_key, 
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))
    
    return c_key


def rsa_decryption(c_key: bytes, private_key: RSAPrivateKey) -> bytes:
    '''
    Asymmetrically decrypts an encrypted key.

    Args:
        c_key (bytes): An encrypted symmetric key.
        private_key (RSAPrivateKey): A private key for RSA method.

    Returns:
        bytes: Decrypted symmetric key.
    '''

    dc_key = private_key.decrypt(
        c_key,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None))
    
    return dc_key