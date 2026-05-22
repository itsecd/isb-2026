
import sys
import os
import argparse
import json

from crypto_symmetric import validate_blowfish_key_length
from crypto_hybrid import generate_hybrid_keys, encrypt_file, decrypt_file
from utils import handle_error


def load_json_settings(json_path: str) -> dict:
    """Загружает настройки из JSON файла."""
    if not json_path or not os.path.exists(json_path):
        return {}
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def mode_generation(args) -> bool:
    """Режим генерации ключей."""
    try:
        generate_hybrid_keys(
            public_path=args.public_key,
            secret_path=args.secret_key,
            encrypted_sym_key_path=args.encrypted_symmetric_key,
            sym_key_length=args.key_length
        )
        print(f"[OK] Ключи сгенерированы. Длина ключа Blowfish: {args.key_length} бит")
        print(f"  Публичный ключ: {args.public_key}")
        print(f"  Приватный ключ: {args.secret_key}")
        print(f"  Зашифрованный ключ: {args.encrypted_symmetric_key}")
        return True
    except Exception as e:
        print(f"[ERROR] {handle_error(e, 'генерация')}")
        return False


def mode_encryption(args) -> bool:
    """Режим шифрования файла."""
    try:
        if not os.path.exists(args.input_file):
            print(f"[ERROR] Файл не найден: {args.input_file}")
            return False
        
        encrypt_file(
            input_file=args.input_file,
            output_file=args.output_file,
            private_key_path=args.secret_key,
            encrypted_sym_key_path=args.encrypted_symmetric_key
        )
        
        original_size = os.path.getsize(args.input_file)
        encrypted_size = os.path.getsize(args.output_file)
        
        print(f"[OK] Файл зашифрован")
        print(f"  Исходный файл: {args.input_file} ({original_size} байт)")
        print(f"  Зашифрованный файл: {args.output_file} ({encrypted_size} байт)")
        return True
    except Exception as e:
        print(f"[ERROR] {handle_error(e, 'шифрование')}")
        return False


def mode_decryption(args) -> bool:
    """Режим дешифрования файла."""
    try:
        if not os.path.exists(args.input_file):
            print(f"[ERROR] Файл не найден: {args.input_file}")
            return False
        
        decrypt_file(
            input_file=args.input_file,
            output_file=args.output_file,
            private_key_path=args.secret_key,
            encrypted_sym_key_path=args.encrypted_symmetric_key
        )
        
        output_size = os.path.getsize(args.output_file)
        
        print(f"[OK] Файл расшифрован")
        print(f"  Зашифрованный файл: {args.input_file}")
        print(f"  Расшифрованный файл: {args.output_file} ({output_size} байт)")
        return True
    except Exception as e:
        print(f"[ERROR] {handle_error(e, 'дешифрование')}")
        return False


def main() -> None:
    """Главная функция."""
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + Blowfish")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Генерация ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Шифрование файла')
    group.add_argument('-dec', '--decryption', action='store_true', help='Дешифрование файла')
    
    parser.add_argument('--json', type=str, help='Путь к JSON файлу с настройками')
    parser.add_argument('--public_key', type=str, help='Путь для публичного RSA ключа')
    parser.add_argument('--secret_key', type=str, help='Путь для приватного RSA ключа')
    parser.add_argument('--encrypted_symmetric_key', type=str, help='Путь к зашифрованному ключу')
    parser.add_argument('--input_file', type=str, help='Входной файл')
    parser.add_argument('--output_file', type=str, help='Выходной файл')
    parser.add_argument('--key_length', type=int, default=128, help='Длина ключа Blowfish (32-448, кратно 8)')
    
    args = parser.parse_args()
    
    if args.key_length:
        try:
            validate_blowfish_key_length(args.key_length)
        except ValueError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
    
    json_data = load_json_settings(args.json)
    
    def get_val(key: str, cli_val):
        return cli_val if cli_val is not None else json_data.get(key)
    
    success = False
    
    if args.generation:
        args.public_key = get_val('public_key', args.public_key)
        args.secret_key = get_val('secret_key', args.secret_key)
        args.encrypted_symmetric_key = get_val('encrypted_symmetric_key', args.encrypted_symmetric_key)
        
        if not all([args.public_key, args.secret_key, args.encrypted_symmetric_key]):
            print("[ERROR] Для генерации нужны: --public_key, --secret_key, --encrypted_symmetric_key")
            sys.exit(1)
        
        success = mode_generation(args)
        
    elif args.encryption:
        args.input_file = get_val('input_file', get_val('initial_file', args.input_file))
        args.output_file = get_val('output_file', get_val('encrypted_file', args.output_file))
        args.secret_key = get_val('secret_key', args.secret_key)
        args.encrypted_symmetric_key = get_val('encrypted_symmetric_key', args.encrypted_symmetric_key)
        
        if not all([args.input_file, args.output_file, args.secret_key, args.encrypted_symmetric_key]):
            print("[ERROR] Для шифрования нужны: --input_file, --output_file, --secret_key, --encrypted_symmetric_key")
            sys.exit(1)
        
        success = mode_encryption(args)
        
    elif args.decryption:
        args.input_file = get_val('input_file', get_val('encrypted_file', args.input_file))
        args.output_file = get_val('output_file', get_val('decrypted_file', args.output_file))
        args.secret_key = get_val('secret_key', args.secret_key)
        args.encrypted_symmetric_key = get_val('encrypted_symmetric_key', args.encrypted_symmetric_key)
        
        if not all([args.input_file, args.output_file, args.secret_key, args.encrypted_symmetric_key]):
            print("[ERROR] Для дешифрования нужны: --input_file, --output_file, --secret_key, --encrypted_symmetric_key")
            sys.exit(1)
        
        success = mode_decryption(args)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()