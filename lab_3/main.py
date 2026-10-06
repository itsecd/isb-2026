import argparse

from decryption import decrypt
from encryption import encrypt
from file_handler import load_config
from generation import generate


def parse_arguments() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.

    :return: объект с распарсенными аргументами
    """

    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема RSA + Blowfish",
    )

    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument(
        "-gen", "--generation",
        action="store_true",
        help="Режим генерации ключей",
    )
    mode_group.add_argument(
        "-enc", "--encryption",
        action="store_true",
        help="Режим шифрования данных",
    )
    mode_group.add_argument(
        "-dec", "--decryption",
        action="store_true",
        help="Режим дешифрования данных",
    )

    parser.add_argument(
        "--input",
        type=str,
        help="Путь к исходному файлу",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Путь к выходному файлу",
    )
    parser.add_argument(
        "--sym-key",
        dest="sym_key",
        type=str,
        help="Путь к зашифрованному симметричному ключу",
    )
    parser.add_argument(
        "--public-key",
        dest="public_key",
        type=str,
        help="Путь к открытому RSA-ключу",
    )
    parser.add_argument(
        "--private-key",
        dest="private_key",
        type=str,
        help="Путь к закрытому RSA-ключу",
    )

    return parser.parse_args()


def main() -> None:
    """
    Точка входа приложения.
    """

    args = parse_arguments()
    settings = load_config("settings.json")

    path_sym_key = args.sym_key or settings["symmetric_key"]
    path_public_key = args.public_key or settings["public_key"]
    path_private_key = args.private_key or settings["private_key"]

    match args:
        case _ if args.generation:
            generate(
                path_sym_key,
                path_public_key,
                path_private_key,
                settings["symmetric_key_length"],
            )

        case _ if args.encryption:
            encrypt(
                args.input or settings["initial_file"],
                path_private_key,
                path_sym_key,
                args.output or settings["encrypted_file"],
            )

        case _ if args.decryption:
            decrypt(
                args.input or settings["encrypted_file"],
                path_private_key,
                path_sym_key,
                args.output or settings["decrypted_file"],
            )


if __name__ == "__main__":
    main()