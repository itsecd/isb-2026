import argparse
import sys

from auxiliary_functions import load_settings
from key_generation import generate_keys
from encryptor import encrypt_data
from decryptor import decrypt_data

def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--gen', action='store_true', help='Генерация ключей')
    group.add_argument('--enc', action='store_true', help='Шифрование данных')
    group.add_argument('--dec', action='store_true', help='Дешифрование данных')
    
    parser.add_argument('--settings', type=str, default='settings.json', help='Путь к файлу настроек JSON')

    args = parser.parse_args()
    settings = load_settings(args.settings)

    match True:
        case _ if args.gen:
            generate_keys(settings)
        case _ if args.enc:
            encrypt_data(settings)
        case _ if args.dec:
            decrypt_data(settings)

if __name__ == '__main__':
    main()