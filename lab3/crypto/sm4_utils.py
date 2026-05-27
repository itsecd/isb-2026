import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding


def generate_sm4_key():
    """
    Генерирует 128-битный ключ SM4.

    Returns:
        bytes: Ключ SM4.

    Raises:
        RuntimeError: Если генерация ключа не удалась.
    """

    try:
        return os.urandom(16)

    except Exception as err:
        raise RuntimeError(f"Ошибка генерации SM4 ключа: {err}")


def sm4_encrypt(key, text):
    """
    Шифрует текст алгоритмом SM4 в режиме CBC.

    Args:
        key (bytes): Ключ SM4.
        text (str): Исходный текст.

    Returns:
        bytes: IV + зашифрованные данные.

    Raises:
        ValueError: Если шифрование не удалось.
    """

    try:
        iv = os.urandom(16)

        padder = padding.PKCS7(128).padder()

        padded_data = (padder.update(text.encode('utf-8')) + padder.finalize())
        cipher = Cipher(algorithms.SM4(key), modes.CBC(iv))
        encryptor = cipher.encryptor()
        encrypted_data = (encryptor.update(padded_data) + encryptor.finalize())
        return iv + encrypted_data

    except Exception as err:
        raise ValueError(f"Ошибка SM4 шифрования: {err}")


def sm4_decrypt(key, encrypted_data):
    """
    Расшифровывает данные алгоритмом SM4.

    Args:
        key (bytes): Ключ SM4.
        encrypted_data (bytes): IV + шифртекст.

    Returns:
        str: Расшифрованный текст.

    Raises:
        ValueError: Если дешифрование не удалось.
    """

    try:
        iv = encrypted_data[:16]
        ciphertext = encrypted_data[16:]

        cipher = Cipher(algorithms.SM4(key),modes.CBC(iv))
        decryptor = cipher.decryptor()
        decrypted_padded = (decryptor.update(ciphertext) + decryptor.finalize())
        unpadder = padding.PKCS7(128).unpadder()
        decrypted_data = (unpadder.update(decrypted_padded) + unpadder.finalize())

        return decrypted_data.decode('utf-8')

    except Exception as err:
        raise ValueError(f"Ошибка SM4 дешифрования: {err}")