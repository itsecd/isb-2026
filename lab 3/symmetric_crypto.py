import os
from cryptography.hazmat.primitives import padding as symmetric_padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from file_utils import read_binary_file, write_binary_file

def generate_symmetric_key() -> bytes:
    """
    Шифрует файл алгоритмом AES-CBC.
    """
    return os.urandom(32)

def encrypt_file_aes(input_file_path: str, output_file_path: str, symmetric_key: str) -> None:
    """
    Шифрует файл алгоритмом AES-CBC.
    """
    plaintext = read_binary_file(input_file_path)

    padder = symmetric_padding.ANSIX923(128).padder()
    padder_plaintext = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(16)

    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))

    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padder_plaintext) + encryptor.finalize()

    write_binary_file(output_file_path, iv + ciphertext)


def decrypt_file_aes(input_file_path: str, output_file_path: str, symmetric_key: bytes) -> None:
    """
    Дешифрует файл алгоритмом AES-CBC.
    """
    encrypted_data = read_binary_file(input_file_path)

    iv =  encrypted_data[:16]
    ciphertext = encrypted_data[16:]
    cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(iv))

    decryptor = cipher.decryptor()
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = symmetric_padding.ANSIX923(128).unpadder()
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    write_binary_file(output_file_path, plaintext)