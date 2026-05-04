import argparse

from file_utils import load_settings
from generate_key import generate_key
from encrypt import encrypt
from decrypt import decrypt


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Гибридная система шифрования RSA + Camellia."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true",
                       help="Запускает режим генерации ключей.")
    group.add_argument("-enc", "--encryption", action="store_true",
                       help="Запускает режим шифрования.")
    group.add_argument("-dec", "--decryption", action="store_true",
                       help="Запускает режим дешифрования.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    settings = load_settings("settings.json")

    match True:
        case _ if args.generation:
            generate_key(
                settings["symmetric_key"],
                settings["public_key"],
                settings["secret_key"],
            )
        case _ if args.encryption:
            encrypt(
                settings["initial_file"],
                settings["secret_key"],
                settings["symmetric_key"],
                settings["encrypted_file"],
            )
        case _ if args.decryption:
            decrypt(
                settings["encrypted_file"],
                settings["secret_key"],
                settings["symmetric_key"],
                settings["decrypted_file"],
            )

if __name__ == "__main__":
    main()