import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms
import file_io


def generate_random_bytes(size: int) -> bytes:
    """
    Генерация случайных байт заданной длины.

    Args:
        size: Количество байт.

    Returns:
        bytes: Случайные байты длиной size.

    Raises:
        ValueError: Недопустимый размер.
        RuntimeError: Ошибка при генерации.
    """
    if size <= 0:
        raise ValueError(f"Размер должен быть положительным, получено: {size}")
    try:
        return os.urandom(size)
    except Exception as e:
        raise RuntimeError(f"Ошибка при генерации случайных байт: {e}")


def load_nonce(path: str, nonce_size: int) -> bytes:
    """
    Загрузка nonce из файла.

    Args:
        path: Путь к файлу с nonce.
        nonce_size: Ожидаемый размер nonce в байтах.

    Returns:
        bytes: Загруженный nonce.

    Raises:
        FileNotFoundError: Файл не найден.
        ValueError: Некорректный размер nonce.
        RuntimeError: Ошибка при загрузке nonce.
    """
    data = file_io.read_file(path)
    if len(data) != nonce_size:
        raise ValueError(f"Nonce должен быть {nonce_size} байт, получено {len(data)}")
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
