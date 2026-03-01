"""Скрипт шифрования для первой части лабораторной работы."""

import argparse
from caesar_cipher import encrypt
from file_utils import read_text, write_text


def main() -> None:
    """
    Зашифровать текст из файла и сохранить результат.

    Аргументы командной строки:
        input  — файл с исходным текстом
        key    — файл с ключом (число сдвига)
        output — файл для сохранения шифротекста
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("key")
    parser.add_argument("output")

    args = parser.parse_args()

    text = read_text(args.input).upper()
    shift = int(read_text(args.key).strip())

    encrypted_text = encrypt(text, shift)
    write_text(args.output, encrypted_text)


if __name__ == "__main__":
    main()
