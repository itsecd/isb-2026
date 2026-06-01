import os
import RSA
import text

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

def encrypt(text_file_path: str, symmetric_key_path: str, private_key_pem_path: str, encrypted_file_path: str):
    """
    Encrypt rtext and save result to file
    Args:
        text_file_path(str): Path to the plaintext
        symmetric_key_path(str): Path to the encrypted symmetric Camellia key
        private_key_pem_path(str): Path to the private RSA key for Camellia key decrypting
        encrypted_file_path(str): Save path for encrypted text
    """
    plaintext = text.read_text(text_file_path)
    
    iv = os.urandom(16)
    
    key = RSA.decrypt_symmetric_key(private_key_pem_path, symmetric_key_path)

    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    encrypted_text = encryptor.update(padded_data) + encryptor.finalize()

    text.save_text(iv + encrypted_text, encrypted_file_path)

def decrypt(text_file_path: str, symmetric_key_path: str, private_key_pem_path: str, decrypted_file_path: str):
    """
    Decrypt the ciphertext and save result to file
    Args:
        text_file_path(str): Path to the ciphertext
        symmetric_key_path(str): Path to the encrypted symmetric Camellia key
        private_key_pem_path(str): Path to the private RSA key for Camellia key decrypting
        decrypted_file_path(str): Save path for decrypted text
    """
    iv, encrypted = text.read_encrypted(text_file_path)

    key = RSA.decrypt_symmetric_key(private_key_pem_path, symmetric_key_path)  

    cipher = Cipher(algorithms.Camellia(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()

    text.save_text(decrypted, decrypted_file_path)