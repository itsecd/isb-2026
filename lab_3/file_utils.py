import os
from typing import List, Tuple
from constants import CAST5_MIN_KEY_LEN, CAST5_MAX_KEY_LEN, CAST5_KEY_STEP


def save_bytes(data: bytes, file_path: str) -> None:
    """
    Сохраняет байтовые данные в файл.

    Args:
        data: Байтовые данные для сохранения.
        file_path: Путь для сохранения файла.
    """
    if not data:
        raise ValueError("Нет данных для сохранения")

    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)

    with open(file_path, 'wb') as f:
        f.write(data)


def load_bytes(file_path: str) -> bytes:
    """
    Загружает байтовые данные из файла.

    Args:
        file_path: Путь к файлу.

    Returns:
        bytes: Содержимое файла.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    with open(file_path, 'rb') as f:
        return f.read()


def file_exists(file_path: str) -> bool:
    """
    Проверяет существование файла.

    Args:
        file_path: Путь к файлу.

    Returns:
        bool: True если файл существует.
    """
    return os.path.exists(file_path)


def get_file_size(file_path: str) -> int:
    """
    Возвращает размер файла в байтах.

    Args:
        file_path: Путь к файлу.

    Returns:
        int: Размер файла в байтах (0 если файл не существует).
    """
    if not os.path.exists(file_path):
        return 0
    return os.path.getsize(file_path)


def check_keys_exist(key_files: List[str]) -> Tuple[bool, List[str]]:
    """
    Проверяет наличие всех файлов ключей.

    Args:
        key_files: Список путей к файлам ключей.

    Returns:
        Tuple[bool, List[str]]: (все_ли_ключи_есть, список_отсутствующих)
    """
    missing = [f for f in key_files if not file_exists(f)]
    return len(missing) == 0, missing


def validate_key_length(length_bits: int) -> None:
    """
    Проверяет допустимость длины ключа CAST-5.

    Args:
        length_bits: Длина ключа в битах.
    """
    if not isinstance(length_bits, int):
        raise TypeError("Длина ключа должна быть целым числом")
    if length_bits < CAST5_MIN_KEY_LEN or length_bits > CAST5_MAX_KEY_LEN or length_bits % CAST5_KEY_STEP != 0:
        raise ValueError(f"Длина ключа {length_bits} бит не подходит. "
                         f"Нужно {CAST5_MIN_KEY_LEN}-{CAST5_MAX_KEY_LEN}, кратно {CAST5_KEY_STEP}")