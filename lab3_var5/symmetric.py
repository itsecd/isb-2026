import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding

def encrypt_text(text: str, key: bytes) -> bytes:
    """
    Шифровка текста алгоритмом CAST5
    """
    data = text.encode('utf-8')
    padder = sym_padding.PKCS7(64).padder()
    padded_data = padder.update(data) + padder.finalize()
    
    iv = os.urandom(8)
    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext

def decrypt_text(encrypt_text: bytes, key: bytes) -> str:
    """
    Дешифрование данных алгоритмом CAST5
    """
    iv = encrypt_text[:8]
    ciphertext = encrypt_text[8:]
    
    cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = sym_padding.PKCS7(64).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data.decode('utf-8')