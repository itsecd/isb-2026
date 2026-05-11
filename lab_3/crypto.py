import os
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.decrepit.ciphers.algorithms import IDEA
from cryptography.hazmat.primitives import padding, hashes
from cryptography.hazmat.primitives.asymmetric import padding as assym_padding, rsa

def generate_idea_key() -> bytes:
    """Генерирует 16-байтный ключ для IDEA."""
    return os.urandom(16)

def generate_rsa_keypair():
    """Генерирует пару RSA ключей (private, public)."""
    keys = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    return keys, keys.public_key()

def encrypt_idea_key_rsa(idea_key: bytes, public_key) -> bytes:
    """Шифрует симметричный ключ IDEA с помощью открытого ключа RSA."""
    return public_key.encrypt(
        idea_key,
        assym_padding.OAEP(
            mgf=assym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def decrypt_idea_key_rsa(encrypted_key: bytes, private_key) -> bytes:
    """Дешифрует симметричный ключ IDEA с помощью закрытого ключа RSA."""
    return private_key.decrypt(
        encrypted_key, 
        assym_padding.OAEP(
            mgf=assym_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

def encrypt_data_idea(text: bytes, idea_key: bytes) -> tuple[bytes, bytes]:
    """Шифрует данные алгоритмом IDEA (возвращает IV и зашифрованный текст)."""
    padder = padding.ANSIX923(64).padder()
    padded_text = padder.update(text) + padder.finalize()
    
    iv = os.urandom(8) 
    cipher = Cipher(IDEA(idea_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    cyph_text = encryptor.update(padded_text) + encryptor.finalize()
    
    return iv, cyph_text

def decrypt_data_idea(actual_cyph_text: bytes, iv: bytes, idea_key: bytes) -> bytes:
    """Дешифрует данные алгоритмом IDEA."""
    cipher = Cipher(IDEA(idea_key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    dc_text = decryptor.update(actual_cyph_text) + decryptor.finalize()
    
    unpadder = padding.ANSIX923(64).unpadder()
    unpadded_dc_text = unpadder.update(dc_text) + unpadder.finalize()
    
    return unpadded_dc_text