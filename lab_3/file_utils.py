import os
import json
from typing import List, Tuple, Dict, Any

_config: Dict[str, Any] = {}


def load_config(config_path: str = "constants.json") -> None:
    """
    Загружает конфигурацию из JSON файла.

    Args:
        config_path: Путь к JSON файлу конфигурации.
    """
    global _config
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Файл конфигурации не найден: {config_path}")
    
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            _config = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка парсинга JSON в файле {config_path}: {e}")


def get_config() -> Dict[str, Any]:
    """Возвращает загруженную конфигурацию."""
    if not _config:
        load_config()
    return _config


def get_rsa_private_file() -> str:
    """Возвращает путь к файлу закрытого ключа RSA."""
    return get_config()["RSA_PRIVATE_FILE"]


def get_rsa_public_file() -> str:
    """Возвращает путь к файлу открытого ключа RSA."""
    return get_config()["RSA_PUBLIC_FILE"]


def get_cast5_key_file() -> str:
    """Возвращает путь к файлу ключа CAST-5."""
    return get_config()["CAST5_KEY_FILE"]


def get_encrypted_cast5_key_file() -> str:
    """Возвращает путь к файлу зашифрованного ключа CAST-5."""
    return get_config()["ENCRYPTED_CAST5_KEY_FILE"]


def get_key_files() -> List[str]:
    """Возвращает список всех файлов ключей."""
    return get_config()["KEY_FILES"]


def get_cast5_min_key_len() -> int:
    """Возвращает минимальную длину ключа CAST-5."""
    return get_config()["CAST5_MIN_KEY_LEN"]


def get_cast5_max_key_len() -> int:
    """Возвращает максимальную длину ключа CAST-5."""
    return get_config()["CAST5_MAX_KEY_LEN"]


def get_cast5_key_step() -> int:
    """Возвращает шаг изменения длины ключа CAST-5."""
    return get_config()["CAST5_KEY_STEP"]


def get_cast5_default_key_len() -> int:
    """Возвращает длину ключа CAST-5 по умолчанию."""
    return get_config()["CAST5_DEFAULT_KEY_LEN"]


def get_rsa_key_size() -> int:
    """Возвращает размер RSA ключа."""
    return get_config()["RSA_KEY_SIZE"]


def save_bytes(data: bytes, file_path: str) -> None:
    """
    Сохраняет байтовые данные в файл.

    Args:
        data: Байтовые данные для сохранения.
        file_path: Путь для сохранения файла.

    Raises:
        ValueError: Если нет данных для сохранения.
        IOError: Если не удалось создать директорию или записать файл.
    """
    if not data:
        raise ValueError("Нет данных для сохранения")

    try:
        os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    except OSError as e:
        raise IOError(f"Не удалось создать директорию для {file_path}: {e}")

    try:
        with open(file_path, 'wb') as f:
            f.write(data)
    except OSError as e:
        raise IOError(f"Не удалось записать файл {file_path}: {e}")


def load_bytes(file_path: str) -> bytes:
    """
    Загружает байтовые данные из файла.

    Args:
        file_path: Путь к файлу.

    Returns:
        bytes: Содержимое файла.

    Raises:
        FileNotFoundError: Если файл не найден.
        IOError: Если не удалось прочитать файл.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    try:
        with open(file_path, 'rb') as f:
            return f.read()
    except OSError as e:
        raise IOError(f"Не удалось прочитать файл {file_path}: {e}")


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
    try:
        return os.path.getsize(file_path)
    except OSError:
        return 0


def check_keys_exist() -> Tuple[bool, List[str]]:
    """
    Проверяет наличие всех файлов ключей.

    Returns:
        Tuple[bool, List[str]]: (все_ли_ключи_есть, список_отсутствующих)
    """
    key_files = get_key_files()
    missing = [f for f in key_files if not file_exists(f)]
    return len(missing) == 0, missing


def validate_key_length(length_bits: int) -> None:
    """
    Проверяет допустимость длины ключа CAST-5.

    Args:
        length_bits: Длина ключа в битах.

    Raises:
        TypeError: Если длина ключа не целое число.
        ValueError: Если длина ключа вне допустимого диапазона.
    """
    min_len = get_cast5_min_key_len()
    max_len = get_cast5_max_key_len()
    step = get_cast5_key_step()

    if not isinstance(length_bits, int):
        raise TypeError("Длина ключа должна быть целым числом")
    if length_bits < min_len or length_bits > max_len or length_bits % step != 0:
        raise ValueError(f"Длина ключа {length_bits} бит не подходит. "
                         f"Нужно {min_len}-{max_len}, кратно {step}")