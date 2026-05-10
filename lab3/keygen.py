import os
import settings_loader
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding


def generate_symmetric_key(key_size):
    return os.urandom(key_size // 8)

def generate_asymmetric_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def save_asymmetric_keys(private_key, public_key, private_path, public_path):
    with open(private_path, "wb") as f:
        f.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open(public_path, "wb") as f:
        f.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

def encrypt_symmetric_key(sym_key, public_key, path):
    encrypted_sym_key = public_key.encrypt(
        sym_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    with open(path, "wb") as f:
        f.write(encrypted_sym_key)


def keygen(settings_path):
    settings = settings_loader.load(settings_path)

    sym_key = generate_symmetric_key(int(settings['aes_key_size']))
    private_key, public_key = generate_asymmetric_keys()

    save_asymmetric_keys(private_key, public_key, settings['private_key'], settings['public_key'])
    encrypt_symmetric_key(sym_key, public_key, settings['symmetric_key'])
    return "Keys successfully generated and saved."