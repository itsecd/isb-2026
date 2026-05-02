import argparse
import json

from decryption import decrypt
from encryption import encrypt
from generate import generate_key

def parser_t() -> argparse.Namespace:
    """Функция для парсера командной строки"""
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", help="Запускает режим генерации ключей")
    group.add_argument("-enc", "--encryption", help="Запускает режим шифрования")
    group.add_argument("-dec", "--decryption", help="Запускает режим дешифрования")

    return parser.parse_args()


def main() -> None:
    args = parser_t()

    with open("settings.json") as f:
        settings = json.load(f)

    match args:
        case _ if args.generation is not None:
            generate_key(
                settings["symmetric_key"],
                settings["public_key"],
                settings["secret_key"],
            )
        case _ if args.encryption is not None:
            encrypt(
                settings["initial_file"],
                settings["secret_key"],
                settings["symmetric_key"],
                settings["encrypted_file"],
            )
        case _:
            decrypt(
                settings["encrypted_file"],
                settings["secret_key"],
                settings["symmetric_key"],
                settings["decrypted_file"],
            )


if __name__ == "__main__":
    main()
