import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers import algorithms as decrepit_algorithms
from cryptography.hazmat.primitives import padding as sym_padding

def encrypt_seed(plain_text: bytes, sym_key: bytes, block_size: int = 128) -> tuple[bytes, bytes]:




def decrypt_seed(cipher_text: bytes, sym_key: bytes, iv: bytes, block_size: int = 128) -> bytes: