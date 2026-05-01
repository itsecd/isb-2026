import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.asymmetric import padding as asym_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.serialization import load_pem_private_key

def encrypt(
    path_original_text: str,
    path_asymmetric_private_text: str,
    path_symmetric_key: str,
    path_cipher_text: str,
) -> None:
    with open(path_symmetric_key, mode="rb") as key_file:
        symmetric_key = key_file.read()

    with open(path_asymmetric_private_text, "rb") as pem_in:
        private_bytes = pem_in.read()
        private_key = load_pem_private_key(
            private_bytes,
            password=None,
        )

    symmetric_key = private_key.decrypt(
        symmetric_key,
        asym_padding.OAEP(
            mgf=asym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None,
        ),
    )

    with open(path_original_text, "rb") as f:
        text = f.read()

    padder = padding.ANSIX923(128).padder()
    text = padder.update(text) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    c_text = encryptor.update(text) + encryptor.finalize()

    with open(path_cipher_text, "wb") as f:
        f.write(iv + c_text)