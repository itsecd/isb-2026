import argparse
import random
import sys
import json
import os

from analysis_utils import count_bit_diff, diff_percent
from hash_utils import compute_hash
from mutation_utils import apply_mutation


def load_algorithms():
    """
    Загрузка доступных алгоритмов хеширования из settings.json.

    Returns:
        dict: Словарь
    """
    if not os.path.exists("settings.json"):
        raise FileNotFoundError("settings.json не найден")

    try:
        with open("settings.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("algorithms", {})
    except Exception as e:
        raise RuntimeError(f"Ошибка чтения settings.json: {e}")


def parse_args():
    """
    Парсинг и валидация аргументов командной строки.

    Returns:
        Объект argparse.Namespace с аргументами командной строки.
    """
    parser = argparse.ArgumentParser(description="Исследование лавинного эффекта хеш-функций.")
    parser.add_argument("-s", "--string", type=str, required=True, help="Исходная строка")
    parser.add_argument("-a", "--algo", type=str, required=True, help="Алгоритм хеширования")
    parser.add_argument("-c", "--count", type=int, default=10, help="Количество экспериментов")

    args = parser.parse_args()

    if args.count < 10:
        parser.error("Количество экспериментов должно быть не менее 10.")

    return args


def main():
    args = parse_args()

    try:
        algorithms = load_algorithms()

        if args.algo not in algorithms and args.algo not in algorithms.values():
            raise ValueError(f"Алгоритм '{args.algo}' не найден в settings.json")

        algo = algorithms.get(args.algo, args.algo)

        print(f"Старт исследования лавинного эффекта.")
        print(f"Входные данные: '{args.string}', Алгоритм: {algo}, Тестов: {args.count}")

        orig_hash = compute_hash(args.string, algo)
        total_bits = len(orig_hash) * 4

        print(f"Исходный хэш: {orig_hash}\n")
        print(f"#\tОперация\tИзменено бит\tПроцент различий\tНовый хэш")

        for i in range(1, args.count + 1):
            mode = random.choice(["char", "bit", "reg"])

            new_bytes, op = apply_mutation(args.string, mode)

            new_hash = compute_hash(new_bytes, algo)
            diff = count_bit_diff(orig_hash, new_hash)
            percent = diff_percent(diff, total_bits)

            print(f"{i}\t{op}\t\t{diff}\t\t{percent:.2f}%\t\t {new_hash}")

        print("\nТестирование завершено.")

    except Exception as e:
        print(f"Ошибка: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
