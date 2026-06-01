import os
import hashlib
from load_and_save_hash import load_hash


def calculating_hash(file_path: str) -> str:
    """
    Вычисляет хэш-сумму SHA-256 для указанного файла .
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    block_size = 65536
    m = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            blok = f.read(block_size)
            while blok:
                m.update(blok)
                blok = f.read(block_size)
    except PermissionError:
        raise PermissionError(f"Нет прав на чтение файла: {file_path}")
    except OSError as e:
        raise RuntimeError(f"Ошибка ввода-вывода при чтении файла: {e}")
    return m.hexdigest()


def integrity_check(file_path: str, hash_file_path: str) -> bool:
    """
    Проверяет целостность файла, сравнивая его текущий хэш с эталонным из файла хэша.
    """
    save_sum = load_hash(hash_file_path)
    new_sum = calculating_hash(file_path)
    if save_sum == new_sum:
        return True
    else:
        print("ЦЕЛОСТНОСТЬ НАРУШЕНА, Файл был изменён.")
        print(f"   Ожидается: {save_sum}")
        print(f"   Получено:  {new_sum}")
        return False


def collision_demo(
    attempts: int = 50000, prefix_len: int = 4, progress_callback=None
) -> dict:
    """
    Ищет частичную коллизию SHA-256 методом перебора числовых строк.
    """
    seen = {}

    for i in range(attempts):
        if progress_callback and i % 500 == 0:
            progress_callback(i)

        text = str(i)
        h = hashlib.sha256(text.encode()).hexdigest()
        prefix = h[:prefix_len]

        if prefix in seen:
            return {
                "attempts": i + 1,
                "first": seen[prefix],
                "second": text,
            }

        seen[prefix] = text

    return {"attempts": attempts, "first": None, "second": None}
