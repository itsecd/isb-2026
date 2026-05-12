import argparse

from file_utils import load_settings
from generate_key import generate_key
from encrypt import encrypt
from decrypt import decrypt


def parse_args() -> argparse.Namespace:
    """Разбор аргументов командной строки.
    Поддерживается 3 режима работы (генерация, шифрование, дешифрование) и необязательные пути
    к ключам, которые переопределяют значения из settings.json.
    Для режима генерации обязательно указывается длина симметричного ключа.
    """
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

    parser.add_argument("--public-key", dest="public_key", default=None,
                        metavar="PATH",
                        help="Путь к своему открытому RSA-ключу (PEM). "
                             "Заменяет public_key из settings.json.")
    parser.add_argument("--secret-key", dest="secret_key", default=None,
                        metavar="PATH",
                        help="Путь к своему закрытому RSA-ключу (PEM). "
                             "Заменяет secret_key из settings.json.")
    parser.add_argument("--symmetric-key", dest="symmetric_key", default=None,
                        metavar="PATH",
                        help="Путь к своему зашифрованному симметричному ключу. "
                             "Заменяет symmetric_key из settings.json.")
    parser.add_argument("--key-bits", dest="key_bits", type=int,
                        choices=[128, 192, 256], default=256,
                        help="Длина симметричного ключа Camellia в битах. "
                             "Допустимые значения: 128, 192, 256. По умолчанию 256.")
    return parser.parse_args()


def main() -> None:
    """Точка входа.
    Считывает аргументы командной строки и настройки из settings.json,
    после чего вызывает 1 из 3 режимов работы: генерацию ключей,
    шифрование или расшифровку файла.
    """
    args = parse_args()
    settings = load_settings("settings.json")

    public_key_path    = args.public_key    or settings["public_key"]
    secret_key_path    = args.secret_key    or settings["secret_key"]
    symmetric_key_path = args.symmetric_key or settings["symmetric_key"]

    match args:
        case argparse.Namespace(generation=True):
            generate_key(
                symmetric_key_path,
                public_key_path,
                secret_key_path,
                args.key_bits,
            )
        case argparse.Namespace(encryption=True):
            encrypt(
                settings["initial_file"],
                secret_key_path,
                symmetric_key_path,
                settings["encrypted_file"],
            )
        case argparse.Namespace(decryption=True):
            decrypt(
                settings["encrypted_file"],
                secret_key_path,
                symmetric_key_path,
                settings["decrypted_file"],
            )


if __name__ == "__main__":
    main()