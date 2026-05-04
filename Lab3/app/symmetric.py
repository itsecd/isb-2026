import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

from app.file_utils import write_bytes, read_bytes


# генерация ключа CAST5
def generate_cast5_key(key_size_bits: int) -> bytes:
    if key_size_bits < 40 or key_size_bits > 128 or key_size_bits % 8 != 0:
        raise ValueError("Неверная длина ключа CAST5")

    return os.urandom(key_size_bits // 8)



# Padding / Unpadding
def pad_data(data: bytes, block_size: int = 64) -> bytes:
    padder = padding.ANSIX923(block_size).padder()
    return padder.update(data) + padder.finalize()


def unpad_data(data: bytes, block_size: int = 64) -> bytes:
    unpadder = padding.ANSIX923(block_size).unpadder()
    return unpadder.update(data) + unpadder.finalize()


# шифрование файла
def encrypt_file(input_path: str, output_path: str, key: bytes):
    data = read_bytes(input_path)

    padded_data = pad_data(data)

    iv = os.urandom(8)

    cipher = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv)
    )

    encryptor = cipher.encryptor()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    write_bytes(output_path, iv + encrypted)


# дешифрование файла
def decrypt_file(input_path: str, output_path: str, key: bytes):
    data = read_bytes(input_path)

    iv = data[:8]
    encrypted = data[8:]

    cipher = Cipher(
        algorithms.CAST5(key),
        modes.CBC(iv)
    )

    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()

    unpadded = unpad_data(decrypted)

    write_bytes(output_path, unpadded)