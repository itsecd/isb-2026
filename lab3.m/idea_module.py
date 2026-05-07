import json
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding as sym_padding


with open(os.path.join(os.path.dirname(__file__), "config.json"), "r") as f:
    _cfg = json.load(f)

IDEA_KEY_SIZE = _cfg["idea_key_size"]
IDEA_BLOCK_SIZE = _cfg["idea_block_size"]
IDEA_BLOCK_BITS = _cfg["idea_block_bits"]


def generate_idea_key() -> bytes:
    """
    Генерирует случайный ключ IDEA (128 бит).

    :return: ключ (16 байт)
    """
    key = os.urandom(IDEA_KEY_SIZE)
    print(f"[OK] Ключ IDEA сгенерирован: {key.hex()[:32]}...")
    return key


def idea_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """
    Шифрует данные алгоритмом IDEA (CBC).

    :param plaintext: исходные данные
    :param key: ключ IDEA (16 байт)
    :return: IV (8 байт) + шифротекст
    :raises Exception: если не удалось зашифровать
    """
    try:
        padder = sym_padding.PKCS7(IDEA_BLOCK_BITS).padder()
        padded_data = padder.update(plaintext) + padder.finalize()

        iv = os.urandom(IDEA_BLOCK_SIZE)
        cipher = Cipher(algorithms.IDEA(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()

        print(f"[OK] Данные зашифрованы IDEA (CBC), "
              f"размер: {len(ciphertext)} байт")
        return iv + ciphertext
    except Exception as e:
        print(f"[ОШИБКА] Не удалось зашифровать данные IDEA: {e}")
        raise


def idea_decrypt(data: bytes, key: bytes) -> bytes:
    """
    Дешифрует данные алгоритмом IDEA (CBC).

    :param data: IV (8 байт) + шифротекст
    :param key: ключ IDEA (16 байт)
    :return: расшифрованные данные
    :raises Exception: если не удалось расшифровать
    """
    try:
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
    except Exception as e:
        print(f"[ОШИБКА] Не удалось расшифровать данные IDEA: {e}")
        raise