from cryptography.hazmat.primitives.asymmetric import rsa, padding as asym_padding
from cryptography.hazmat.primitives import serialization, hashes

def get_asym_padding():




def generate_rsa_keys(public_exponent: int = 65537, key_size: int = 2048) -> tuple[bytes, bytes]:





def encrypt_rsa(public_key_pem: bytes, data: bytes) -> bytes:





def decrypt_rsa(private_key_pem: bytes, encrypted_data: bytes) -> bytes: