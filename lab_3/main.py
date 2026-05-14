import argparse

from mixed import encrypt_data, decrypt_data
from keygen import generate_keys
from fileutils import load_settings


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments
    """
    parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + Blowfish)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true', help='Запускает режим дешифрования')
    return parser.parse_args()


def main() -> None:
    """
    Main function
    """
    try:
        args = parse_arguments()
        settings = load_settings()
        match args:
            case _ if args.generation:
                key_length = settings['symmetric_key_length']
                if not (32 <= key_length <= 448 and key_length % 8 == 0):
                    raise ValueError("Blowfish требует ключ от 32 до 448 бит и кратный 8")
                generate_keys(settings)
            case _ if args.encryption:
                encrypt_data(settings)
            case _ if args.decryption:
                decrypt_data(settings)

    except ValueError as err:
        print(f"Not valid value: {err}")
    except Exception as err:
        print(f"Error while working: {err}")


if __name__ == "__main__":
    main()
