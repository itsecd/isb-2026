import os
import json
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from exceptions import KeyGenerationError, EncryptionError, DecryptionError, FileProcessingError

_SETTINGS_PATH = "settings.json"

def _load_cast5_constants():
    """
    Загружает константы для CAST5 из файла settings.json.

    :return: Словарь с параметрами алгоритма.
    :raises FileProcessingError: Если файл не найден или содержит некорректный JSON.
    """
    try:
        with open(_SETTINGS_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception as e:
        raise FileProcessingError(f"Не удалось загрузить {_SETTINGS_PATH}: {e}") from e

_constants = _load_cast5_constants()

CAST5_BLOCK_SIZE = _constants["cast5_block_size"]
CAST5_IV_SIZE = _constants["cast5_iv_size"]
CAST5_MIN_KEY_SIZE = _constants["cast5_min_key_size"]
CAST5_MAX_KEY_SIZE = _constants["cast5_max_key_size"]
CAST5_KEY_STEP = _constants["cast5_key_step"]


def generate_cast5_key(key_size_bits: int) -> bytes:
    """
    Генерирует случайный ключ для алгоритма CAST5.

    :param key_size_bits: Размер ключа в битах. Должен быть в диапазоне
                          [CAST5_MIN_KEY_SIZE, CAST5_MAX_KEY_SIZE] и кратен CAST5_KEY_STEP.
    :return: Ключ в виде байтовой строки.
    :raises KeyGenerationError: Если передан некорректный размер ключа или сбой генерации.
    """
    try:
        if not (CAST5_MIN_KEY_SIZE <= key_size_bits <= CAST5_MAX_KEY_SIZE
                and key_size_bits % CAST5_KEY_STEP == 0):
            raise ValueError("Некорректный размер ключа CAST5")
        return os.urandom(key_size_bits // 8)
    except Exception as error:
        raise KeyGenerationError(f"Ошибка генерации ключа: {error}") from error


def encrypt_file_cast5(input_path: str, output_path: str, key: bytes) -> None:
    """
    Шифрует файл с помощью CAST5 в режиме CBC с выравниванием PKCS7.
    В начало выходного файла записывается IV (размер CAST5_IV_SIZE), затем зашифрованные данные.

    :param input_path: Путь к исходному файлу (открытому тексту).
    :param output_path: Путь для сохранения зашифрованного файла.
    :param key: Ключ CAST5 (байты, длина должна соответствовать ожидаемой).
    :raises EncryptionError: Если ошибка чтения/записи файла, паддинга или шифрования.
    """
    try:
        with open(input_path, "rb") as f:
            data = f.read()

        padder = padding.PKCS7(CAST5_BLOCK_SIZE).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(CAST5_IV_SIZE)
        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        with open(output_path, "wb") as f:
            f.write(iv)
            f.write(encrypted_data)
    except Exception as error:
        raise EncryptionError(f"Ошибка шифрования файла: {error}") from error


def decrypt_file_cast5(input_path: str, output_path: str, key: bytes) -> None:
    """
    Расшифровывает файл, зашифрованный функцией encrypt_file_cast5.

    :param input_path: Путь к зашифрованному файлу (IV + шифротекст).
    :param output_path: Путь для сохранения расшифрованного файла.
    :param key: Ключ CAST5 (байты, тот же, что использовался для шифрования).
    :raises DecryptionError: Если ошибка чтения/записи файла, расшифрования или удаления паддинга.
    """
    try:
        with open(input_path, "rb") as f:
            content = f.read()

        iv = content[:CAST5_IV_SIZE]
        encrypted_data = content[CAST5_IV_SIZE:]

        cipher = Cipher(algorithms.CAST5(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = decryptor.update(encrypted_data) + decryptor.finalize()

        unpadder = padding.PKCS7(CAST5_BLOCK_SIZE).unpadder()
        decrypted_data = unpadder.update(decrypted_padded) + unpadder.finalize()

        with open(output_path, "wb") as f:
            f.write(decrypted_data)
    except Exception as error:
        raise DecryptionError(f"Ошибка дешифрования: {error}") from error