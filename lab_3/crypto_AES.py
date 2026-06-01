import os

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def encrypt_aes(plaintext, key):
    """
    Шифрование данных AES-CBC
    
    Args:
        plaintext: байты для шифрования
        key: ключ AES (16, 24 или 32 байта)
    
    Returns:
        bytes: IV (16 байт) + зашифрованные данные
    """
    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(128).padder()
    
    padded = padder.update(plaintext) + padder.finalize()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    
    return iv + ciphertext


def decrypt_aes(ciphertext, key):
    """
    Дешифрование данных AES-CBC
    
    Args:
        ciphertext: байты, содержащие IV (первые 16 байт) и зашифрованные данные
        key: ключ AES (16, 24 или 32 байта)
    
    Returns:
        bytes: расшифрованные данные
    """
    if len(ciphertext) < 16:
        raise ValueError("Ciphertext too short, must contain at least 16 bytes for IV")
    
    iv = ciphertext[:16]
    data = ciphertext[16:]
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = padding.PKCS7(128).unpadder()
    
    decrypted_padded = decryptor.update(data) + decryptor.finalize()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    
    return decrypted