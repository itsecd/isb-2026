import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

from auxiliary_functions import read_file, write_file, decrypt_symmetric_key

def decrypt_data(settings):
    """Дешифрует данные."""

    symmetric_key = decrypt_symmetric_key(settings)
    if symmetric_key is None:
        return
    print(f"Симметричный ключ расшифрован")

    encrypted_data = read_file(settings['encrypted_file'])
    if encrypted_data is None:
        return
    
    block_size = settings['BLOCK_SIZE_BYTES']
    if len(encrypted_data) < block_size:
        print("Зашифрованный файл слишком мал или поврежден.")
        return
        
    iv = encrypted_data[:block_size]
    ciphertext = encrypted_data[block_size:]

    try:
        cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

        unpadder = sym_padding.PKCS7(algorithms.SEED.block_size).unpadder()
        plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()
    except Exception as e:
        print(f"Ошибка дешифрования данных: {e}")
        return

    if not write_file(settings['decrypted_file'], plaintext):
        return
        
    print(f"Текст расшифрован и сохранен в: {settings['decrypted_file']}")
    print("Дешифрование завершено")