import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
import file_io

KEY_SIZE   = 32   # 256 бит
NONCE_SIZE = 16   # 128 бит


def generate_sym_key() -> bytes:
    """
    Генерация симметричного ключа для ChaCha20.

    Returns:
        bytes: Случайный ключ длиной KEY_SIZE байт (256 бит).

    Raises:
        RuntimeError: Ошибка при генерации ключа.
    """
    try:
        return os.urandom(KEY_SIZE)
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации ключа: {e}")


def generate_nonce() -> bytes:
    """
    Генерация одноразового случайного числа (nonce).

    Returns:
        bytes: Случайный nonce длиной NONCE_SIZE байт (128 бит).

    Raises:
        RuntimeError: Ошибка при генерации nonce.
    """
    try:
        return os.urandom(NONCE_SIZE)
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации nonce: {e}")


def save_encrypted_sym_key(blob: bytes, path: str) -> None:
    """
    Сохранение зашифрованного симметричного ключа в файл.

    Args:
        blob: Зашифрованный симметричный ключ.
        path: Путь для сохранения.

    Raises:
        RuntimeError: Ошибка при сохранении.
    """
    file_io.write_file(path, blob)


def load_encrypted_sym_key(path: str) -> bytes:
    """
    Загрузка зашифрованного симметричного ключа из файла.

    Args:
        path: Путь к файлу с зашифрованным ключом.

    Returns:
        bytes: Загруженные данные в байтовом формате.

    Raises:
        FileNotFoundError: Файл не найден.
        RuntimeError: Ошибка при загрузке ключа.
    """
    return file_io.read_file(path)


def save_nonce(nonce: bytes, path: str) -> None:
    """
    Сохранение nonce в файл.

    Args:
        nonce: Nonce для сохранения.
        path: Путь для сохранения.

    Raises:
        RuntimeError: Ошибка при сохранении.
    """
    file_io.write_file(path, nonce)


def load_nonce(path: str) -> bytes:
    """
    Загрузка nonce из файла.

    Args:
        path: Путь к файлу с nonce.

    Returns:
        bytes: Загруженный nonce.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Некорректный размер nonce.
        RuntimeError: Ошибка при загрузке nonce.
    """
    data = file_io.read_file(path)
    if len(data) != NONCE_SIZE:
        raise ValueError(f"Nonce должен быть {NONCE_SIZE} байт, получено {len(data)}")
    return data


def chacha20_crypt(data: bytes, key: bytes, nonce: bytes) -> bytes:
    """
    Шифрование или дешифрование данных с помощью ChaCha20.
    В ChaCha20 операции шифрования и дешифрования идентичны.

    Args:
        data: Данные для обработки.
        key: Симметричный ключ.
        nonce: Одноразовое случайное число.

    Returns:
        bytes: Обработанные данные (шифротекст или открытый текст).

    Raises:
        RuntimeError: Ошибка при выполнении шифрования/дешифрования.
    """
    try:
        cipher = Cipher(algorithms.ChaCha20(key, nonce), mode=None)
        encryptor = cipher.encryptor()
        return encryptor.update(data) + encryptor.finalize()
    except Exception as e:
        raise RuntimeError(f"Ошибка при шифровании/дешифровании ChaCha20: {e}")
