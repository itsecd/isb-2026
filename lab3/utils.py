import os
from cryptography.hazmat.primitives import padding, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)

SEED_KEY_SIZE = 16
SEED_BLOCK_SIZE = 128
RSA_KEY_SIZE = 2048
PUBLIC_EXPONENT = 65537
IV_SIZE = 16


def generate_symmetric_key():
    return os.urandom(SEED_KEY_SIZE)


def generate_asymmetric_keys():
    private_key = rsa.generate_private_key(
        public_exponent=PUBLIC_EXPONENT,
        key_size=RSA_KEY_SIZE,
    )
    public_key = private_key.public_key()
    return private_key, public_key


def serialize_private_key(private_key, path):
    pem_data = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )
    with open(path, 'wb') as f:
        f.write(pem_data)


def serialize_public_key(public_key, path):
    pem_data = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    with open(path, 'wb') as f:
        f.write(pem_data)


def load_private_key(path):
    with open(path, 'rb') as f:
        pem_bytes = f.read()
    return load_pem_private_key(pem_bytes, password=None)


def load_public_key(path):
    with open(path, 'rb') as f:
        pem_bytes = f.read()
    return load_pem_public_key(pem_bytes)


def rsa_encrypt(public_key, data):
    return public_key.encrypt(
        data,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def rsa_decrypt(private_key, ciphertext):
    return private_key.decrypt(
        ciphertext,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )


def pad_data(data):
    padder = padding.ANSIX923(SEED_BLOCK_SIZE).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(padded_data):
    unpadder = padding.ANSIX923(SEED_BLOCK_SIZE).unpadder()
    return unpadder.update(padded_data) + unpadder.finalize()


def seed_encrypt(key, plaintext):
    iv = os.urandom(IV_SIZE)
    cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded_data = pad_data(plaintext)
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv, ciphertext


def seed_decrypt(key, iv, ciphertext):
    cipher = Cipher(algorithms.SEED(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    return unpad_data(padded_data)


def save_bytes(data, path):
    with open(path, 'wb') as f:
        f.write(data)


def load_bytes(path):
    with open(path, 'rb') as f:
        return f.read()