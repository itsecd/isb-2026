from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

def encrypt_message(encryption_key: bytes, plaintext: str) -> bytes:
    """
    Шифрование сообщения алгоритмом Blowfish
    """
    initialization_vector = os.urandom(8)
    blowfish_cipher = Cipher(
        algorithms.Blowfish(encryption_key),
        modes.CBC(initialization_vector)
    )
    
    message_bytes = plaintext.encode("utf-8")
    padder = padding.PKCS7(64).padder()
    padded_message = padder.update(message_bytes) + padder.finalize()
    
    encryptor = blowfish_cipher.encryptor()
    ciphertext = encryptor.update(padded_message) + encryptor.finalize()
    
    return initialization_vector + ciphertext

def decrypt_message(decryption_key: bytes, encrypted_data: bytes) -> str:
    """
    Расшифровка сообщения алгоритмом Blowfish
    """
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    
    blowfish_cipher = Cipher(
        algorithms.Blowfish(decryption_key), 
        modes.CBC(iv)
    )
    
    decryptor = blowfish_cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    
    unpadder = padding.PKCS7(64).unpadder()
    plaintext_bytes = unpadder.update(padded_plaintext) + unpadder.finalize()
    
    return plaintext_bytes.decode("utf-8")