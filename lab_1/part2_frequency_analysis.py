"""Скрипт выполнения частотного анализа (вторая часть лабораторной)."""

import argparse
from frequency import calculate_frequencies, save_frequencies
from file_utils import read_text


def main() -> None:
    """
    Выполнить частотный анализ зашифрованного текста
    и сохранить частоты в отдельный файл.

    Аргументы командной строки:
        input        — файл с зашифрованным текстом
        freq_output  — файл для сохранения частот
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("freq_output")

    args = parser.parse_args()

    text = read_text(args.input)

    frequencies = calculate_frequencies(text)
    save_frequencies(frequencies, args.freq_output)


if __name__ == "__main__":
    main()
