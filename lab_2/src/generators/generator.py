#!/usr/bin/env python3
# lab_2/src/generators/generator.py
"""
Генератор псевдослучайных бинарных последовательностей на Python
Использует стандартный модуль random
"""

import argparse
import random
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки"""
    parser = argparse.ArgumentParser(
        description="Генерация 128-битной псевдослучайной последовательности"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="../../data/sequences/python_sequence.txt",
        help="Путь к файлу для сохранения"
    )
    parser.add_argument(
        "-l", "--length",
        type=int,
        default=128,
        help="Длина последовательности (по умолчанию: 128)"
    )
    return parser.parse_args()


def generate_binary_sequence(length: int) -> str:
    """
    Генерирует бинарную последовательность
    
    :param length: количество бит
    :return: строка из '0' и '1'
    """
    return ''.join(str(random.randint(0, 1)) for _ in range(length))


def save_sequence(sequence: str, filepath: str) -> bool:
    """
    Сохраняет последовательность в файл с созданием папок
    
    :param sequence: бинарная строка
    :param filepath: путь к файлу (относительный или абсолютный)
    :return: True если успешно
    """
    try:
        # ✅ Создаём папки автоматически
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(sequence)
        return True
    except IOError as e:
        print(f"[Python] Error: {e}", file=sys.stderr)
        return False


def main() -> int:
    """Точка входа"""
    args = parse_args()
    
    sequence = generate_binary_sequence(args.length)
    
    if save_sequence(sequence, args.output):
        print(f"[Python] Generated {len(sequence)} bits")
        print(f"[Python] Saved: {args.output}")
        print(f"[Python] Sequence: {sequence}")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())