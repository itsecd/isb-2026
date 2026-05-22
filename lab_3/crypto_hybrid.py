
"""
Модуль гибридной криптосистемы (RSA + Blowfish)
"""

import os
from crypto_symmetric import (
    generate_symmetric_key, encrypt_symmetric, decrypt_symmetric,
    save_symmetric_key, load_symmetric_key
)
from crypto_asymmetric import (
    generate_rsa_keypair, save_rsa_private_key, save_rsa_public_key,
    load_rsa_private_key, load_rsa_public_key,
    encrypt_asymmetric, decrypt_asymmetric
)


def generate_hybrid_keys(public_path: str, secret_path: str, 
                          encrypted_sym_key_path: str, 
                          sym_key_length: int = 128) -> dict:
    """
    Генерация ключей гибридной системы.
    
    Args:
        public_path: Путь для сохранения публичного RSA ключа.
        secret_path: Путь для сохранения приватного RSA ключа.
        encrypted_sym_key_path: Путь для сохранения зашифрованного симметричного ключа.
        sym_key_length: Длина симметричного ключа в битах.
    
    Returns:
        Словарь с информацией о сгенерированных ключах.
    """
    sym_key = generate_symmetric_key(sym_key_length)
    rsa_private, rsa_public = generate_rsa_keypair()
    
    save_rsa_private_key(rsa_private, secret_path)
    save_rsa_public_key(rsa_public, public_path)
    save_symmetric_key(sym_key, encrypted_sym_key_path + ".tmp")
    
    encrypted_sym_key = encrypt_asymmetric(rsa_public, sym_key)
    
    with open(encrypted_sym_key_path, 'wb') as f:
        f.write(encrypted_sym_key)
    
    if os.path.exists(encrypted_sym_key_path + ".tmp"):
        os.remove(encrypted_sym_key_path + ".tmp")
    
    return {
        'public_key_path': public_path,
        'private_key_path': secret_path,
        'encrypted_sym_key_path': encrypted_sym_key_path,
        'sym_key_length': sym_key_length
    }


def encrypt_file(input_file: str, output_file: str, 
                 private_key_path: str, encrypted_sym_key_path: str) -> None:
    """
    Шифрование файла с использованием гибридной системы.
    
    Args:
        input_file: Путь к исходному файлу.
        output_file: Путь для сохранения зашифрованного файла.
        private_key_path: Путь к приватному RSA ключу.
        encrypted_sym_key_path: Путь к зашифрованному симметричному ключу.
    """
    rsa_private = load_rsa_private_key(private_key_path)
    
    with open(encrypted_sym_key_path, 'rb') as f:
        encrypted_sym_key = f.read()
    
    sym_key = decrypt_asymmetric(rsa_private, encrypted_sym_key)
    
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    
    iv, ciphertext = encrypt_symmetric(sym_key, plaintext)
    
    with open(output_file, 'wb') as f:
        f.write(iv + ciphertext)


def decrypt_file(input_file: str, output_file: str,
                 private_key_path: str, encrypted_sym_key_path: str) -> None:
    """
    Дешифрование файла с использованием гибридной системы.
    
    Args:
        input_file: Путь к зашифрованному файлу.
        output_file: Путь для сохранения расшифрованного файла.
        private_key_path: Путь к приватному RSA ключу.
        encrypted_sym_key_path: Путь к зашифрованному симметричному ключу.
    """
    rsa_private = load_rsa_private_key(private_key_path)
    
    with open(encrypted_sym_key_path, 'rb') as f:
        encrypted_sym_key = f.read()
    
    sym_key = decrypt_asymmetric(rsa_private, encrypted_sym_key)
    
    with open(input_file, 'rb') as f:
        encrypted_data = f.read()
    
    if len(encrypted_data) < 8:
        raise ValueError("Зашифрованный файл слишком мал")
    
    iv = encrypted_data[:8]
    ciphertext = encrypted_data[8:]
    
    plaintext = decrypt_symmetric(sym_key, iv, ciphertext)
    
    with open(output_file, 'wb') as f:
        f.write(plaintext)