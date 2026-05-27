import argparse
import sys
import os

from modules.config import read_config, load_settings, validate_symmetric_key_size
from modules.keys import (
    generate_symmetric_key,
    generate_asymmetric_keys,
    save_private_key,
    save_public_key,
    load_private_key,
    load_public_key,
    save_encrypted_symmetric_key,
    load_encrypted_symmetric_key
)
from modules.symmetric import encrypt_file, decrypt_file
from modules.asymmetric import encrypt_symmetric_key, decrypt_symmetric_key


def mode_generation(config_path: str) -> None:
    """
    Режим генерации ключей гибридной криптосистемы.

    Выполняет следующие шаги:
    1. Загружает конфигурацию из JSON-файла.
    2. Генерирует симметричный ключ AES заданной длины.
    3. Генерирует пару асимметричных ключей RSA.
    4. Сохраняет открытый и закрытый ключи RSA в PEM-файлы.
    5. Шифрует симметричный ключ открытым ключом RSA.
    6. Сохраняет зашифрованный симметричный ключ.

    Args:
        config_path (str): путь к JSON-файлу конфигурации.

    Параметры конфигурации:
        - public_key: путь для сохранения открытого ключа.
        - private_key: путь для сохранения закрытого ключа.
        - encrypted_symmetric_key: путь для сохранения зашифрованного симметричного ключа.
        - symmetric_key_size_bits (опционально): длина ключа AES (128, 192, 256).
        - user_public_key (опционально): путь к пользовательскому открытому ключу.
        - user_private_key (опционально): путь к пользовательскому закрытому ключу.
    """
    print("\nРежим генерации ключей\n")
    
    settings = load_settings()
    config = read_config(config_path)
    
    symmetric_bits = validate_symmetric_key_size(
        config.get('symmetric_key_size_bits', settings['default_symmetric_key_size'])
    )
    
    symmetric_key = generate_symmetric_key(symmetric_bits)
    
    use_user_rsa_keys = bool(config.get('user_public_key')) and bool(config.get('user_private_key'))
    
    match use_user_rsa_keys:
        case True:
            print("\nИспользую пользовательские ключи RSA")
            try:
                public_key = load_public_key(config['user_public_key'])
                private_key = load_private_key(config['user_private_key'])
            except Exception:
                print("Не удалось загрузить пользовательские ключи. Генерирую новые.")
                private_key, public_key = generate_asymmetric_keys(
                    key_size=settings['default_rsa_key_size'],
                    public_exponent=settings['rsa_public_exponent']
                )
                save_private_key(private_key, config['private_key'])
                save_public_key(public_key, config['public_key'])
        case False:
            print("\nГенерирую новую пару ключей RSA")
            private_key, public_key = generate_asymmetric_keys(
                key_size=settings['default_rsa_key_size'],
                public_exponent=settings['rsa_public_exponent']
            )
            save_private_key(private_key, config['private_key'])
            save_public_key(public_key, config['public_key'])
    
    encrypted_sym_key = encrypt_symmetric_key(symmetric_key, public_key)
    save_encrypted_symmetric_key(encrypted_sym_key, config['encrypted_symmetric_key'])
    
    print("\nГенерация ключей успешно завершена\n")


