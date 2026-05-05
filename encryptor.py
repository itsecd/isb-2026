import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

from auxiliary_functions import read_file, write_file, decrypt_symmetric_key

def encrypt_data(settings):
    """Шифрует данные."""
    
    symmetric_key = decrypt_symmetric_key(settings)
    if symmetric_key is None:
        return
    print(f"Симметричный ключ расшифрован")

    plaintext = read_file(settings['initial_file'])
    if plaintext is None:
        return

    iv = os.urandom(settings['BLOCK_SIZE_BYTES'])
    
    padder = sym_padding.PKCS7(algorithms.SEED.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    final_data = iv + ciphertext

    if not write_file(settings['encrypted_file'], final_data):
        return
        
    print(f"Текст зашифрован и сохранен в: {settings['encrypted_file']}")
    print("Шифрование завершено")