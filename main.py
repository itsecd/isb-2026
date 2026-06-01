"""
Точка входа гибридной криптосистемы RSA + 3DES.

Обеспечивает CLI-интерфейс с тремя взаимоисключающими режимами:
генерация ключей, шифрование и дешифрование. Пути могут задаваться
через аргументы командной строки, файл settings.json или значения
по умолчанию.
"""

import argparse
import sys
from utils import load_settings, get_path
from keys import generate_keys
from crypto import encrypt_data, decrypt_data


def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы командной строки.

    Returns:
        Объект Namespace с разобранными аргументами.
    """
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (RSA + 3DES/DES)"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true',
                       help='Режим генерации ключей')
    group.add_argument('-enc', '--encrypt', action='store_true',
                       help='Режим шифрования')
    group.add_argument('-dec', '--decrypt', action='store_true',
                       help='Режим дешифрования')

    parser.add_argument('--key-len', type=int, choices=[64, 128, 192],
                        default=192,
                        help='Длина симметричного ключа в битах (только -gen)')
    parser.add_argument('--pub-key', type=str,
                        help='Путь для открытого ключа RSA')
    parser.add_argument('--priv-key', type=str,
                        help='Путь для закрытого ключа RSA')
    parser.add_argument('--enc-sym-key', type=str,
                        help='Путь для зашифрованного симметричного ключа')
    parser.add_argument('--input', type=str,
                        help='Входной файл')
    parser.add_argument('--output', type=str,
                        help='Выходной файл')
    parser.add_argument('--loaded-priv-key', type=str,
                        help='Путь к закрытому ключу RSA (-enc/-dec)')
    parser.add_argument('--loaded-enc-sym-key', type=str,
                        help='Путь к зашифрованному симметричному ключу (-enc/-dec)')

    return parser.parse_args()


def main() -> None:
    """
    Главная функция приложения.

    Загружает настройки, определяет пути по приоритету и вызывает
    соответствующий режим работы. Перехватывает все исключения верхнего
    уровня и выводит понятное сообщение об ошибке.
    """
    args = parse_args()
    settings = load_settings()

    try:
        if args.generate:
            pub_key_path = get_path(args.pub_key, settings, 'public_key', 'public.pem')
            priv_key_path = get_path(args.priv_key, settings, 'secret_key', 'private.pem')
            enc_sym_key_path = get_path(args.enc_sym_key, settings,
                                        'symmetric_key_encrypted', 'sym_key.enc')
            generate_keys(args.key_len, pub_key_path, priv_key_path, enc_sym_key_path)

        elif args.encrypt:
            input_path = get_path(args.input, settings, 'initial_file', 'input.txt')
            output_path = get_path(args.output, settings, 'encrypted_file', 'output.enc')
            priv_key_path = get_path(args.loaded_priv_key, settings, 'secret_key', 'private.pem')
            enc_sym_key_path = get_path(args.loaded_enc_sym_key, settings,
                                        'symmetric_key_encrypted', 'sym_key.enc')
            encrypt_data(input_path, priv_key_path, enc_sym_key_path, output_path)

        elif args.decrypt:
            input_path = get_path(args.input, settings, 'encrypted_file', 'output.enc')
            output_path = get_path(args.output, settings, 'decrypted_file', 'decrypted.txt')
            priv_key_path = get_path(args.loaded_priv_key, settings, 'secret_key', 'private.pem')
            enc_sym_key_path = get_path(args.loaded_enc_sym_key, settings,
                                        'symmetric_key_encrypted', 'sym_key.enc')
            decrypt_data(input_path, priv_key_path, enc_sym_key_path, output_path)

    except FileNotFoundError as e:
        print(f"\n[FATAL] Файл не найден: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"\n[FATAL] Ошибка параметров: {e}", file=sys.stderr)
        sys.exit(1)
    except PermissionError as e:
        print(f"\n[FATAL] Нет прав доступа: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[FATAL] Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()