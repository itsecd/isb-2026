import hashlib
import os
import secrets
import string
from typing import Tuple
from tqdm import tqdm


def calculate_file_hash(file_path: str, block_size: int = 65536) -> str:
    """
    Вычисляет SHA-256 хеш файла по блокам для оптимизации памяти.

    Args:
        file_path (str): Полный путь к хешируемому файлу.
        block_size (int, optional): Размер считываемого блока в байтах. По умолчанию 65536.

    Returns:
        str: Строка шестнадцатеричного хеша (длиной 64 символа).

    Raises:
        FileNotFoundError: Если указанный файл не существует.
        OSError: При ошибках доступа или чтения файла.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    sha256 = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for block in iter(lambda: f.read(block_size), b""):
                sha256.update(block)
        return sha256.hexdigest()
    except OSError as e:
        print(f"Ошибка при чтении файла для расчета хеша: {e}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def save_hash_to_file(hash_value: str, output_path: str) -> None:
    """
    Сохраняет вычисленную контрольную сумму (хеш) в текстовый файл.

    Args:
        hash_value (str): Строка хеша для сохранения.
        output_path (str): Путь к файлу, в который будет записан хеш.

    Raises:
        OSError: Если не удалось создать директорию или записать данные в файл.
    """
    folder = os.path.dirname(output_path)
    if folder:
        try:
            os.makedirs(folder, exist_ok=True)
        except OSError as e:
            print(f"Ошибка при создании директории для хеша: {e}")
            raise

    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(hash_value)
    except OSError as e:
        print(f"Ошибка при записи файла хеша: {e}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def load_hash_from_file(hash_path: str) -> str:
    """
    Загружает ранее сохраненный хеш из файла.

    Args:
        hash_path (str): Путь к файлу, содержащему контрольную сумму.

    Returns:
        str: Очищенная от пробельных символов строка хеша.

    Raises:
        FileNotFoundError: Если файл с хешем отсутствует.
        OSError: Ошибка при открытии или чтении файла.
    """
    if not os.path.exists(hash_path):
        raise FileNotFoundError(f"Файл с хешем не найден: {hash_path}")

    try:
        with open(hash_path, "r", encoding="utf-8") as f:
            return f.read().strip()
    except OSError as e:
        print(f"Ошибка при чтении файла хеша: {e}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def verify_file_integrity(file_path: str, hash_path: str) -> Tuple[bool, str, str]:
    """
    Выполняет проверку целостности файла путем сравнения текущего и эталонного хешей.

    Args:
        file_path (str): Путь к проверяемому файлу.
        hash_path (str): Путь к файлу с эталонным хешем.

    Returns:
        Tuple[bool, str, str]: Кортеж, содержащий:
            - bool: True, если хеши совпали, иначе False.
            - str: Текущий вычисленный хеш.
            - str: Ожидаемый (загруженный) хеш.

    Raises:
        FileNotFoundError: Если один из файлов не найден.
        OSError: Ошибка ввода-вывода при обработке файлов.
    """
    try:
        current_hash = calculate_file_hash(file_path)
        expected_hash = load_hash_from_file(hash_path)
        return current_hash == expected_hash, current_hash, expected_hash
    except OSError as e:
        print(f"Ошибка при верификации целостности: {e}")
        raise
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        raise


def simulate_collision_search(target_prefix_len: int = 4) -> Tuple[str, str, int]:
    """
    Проводит симуляцию и визуализацию поиска частичной коллизии для первых N символов SHA-256.

    Args:
        target_prefix_len (int, optional): Длина совпадающего префикса (от 1 до 8). По умолчанию 4.

    Returns:
        Tuple[str, str, int]: Кортеж с результатами:
            - str: Базовая случайно сгенерированная строка.
            - str: Строка-кандидат, вызвавшая частичную коллизию.
            - int: Общее количество затраченных попыток (итераций).

    Raises:
        ValueError: Если длина префикса выходит за допустимые границы [1, 8].
    """
    if target_prefix_len < 1 or target_prefix_len > 8:
        raise ValueError(
            "Длина префикса для симуляции должна быть в диапазоне от 1 до 8.")

    try:
        alphabet = string.ascii_letters + string.digits
        base_str = "".join(secrets.choice(alphabet) for _ in range(10))
        target_hash = hashlib.sha256(base_str.encode()).hexdigest()
        target_prefix = target_hash[:target_prefix_len]

        attempts = 0
        max_estimated = 16 ** target_prefix_len

        with tqdm(total=max_estimated, desc="Collision Detection", unit="hashes") as pbar:
            while True:
                attempts += 1
                candidate = "".join(secrets.choice(alphabet)
                                    for _ in range(12))
                if candidate == base_str:
                    continue

                cand_hash = hashlib.sha256(candidate.encode()).hexdigest()

                if cand_hash[:target_prefix_len] == target_prefix:
                    pbar.update(1)
                    return base_str, candidate, attempts

                if attempts % 1000 == 0:
                    pbar.update(1000 if attempts <= max_estimated else 0)
    except Exception as err:
        print(
            f"Unexpected error during collision search: {err=}, {type(err)=}")
        raise
