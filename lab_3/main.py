import argparse
import json

from decryption import decrypt
from encryption import encrypt
from generate import generate_key


def parser_t() -> argparse.Namespace:
    """Функция для парсера командной строки"""
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

    parser.add_argument("--input", help="Путь к исходному файлу")
    parser.add_argument("--output", help="Путь к выходному файлу")
    parser.add_argument("--key", help="Путь к симметричному ключу")
    parser.add_argument("--public", help="Путь к открытому RSA ключу")
    parser.add_argument("--private", help="Путь к закрытому RSA ключу")

    return parser.parse_args()


def main() -> None:
    args = parser_t()

    with open("settings.json") as f:
        settings = json.load(f)

    key = args.key or settings["symmetric_key"]
    public = args.public or settings["public_key"]
    private = args.private or settings["secret_key"]
    input_ = args.input or settings["initial_file"]

    match args:
        case _ if args.generation:
            generate_key(key, public, private)
        case _ if args.encryption:
            encrypt(input_, private, key, args.output or settings["encrypted_file"])
        case _:
            decrypt(
                args.input or settings["encrypted_file"],
                private,
                key,
                args.output or settings["decrypted_file"],
            )


if __name__ == "__main__":
    main()
