"""Скрипт расшифрования для проверки корректности алгоритма."""

import argparse
from caesar_cipher import decrypt
from file_utils import read_text, write_text


def main() -> None:
    """
    Расшифровать текст из файла и сохранить результат.

    Аргументы командной строки:
        input  — файл с зашифрованным текстом
        key    — файл с ключом (число сдвига)
        output — файл для сохранения расшифрованного текста
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("key")
    parser.add_argument("output")

    args = parser.parse_args()

    text = read_text(args.input)
    shift = int(read_text(args.key).strip())

    decrypted_text = decrypt(text, shift)
    write_text(args.output, decrypted_text)


if __name__ == "__main__":
    main()
