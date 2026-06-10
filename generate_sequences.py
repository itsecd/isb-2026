"""Генерация трёх бинарных последовательностей разными ГПСЧ с обработкой ошибок."""

import random
import secrets
import os
import sys

from constants import SEQUENCE_LENGTH, SEQUENCES_DIR, SEQUENCE_FILES


def safe_write_sequence(filepath: str, generator_func) -> bool:
    """
    Записывает битовую последовательность в файл с обработкой исключений.

    Parameters
    ----------
    filepath : str
        Полный путь к файлу для записи.
    generator_func : callable
        Функция, которая при каждом вызове возвращает '0' или '1'.

    Returns
    -------
    bool
        True, если запись успешна, иначе False.
    """
    try:
        with open(filepath, 'w') as f:
            for _ in range(SEQUENCE_LENGTH):
                f.write(generator_func())
        return True
    except IOError as e:
        print(f"Ошибка записи в файл {filepath}: {e}", file=sys.stderr)
        return False


def main() -> None:
    """Генерирует три последовательности разными ГПСЧ."""
    try:
        os.makedirs(SEQUENCES_DIR, exist_ok=True)
    except OSError as e:
        print(f"Ошибка создания директории {SEQUENCES_DIR}: {e}", file=sys.stderr)
        sys.exit(1)

    def c_generator():
        return str(random.getrandbits(1))

    rng = random.Random()

    def cpp_generator():
        return str(rng.getrandbits(1))

    def py_generator():
        return str(secrets.randbits(1))

    success_c = safe_write_sequence(
        os.path.join(SEQUENCES_DIR, SEQUENCE_FILES["C (rand)"]),
        c_generator
    )
    success_cpp = safe_write_sequence(
        os.path.join(SEQUENCES_DIR, SEQUENCE_FILES["C++ (mt19937)"]),
        cpp_generator
    )
    success_py = safe_write_sequence(
        os.path.join(SEQUENCES_DIR, SEQUENCE_FILES["Python (secrets)"]),
        py_generator
    )

    if success_c and success_cpp and success_py:
        print("Все три последовательности успешно сгенерированы.")
    else:
        print("Некоторые последовательности не были созданы из-за ошибок.", file=sys.stderr)


if __name__ == "__main__":
    main()
