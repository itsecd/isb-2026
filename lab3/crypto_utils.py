import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization

from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key
)

def generate_cast5_key(key_size_bits: int) -> bytes:

    if key_size_bits < 40 or key_size_bits > 128 or key_size_bits % 8 != 0:
        raise ValueError(
            "Длина ключа CAST5 должна быть от 40 до 128 бит с шагом 8"
        )

    return os.urandom(key_size_bits // 8)


def encrypt_file_cast5(input_path: str,
                       output_path: str,
                       key: bytes):

    with open(input_path, "rb") as f:
        data = f.read()

    padder = padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()

    iv = os.urandom(8)

    cipher = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()

    encrypted_data = encryptor.update(
        padded_data
    ) + encryptor.finalize()

    with open(output_path, "wb") as f:
        # сначала IV
        f.write(iv)
        # затем ciphertext
        f.write(encrypted_data)


def decrypt_file_cast5(input_path: str,
                       output_path: str,
                       key: bytes):

    with open(input_path, "rb") as f:
        content = f.read()

    iv = content[:8]
    encrypted_data = content[8:]

    cipher = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()

    decrypted_padded = decryptor.update(
        encrypted_data
    ) + decryptor.finalize()

    unpadder = padding.PKCS7(64).unpadder()

    decrypted_data = unpadder.update(
        decrypted_padded
    ) + unpadder.finalize()

    with open(output_path, "wb") as f:
        f.write(decrypted_data)

def generate_rsa_keys():

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    public_key = private_key.public_key()

    return private_key, public_key


def save_private_key(private_key, path: str):

    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,

                format=serialization.PrivateFormat.TraditionalOpenSSL,

                encryption_algorithm=serialization.NoEncryption()
            )
        )


def save_public_key(public_key, path: str):

    with open(path, "wb") as f:
        f.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,

                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def load_private_key(path: str):

    with open(path, "rb") as f:
        return load_pem_private_key(
            f.read(),
            password=None
        )


def load_public_key(path: str):

    with open(path, "rb") as f:
        return load_pem_public_key(
            f.read()
        )

def encrypt_symmetric_key(key: bytes,
                          public_key):

    encrypted_key = public_key.encrypt(
        key,

        asym_padding.OAEP(
            mgf=asym_padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None
        )
    )

    return encrypted_key


def decrypt_symmetric_key(encrypted_key: bytes,
                          private_key):

    decrypted_key = private_key.decrypt(
        encrypted_key,

        asym_padding.OAEP(
            mgf=asym_padding.MGF1(
                algorithm=hashes.SHA256()
            ),

            algorithm=hashes.SHA256(),

            label=None
        )
    )

    return decrypted_key