def mode_encryption(config_path: str) -> None:
    """
    Режим шифрования данных гибридной криптосистемой.

    Выполняет следующие шаги:
    1. Загружает конфигурацию из JSON-файла.
    2. Загружает закрытый ключ RSA.
    3. Загружает зашифрованный симметричный ключ.
    4. Расшифровывает симметричный ключ с помощью RSA.
    5. Шифрует данные алгоритмом AES с расшифрованным ключом.

    Args:
        config_path (str): путь к JSON-файлу конфигурации.

    Параметры конфигурации:
        - initial_file: путь к файлу для шифрования.
        - private_key: путь к закрытому ключу RSA.
        - encrypted_symmetric_key: путь к зашифрованному симметричному ключу.
        - encrypted_file: путь для сохранения зашифрованного файла.
    """
    print("\nРежим шифрования\n")
    
    config = read_config(config_path)
    
    try:
        private_key = load_private_key(config['private_key'])
    except Exception:
        print("Критическая ошибка при загрузке закрытого ключа.")
        sys.exit(1)
    
    try:
        encrypted_sym = load_encrypted_symmetric_key(config['encrypted_symmetric_key'])
    except Exception:
        print("Критическая ошибка при загрузке зашифрованного симметричного ключа.")
        sys.exit(1)
    
    try:
        symmetric_key = decrypt_symmetric_key(encrypted_sym, private_key)
    except Exception:
        print("Критическая ошибка при расшифровке симметричного ключа.")
        sys.exit(1)
    
    try:
        encrypt_file(config['initial_file'], config['encrypted_file'], symmetric_key)
    except Exception:
        print("Критическая ошибка при шифровании файла.")
        sys.exit(1)
    
    print("\nШифрование успешно завершено\n")


def mode_decryption(config_path: str) -> None:
    """
    Режим дешифрования данных гибридной криптосистемой.

    Выполняет следующие шаги:
    1. Загружает конфигурацию из JSON-файла.
    2. Загружает закрытый ключ RSA.
    3. Загружает зашифрованный симметричный ключ.
    4. Расшифровывает симметричный ключ с помощью RSA.
    5. Расшифровывает данные алгоритмом AES с расшифрованным ключом.

    Args:
        config_path (str): путь к JSON-файлу конфигурации.

    Параметры конфигурации:
        - encrypted_file: путь к зашифрованному файлу.
        - private_key: путь к закрытому ключу RSA.
        - encrypted_symmetric_key: путь к зашифрованному симметричному ключу.
        - decrypted_file: путь для сохранения расшифрованного файла.
    """
    print("\nРежим дешифрования\n")
    
    config = read_config(config_path)
    
    try:
        private_key = load_private_key(config['private_key'])
    except Exception:
        print("Критическая ошибка при загрузке закрытого ключа.")
        sys.exit(1)
    
    try:
        encrypted_sym = load_encrypted_symmetric_key(config['encrypted_symmetric_key'])
    except Exception:
        print("Критическая ошибка при загрузке зашифрованного симметричного ключа.")
        sys.exit(1)
    
    try:
        symmetric_key = decrypt_symmetric_key(encrypted_sym, private_key)
    except Exception:
        print("Критическая ошибка при расшифровке симметричного ключа.")
        sys.exit(1)
    
    try:
        decrypt_file(config['encrypted_file'], config['decrypted_file'], symmetric_key)
    except Exception:
        print("Критическая ошибка при расшифровке файла.")
        sys.exit(1)
    
    print("\nДешифрование успешно завершено\n")


def create_parser() -> argparse.ArgumentParser:
    """
    Создаёт парсер аргументов командной строки.

    Returns:
        argparse.ArgumentParser: настроенный парсер.
    """
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема AES + RSA. Лабораторная работа No3'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-gen', '--generation',
        action='store_true',
        help='Запуск режима генерации ключей'
    )
    group.add_argument(
        '-enc', '--encryption',
        action='store_true',
        help='Запуск режима шифрования файла'
    )
    group.add_argument(
        '-dec', '--decryption',
        action='store_true',
        help='Запуск режима дешифрования файла'
    )
    parser.add_argument(
        'config',
        help='Путь к JSON-файлу с конфигурацией'
    )
    
    return parser


def main() -> None:
    """
    Главная функция программы.

    Разбирает аргументы командной строки и запускает соответствующий режим.
    Использует конструкцию match/case для выбора режима работы.
    """
    parser = create_parser()
    
    try:
        args = parser.parse_args()
    except SystemExit:
        sys.exit(1)
    
    match args:
        case _ if args.generation:
            mode_generation(args.config)
        case _ if args.encryption:
            mode_encryption(args.config)
        case _ if args.decryption:
            mode_decryption(args.config)
        case _:
            parser.print_help()
            sys.exit(1)


if __name__ == '__main__':
    main()