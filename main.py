import argparse
import json
import sys
import os
from operations import run_generation, run_encryption, run_decryption


def parser() -> argparse.Namespace:
    """Парсер"""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen",
        "--generation",
        action="store_true",
        help="Запускает режим генерации ключей",
    )
    group.add_argument(
        "-enc", "--encryption", action="store_true", help="Запускает режим шифрования"
    )
    group.add_argument(
        "-dec", "--decryption", action="store_true", help="Запускает режим дешифрования"
    )
    parser.add_argument("-k", "--key-size", type=int, default=256)
    return parser.parse_args()


def load_setting() -> dict:
    """Загружает настройки из файла settings.json."""
    with open("settings.json") as json_file:
        json_data = json.load(json_file)
    return json_data


def main() -> None:
    """Точка входа в программу."""
    args = parser()
    settings = load_setting()

    match args:
        case _ if args.generation:
            run_generation(settings, args.key_size)
        case _ if args.encryption:
            run_encryption(settings)
        case _:
            run_decryption(settings)


if __name__ == "__main__":
    main()
