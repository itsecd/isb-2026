import os

from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes


BLOWFISH_BLOCK_BITS = 64
BLOWFISH_BLOCK_BYTES = BLOWFISH_BLOCK_BITS // 8


def generate_sym_key(key_length: int = 128) -> bytes:
    """
    Генерирует случайный симметричный ключ Blowfish.

    :param key_length: длина ключа в битах (32–448, кратно 8)
    :return: сгенерированный симметричный ключ
    """

    if not (32 <= key_length <= 448 and key_length % 8 == 0):
        raise ValueError(
            f"Длина ключа Blowfish должна быть от 32 до 448 бит "
            f"и кратна 8, получено {key_length}"
        )

    return os.urandom(key_length // 8)


def encrypt_sym(data: bytes, key: bytes) -> tuple[bytes, bytes]:
    """
    Шифрует данные алгоритмом Blowfish в режиме CBC.

    :param data: данные для шифрования
    :param key: симметричный ключ Blowfish
    :return: кортеж (вектор инициализации, шифротекст)
    """

    try:
        padder = padding.PKCS7(BLOWFISH_BLOCK_BITS).padder()
        padded_data = padder.update(data) + padder.finalize()

        iv = os.urandom(BLOWFISH_BLOCK_BYTES)
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        c_text = encryptor.update(padded_data) + encryptor.finalize()

        return iv, c_text
    except Exception as err:
        raise RuntimeError(
            f"Ошибка при шифровании файла: {err}"
        ) from err


def decrypt_sym(iv: bytes, c_text: bytes, key: bytes) -> bytes:
    """
    Расшифровывает данные алгоритмом Blowfish в режиме CBC.

    :param iv: вектор инициализации
    :param c_text: зашифрованные данные
    :param key: симметричный ключ Blowfish
    :return: расшифрованные данные
    """

    try:
        cipher = Cipher(algorithms.Blowfish(key), modes.CBC(iv))
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(c_text) + decryptor.finalize()

        unpadder = padding.PKCS7(BLOWFISH_BLOCK_BITS).unpadder()
        dc_text = unpadder.update(padded_data) + unpadder.finalize()

        return dc_text
    except Exception as err:
        raise RuntimeError(
            f"Ошибка при расшифровке файла: {err}"
        ) from err