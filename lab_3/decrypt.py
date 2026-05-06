import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
from cryptography.hazmat.primitives.asymmetric import padding as asymmetric_padding
from file_utils import read_file
from encrypt import unpack_encrypted_data

def load_encrypted_file(filepath: str) -> tuple[bytes, bytes]:
    try:
        with open(filepath, 'rb') as enc_file:
            data = enc_file.read()
        return unpack_encrypted_data(data)
    
    except Exception as e:
        raise RuntimeError(f"Couldn't load encrypted text {filepath}") from e


def decrypt_symmetric_key(encrypted_key_path: str, private_key) -> bytes:
    encrypted_key = read_file(encrypted_key_path)

    sym_key = private_key.decrypt(
        encrypted_key,
        asymmetric_padding.OAEP(
            mgf=asymmetric_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    if len(sym_key) != 32:
        raise ValueError("Decrypted symmetric key must be 32 bytes for ChaCha20")
    
    return sym_key


def chacha20_decrypt(ciphertext: bytes, key: bytes, nonce: bytes) -> bytes:
    if len(key) != 32:
        raise ValueError("ChaCha20 key must be exactly 32 bytes (256 bits)")
    if len(nonce) != 16:
        raise ValueError("Nonce must be exactly 16 bytes (128 bits)")

    cipher = Cipher(
        algorithms.ChaCha20(key, nonce),
        mode=None
    )

    decryptor = cipher.decryptor()
    return decryptor.update(ciphertext) + decryptor.finalize()