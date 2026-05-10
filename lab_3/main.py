import argparse
import json
import os.path
from key_generator import generate_keys

def load_settings() -> dict:
    setting_file = 'settings.json'
    if not os.path.exists(setting_file):
        default_settings = {
            'initial_file': 'text.txt',
            'encrypted_file': 'encrypted.bin',
            'decrypted_file': 'decrypted.txt',
            'symmetric_key': 'symmetric_key.bin',
            'public_key': 'public_key.pem',
            'secret_key': 'secret_key.pem',
        }
        with open(setting_file, 'w', encoding='utf-8') as json_file:
            json.dump(default_settings, json_file)
    with open(setting_file, 'r', encoding='utf-8') as json_file:
        return json.load(json_file)


def parse_arguments() -> argparse.Namespace:
    """
    Adds and parses command-line arguments
    """
    parser = argparse.ArgumentParser(description="Search candidates by phone code")
    parser.add_argument('-l', '--length', type=int, default=256,
                        help='Длина ключа для Blowfish (от 32 до 448б кратный 8)')
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
        if args.generation:
            if not (32 <= args.length <= 448 and args.length % 8 == 0):
                raise ValueError("Blowfish требует ключ от 32 до 448 бит и кратный 8")
            generate_keys(settings, args.length)
        elif args.encryption:
            encrypt_with_keys(settings)
        elif args.decryption:
            decrypt_with_keys(settings)

    except Exception as err:
        print(f"Error while working: {err}")


if __name__ == "__main__":
    main()
