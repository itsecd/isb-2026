import json
import argparse
import sys

import constants as const
from hybrid_crypto import generate_keys, encrypt_data, decrypt_data


def load_settings(settings_file: str) -> dict:
    """Загружает настройки из JSON-файла"""
    try:
        with open(settings_file, 'r', encoding='utf-8') as f:
            settings = json.load(f)
        print(f"[OK] Настройки загружены из {settings_file}")
        return settings
    except FileNotFoundError:
        print(f"[ОШИБКА] Файл настроек {settings_file} не найден!")
        sys.exit(1)


def create_default_settings_file(settings_file: str):
    """ Создаёт файл настроек со значениями по умолчанию """
    default_settings = {
        "initial_file": const.DEFAULT_INITIAL_FILE,
        "encrypted_file": const.DEFAULT_ENCRYPTED_FILE,
        "decrypted_file": const.DEFAULT_DECRYPTED_FILE,
        "symmetric_key_file": const.DEFAULT_SYMMETRIC_KEY_FILE,
        "nonce_file": const.DEFAULT_NONCE_FILE,
        "encrypted_symmetric_key_file": const.DEFAULT_ENCRYPTED_SYMMETRIC_KEY_FILE,
        "public_key_file": const.DEFAULT_PUBLIC_KEY_FILE,
        "private_key_file": const.DEFAULT_PRIVATE_KEY_FILE
    }
    with open(settings_file, 'w', encoding='utf-8') as f:
        json.dump(default_settings, f, indent=4)
    print(f"[OK] Создан файл настроек по умолчанию: {settings_file}")
    return default_settings


def main():
    # Парсинг аргументов командной строки
    parser = argparse.ArgumentParser(description="Гибридная криптосистема: RSA + ChaCha20")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Запускает режим шифрования данных')
    group.add_argument('-dec', '--decryption', action='store_true', help='Запускает режим дешифрования данных')
    parser.add_argument('-s', '--settings', type=str, default=const.DEFAULT_SETTINGS_FILE, help=f'Путь к файлу настроек (по умолчанию: {const.DEFAULT_SETTINGS_FILE})')

    args = parser.parse_args()

    # Загрузка или создание файла настроек
    try:
        settings = load_settings(args.settings)
    except FileNotFoundError:
        settings = create_default_settings_file(args.settings)

    # Проверка наличия всех необходимых ключей в настройках
    required_keys = [
        'initial_file', 'encrypted_file', 'decrypted_file',
        'symmetric_key_file', 'nonce_file', 'encrypted_symmetric_key_file',
        'public_key_file', 'private_key_file' ]
    
    for key in required_keys:
        if key not in settings:
            print(f"[ОШИБКА] В файле настроек отсутствует ключ '{key}'")
            sys.exit(1)

    # Выполнение соответствующего режима
    if args.generation:
        generate_keys(
            symmetric_key_path=settings['symmetric_key_file'],
            nonce_path=settings['nonce_file'],
            encrypted_symmetric_key_path=settings['encrypted_symmetric_key_file'],
            public_key_path=settings['public_key_file'],
            private_key_path=settings['private_key_file']
        )
    elif args.encryption:
        encrypt_data(
            initial_file_path=settings['initial_file'],
            encrypted_file_path=settings['encrypted_file'],
            encrypted_symmetric_key_path=settings['encrypted_symmetric_key_file'],
            private_key_path=settings['private_key_file'],
            nonce_path=settings['nonce_file']
        )
    elif args.decryption:
        decrypt_data(
            encrypted_file_path=settings['encrypted_file'],
            decrypted_file_path=settings['decrypted_file'],
            encrypted_symmetric_key_path=settings['encrypted_symmetric_key_file'],
            private_key_path=settings['private_key_file'],
            nonce_path=settings['nonce_file']
        )


if __name__ == "__main__":
    main()