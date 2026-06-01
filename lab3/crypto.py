import argparse
import sys
from hybrid import HybridCrypto
from utils import load_settings, FileUtilsError


def parse_arguments() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.
    
    Returns:
        argparse.Namespace: Объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (RSA + Blowfish)"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-k', '--keygen', action='store_true',
                       help='Генерация ключей')
    group.add_argument('-e', '--encrypt', action='store_true',
                       help='Шифрование файла')
    group.add_argument('-d', '--decrypt', action='store_true',
                       help='Дешифрование файла')
    
    return parser.parse_args()


def main() -> None:
    """
    Главная функция приложения.
    """
    try:
        args = parse_arguments()
        settings = load_settings()
        crypto = HybridCrypto()
        
        if args.keygen:
            print("Генерация ключей")
            crypto.generate_keys(
                settings['public_key'],
                settings['secret_key'],
                settings['symmetric_key'],
                settings['symmetric_key_length']
            )
            print("Готово")
            
        elif args.encrypt:
            print("Шифрование файла")
            crypto.encrypt_file(
                settings['initial_file'],
                settings['encrypted_file'],
                settings['public_key'],
                settings['symmetric_key'],
                settings['symmetric_key_length']
            )
            print("Готово")
            
        elif args.decrypt:
            print("Расшифровка файла")
            crypto.decrypt_file(
                settings['encrypted_file'],
                settings['decrypted_file'],
                settings['secret_key'],
                settings['symmetric_key']
            )
            print("Готово")
            
    except FileUtilsError as err:
        print(f"Ошибка при работе с файлами: {err}", file=sys.stderr)
        sys.exit(1)
    except ValueError as err:
        print(f"Ошибка валидации: {err}", file=sys.stderr)
        sys.exit(1)
    except Exception as err:
        print(f"Непредвиденная ошибка: {err}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()