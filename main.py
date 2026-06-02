import argparse
import sys
from commands import (
    load_config,
    generate_rsa_keys,
    encrypt_text,
    decrypt_text,
    show_encrypted,
    show_decrypted,
    show_keys
)


def main():
    parser = argparse.ArgumentParser(description="RSA + SM4 шифрование")
    parser.add_argument("-s", "--settings", default="settings.json", help="путь к JSON-файлу конфигурации")
    subparsers = parser.add_subparsers(dest="command", required=True, help="команда")
    subparsers.add_parser("generate-rsa", help="Сгенерировать RSA-ключи")
    encrypt_parser = subparsers.add_parser("encrypt", help="Зашифровать файл")
    encrypt_parser.add_argument("-i", "--input-file", help="входной текстовый файл")
    subparsers.add_parser("decrypt", help="Расшифровать файл")
    subparsers.add_parser("show-encrypted", help="Показать зашифрованный файл в hex")
    subparsers.add_parser("show-decrypted", help="Показать расшифрованный текст")
    subparsers.add_parser("show-keys", help="Показать ключи")

    args = parser.parse_args()
    config = load_config(args.settings)

    match args.command:
        case "generate-rsa":
            generate_rsa_keys(config)
        case "encrypt":
            encrypt_text(config, getattr(args, "input_file", None))
        case "decrypt":
            decrypt_text(config)
        case "show-encrypted":
            show_encrypted(config)
        case "show-decrypted":
            show_decrypted(config)
        case "show-keys":
            show_keys(config)
        case _:
            parser.print_help()
            sys.exit(1)


if __name__ == "__main__":
    main()
