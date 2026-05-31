import argparse
import sys

from utils import settings, FileUtilsError
from crypto_hybrid import generate_hybrid_keys, encrypt_data, decrypt_data


def parse_arguments() -> argparse.Namespace:
    """
    Разбирает аргументы командной строки.
    
    Returns:
        argparse.Namespace: Объект с распарсенными аргументами
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (RSA + Blowfish)",
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', 
                       help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', 
                       help='Шифрование файла')
    group.add_argument('-dec', '--decryption', action='store_true', 
                       help='Дешифрование файла')
    
    return parser.parse_args()


def main() -> None:
    """
    Главная функция приложения.
    """
    try:
        args = parse_arguments()
        settings = load_settings()
        
        if args.generation:
            generate_hybrid_keys(settings)
        elif args.encryption:
            encrypt_data(settings)
        elif args.decryption:
            decrypt_data(settings)
            
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
