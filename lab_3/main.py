import argparse

from settings_loader import load_config

from cipher_core import (
    generate_keys,
    encrypt_file,
    decrypt_file
)


def main():

    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема RSA + IDEA"
    )

    parser.add_argument(
        "-c",
        "--config",
        default="settings.json",
        help="Путь к settings.json"
    )

    group = parser.add_mutually_exclusive_group(
        required=True
    )

    group.add_argument(
        "-gen",
        "--generation",
        action="store_true",
        help="Генерация ключей"
    )

    group.add_argument(
        "-enc",
        "--encryption",
        action="store_true",
        help="Шифрование файла"
    )

    group.add_argument(
        "-dec",
        "--decryption",
        action="store_true",
        help="Дешифрование файла"
    )

    args = parser.parse_args()

    settings = load_config(args.config)

    if args.generation:

        generate_keys(
            settings["encrypted_key_file"],
            settings["public_key_file"],
            settings["private_key_file"]
        )

    elif args.encryption:

        encrypt_file(
            settings["input_file"],
            settings["private_key_file"],
            settings["encrypted_key_file"],
            settings["encrypted_file"]
        )

    elif args.decryption:

        decrypt_file(
            settings["encrypted_file"],
            settings["private_key_file"],
            settings["encrypted_key_file"],
            settings["decrypted_file"]
        )


if __name__ == "__main__":
    main()