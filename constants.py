"""Константы для генерации и тестирования последовательностей."""

import os

SEQUENCE_LENGTH = 1_000_000

SEQUENCES_DIR = "generators/sequences"

SEQUENCE_FILES = {
    "C (rand)": "sequence_c.txt",
    "C++ (mt19937)": "sequence_cpp.txt",
    "Python (secrets)": "sequence_python.txt"
}

RESULTS_FILE = "results.csv"
CSV_DELIMITER = ";"
CSV_FIELDS = [
    "Генератор",
    "Длина (бит)",
    "Частотный тест (p-value)",
    "Тест прогонов (p-value)",
    "Тест на длинную серию (p-value)",
    "Результат"
]

ALPHA = 0.01


def get_sequence_path(generator_name: str) -> str:
    """Возвращает полный путь к файлу последовательности по имени генератора."""
    return os.path.join(SEQUENCES_DIR, SEQUENCE_FILES[generator_name])