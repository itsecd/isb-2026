"""Запуск NIST-тестов с полной обработкой исключений и сохранением результатов."""

import csv
import os
import sys
from typing import Dict, List, Tuple

from nist_tests import monobit_test, runs_test, longest_run_ones_in_block
from constants import (
    SEQUENCE_FILES, RESULTS_FILE, CSV_DELIMITER, CSV_FIELDS, ALPHA,
    get_sequence_path
)


def load_sequence(filepath: str) -> str:
    """
    Загружает бинарную последовательность из текстового файла.

    Parameters
    ----------
    filepath : str
        Путь к файлу.

    Returns
    -------
    str
        Содержимое файла (пустая строка при ошибке).
    """
    try:
        with open(filepath, 'r') as f:
            bits = f.read().strip()
        if not bits:
            print(f"Предупреждение: файл {filepath} пуст", file=sys.stderr)
        return bits
    except FileNotFoundError:
        print(f"Файл {filepath} не найден", file=sys.stderr)
        return ""
    except IOError as e:
        print(f"Ошибка чтения {filepath}: {e}", file=sys.stderr)
        return ""


def safe_run_tests(bits: str, name: str) -> Dict[str, float]:
    """
    Безопасно запускает три теста, перехватывая исключения.

    Parameters
    ----------
    bits : str
        Бинарная строка.
    name : str
        Имя генератора (для сообщений об ошибках).

    Returns
    -------
    Dict[str, float]
        Словарь с p-значениями или -1.0 при ошибке.
    """
    results = {}
    try:
        results['mono'] = monobit_test(bits)
    except Exception as e:
        print(f"Ошибка в monobit_test для {name}: {e}", file=sys.stderr)
        results['mono'] = -1.0

    try:
        results['runs'] = runs_test(bits)
    except Exception as e:
        print(f"Ошибка в runs_test для {name}: {e}", file=sys.stderr)
        results['runs'] = -1.0

    try:
        results['long'] = longest_run_ones_in_block(bits)
    except Exception as e:
        print(f"Ошибка в longest_run_ones_in_block для {name}: {e}", file=sys.stderr)
        results['long'] = -1.0

    return results


def main() -> None:
    """Главная функция: тестирует все доступные последовательности и записывает CSV."""
    sequences: List[Tuple[str, str]] = [
        (name, get_sequence_path(name)) for name in SEQUENCE_FILES
    ]
    results: List[Dict[str, str]] = []

    for name, path in sequences:
        bits = load_sequence(path)
        if not bits:
            print(f"Пропускаем {name} из-за ошибки чтения", file=sys.stderr)
            continue

        n = len(bits)
        print(f"Тестируем {name}, длина = {n} бит...")
        p_values = safe_run_tests(bits, name)

        p_mono = p_values['mono']
        p_runs = p_values['runs']
        p_long = p_values['long']

        passed = (
            p_mono != -1.0 and p_runs != -1.0 and
            p_mono >= ALPHA and p_runs >= ALPHA and
            (p_long == -1.0 or p_long >= ALPHA)
        )
        result_text = "пройден" if passed else "НЕ ПРОЙДЕН (ошибка или p<0.01)"

        results.append({
            "Генератор": name,
            "Длина (бит)": str(n),
            "Частотный тест (p-value)": f"{p_mono:.6f}" if p_mono != -1.0 else "ошибка",
            "Тест прогонов (p-value)": f"{p_runs:.6f}" if p_runs != -1.0 else "ошибка",
            "Тест на длинную серию (p-value)": (
                f"{p_long:.6f}" if p_long != -1.0 else "недостаточно данных или ошибка"
            ),
            "Результат": result_text
        })

    try:
        with open(RESULTS_FILE, "w", newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(
                csvfile, fieldnames=CSV_FIELDS, delimiter=CSV_DELIMITER
            )
            writer.writeheader()
            for row in results:
                writer.writerow(row)
        print(f"\nРезультаты сохранены в {RESULTS_FILE}")
    except IOError as e:
        print(f"Не удалось записать {RESULTS_FILE}: {e}", file=sys.stderr)
        sys.exit(1)

    for r in results:
        print(f"{r['Генератор']}: {r['Результат']}")


if __name__ == "__main__":
    main()