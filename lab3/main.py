import argparse
from utils import load_settings
from keygen import generate_keys
from encrypt import encrypt_data
from decrypt import decrypt_data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Гибридная криптосистема (RSA + Camellia)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true', help='Запускает режим дешифрования')
    parser.add_argument('-s', '--size', type=int, choices=[128, 192, 256], default=256, help='Длина ключа Camellia в битах (128, 192 или 256)')

    args = parser.parse_args()
    config = load_settings()

    if args.generation:
        generate_keys(config, args.size)
    elif args.encryption:
        encrypt_data(config)
    elif args.decryption:
        decrypt_data(config)