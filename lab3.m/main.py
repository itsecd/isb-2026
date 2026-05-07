"""
Режимы можно использовать в произвольном порядке и независимо.

Использование:
    python main.py -gen <зашифр_ключ> <открытый_ключ> <закрытый_ключ>
    python main.py -enc <файл> <закрытый_ключ> <зашифр_ключ> <выход>
    python main.py -dec <файл> <закрытый_ключ> <зашифр_ключ> <выход>
    python main.py -enc-custom <файл> <PEM> <HEX> <выход>
    python main.py -dec-custom <файл> <PEM> <HEX> <выход>
"""

import argparse
from key_gen import generate_keys
from encrypt import encrypt_file
from decrypt import decrypt_file
from crypto_custom import encrypt_custom, decrypt_custom


def main() -> None:
    """
    Точка входа. Парсит аргументы командной строки
    и запускает нужный режим.
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема RSA + IDEA (128 бит)",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-gen", "--generation", nargs=3,
        metavar=("ENC_SYM_KEY", "PUBLIC_KEY", "PRIVATE_KEY"),
        help="Генерация ключей",
    )
    group.add_argument(
        "-enc", "--encryption", nargs=4,
        metavar=("INPUT", "PRIVATE_KEY", "ENC_SYM_KEY", "OUTPUT"),
        help="Шифрование (ключи из файлов)",
    )
    group.add_argument(
        "-dec", "--decryption", nargs=4,
        metavar=("INPUT", "PRIVATE_KEY", "ENC_SYM_KEY", "OUTPUT"),
        help="Дешифрование (ключи из файлов)",
    )
    group.add_argument(
        "-enc-custom", "--encryption-custom", nargs=4,
        metavar=("INPUT", "PRIVATE_KEY_PEM", "ENC_SYM_KEY_HEX", "OUTPUT"),
        help="Шифрование со своими ключами",
    )
    group.add_argument(
        "-dec-custom", "--decryption-custom", nargs=4,
        metavar=("INPUT", "PRIVATE_KEY_PEM", "ENC_SYM_KEY_HEX", "OUTPUT"),
        help="Дешифрование со своими ключами",
    )

    args = parser.parse_args()

    match args:
        case _ if args.generation is not None:
            generate_keys(
                enc_sym_key_path=args.generation[0],
                public_key_path=args.generation[1],
                private_key_path=args.generation[2],
            )
        case _ if args.encryption is not None:
            encrypt_file(
                input_path=args.encryption[0],
                private_key_path=args.encryption[1],
                enc_sym_key_path=args.encryption[2],
                output_path=args.encryption[3],
            )
        case _ if args.decryption is not None:
            decrypt_file(
                input_path=args.decryption[0],
                private_key_path=args.decryption[1],
                enc_sym_key_path=args.decryption[2],
                output_path=args.decryption[3],
            )
        case _ if args.encryption_custom is not None:
            encrypt_custom(
                input_path=args.encryption_custom[0],
                private_key_pem=args.encryption_custom[1],
                enc_sym_key_hex=args.encryption_custom[2],
                output_path=args.encryption_custom[3],
            )
        case _ if args.decryption_custom is not None:
            decrypt_custom(
                input_path=args.decryption_custom[0],
                private_key_pem=args.decryption_custom[1],
                enc_sym_key_hex=args.decryption_custom[2],
                output_path=args.decryption_custom[3],
            )


if __name__ == "__main__":
    main()