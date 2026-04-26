
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


IDEA_KEY_SIZE = 16        
IDEA_BLOCK_SIZE = 8       
IDEA_BLOCK_BITS = 64      


def generate_idea_key() -> bytes:
    """
    Генерирует случайный ключ IDEA (128 бит).

    """
    key = os.urandom(IDEA_KEY_SIZE)
    print(f"[OK] Ключ IDEA сгенерирован: {key.hex()[:32]}...")
    return key


def idea_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом IDEA (CBC).

    """
    padder = sym_padding.PKCS7(IDEA_BLOCK_BITS).padder()
    padded_data = padder.update(plaintext) + padder.finalize()

    iv = os.urandom(IDEA_BLOCK_SIZE)
    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    print(f"[OK] Данные зашифрованы IDEA (CBC), "
          f"размер: {len(ciphertext)} байт")
    return iv + ciphertext


def idea_decrypt(data: bytes, key: bytes) -> bytes:
    """
    Дешифрует данные алгоритмом IDEA (CBC).

    """
    iv = data[:IDEA_BLOCK_SIZE]
    ciphertext = data[IDEA_BLOCK_SIZE:]

    cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = sym_padding.PKCS7(IDEA_BLOCK_BITS).unpadder()
    plaintext = unpadder.update(padded_data) + unpadder.finalize()

    print(f"[OK] Данные расшифрованы IDEA (CBC), "
          f"размер: {len(plaintext)} байт")
    return plaintext