import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding as sym_padding

from auxiliary_functions import read_file, write_file

def generate_symmetric_key(settings):
    """Генерирует симметричный ключ SEED."""
    symmetric_key = os.urandom(settings['BLOCK_SIZE_BYTES'])
    print(f"Симметричный ключ SEED сгенерирован.")
    return symmetric_key

def encrypt_data(settings, symmetric_key):
    """Шифрует данные с помощью симметричного ключа SEED."""
    plaintext = read_file(settings['initial_file'])
    if plaintext is None:
        return False

    iv = os.urandom(settings['BLOCK_SIZE_BYTES'])
    
    padder = sym_padding.PKCS7(algorithms.SEED.block_size).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    cipher = Cipher(algorithms.SEED(symmetric_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    final_data = iv + ciphertext

    if not write_file(settings['encrypted_file'], final_data):
        return False
        
    print(f"Текст зашифрован и сохранен в: {settings['encrypted_file']}")
    print("Шифрование завершено")
    return True

def decrypt_data(settings, symmetric_key):
    """Дешифрует данные с помощью симметричного ключа SEED."""
    encrypted_data = read_file(settings['encrypted_file'])
    if encrypted_data is None:
        return False
    
    block_size = settings['BLOCK_SIZE_BYTES']
    if len(encrypted_data) < block_size:
        print("Зашифрованный файл слишком мал или поврежден.")
        return False
        
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
        return False

    if not write_file(settings['decrypted_file'], plaintext):
        return False
        
    print(f"Текст расшифрован и сохранен в: {settings['decrypted_file']}")
    print("Дешифрование завершено")
    return True