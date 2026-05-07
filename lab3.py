import json
import sys
import argparse

from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from key_generator import generate_rsa_keys, save_rsa_keys, generate_aes_key
from encryptor import encrypt_symmetric_key, aes_encrypt_file
from decryptor import decrypt_symmetric_key, aes_decrypt_file


def load_public_key(path):
    try:
        with open(path, 'rb') as f:
            return load_pem_public_key(f.read())
    except FileNotFoundError:
        print(f"Файл открытого ключа не найден: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при загрузке открытого ключа: {e}")
        sys.exit(1)


def load_private_key(path):
    try:
        with open(path, 'rb') as f:
            return load_pem_private_key(f.read(), password=None)
    except FileNotFoundError:
        print(f"Файл закрытого ключа не найден: {path}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при загрузке закрытого ключа: {e}")
        sys.exit(1)


def load_config(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Файл конфигурации не найден: {path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Ошибка чтения JSON в файле {path}: {e}")
        sys.exit(1)

    required_keys = [
        'initial_file', 'encrypted_file', 'decrypted_file',
        'symmetric_key', 'public_key', 'secret_key'
    ]
    missing = [k for k in required_keys if k not in config]
    if missing:
        print(f"В конфигурации не хватает ключей: {', '.join(missing)}")
        sys.exit(1)

    config.setdefault('aes_key_size', 256)
    return config


def mode_generate_keys(config):
    print("\nРежим генерации ключей\n")

    key_size = config['aes_key_size']
    if key_size not in (128, 192, 256):
        print(
            f"Некорректная длина ключа AES: {key_size}.\n"
            f"Допустимые значения: 128, 192, 256. Использую 256."
        )
        key_size = 256

    symmetric_key = generate_aes_key(key_size)
    private_key, public_key = generate_rsa_keys()

    save_rsa_keys(private_key, public_key, config['secret_key'], config['public_key'])

    encrypted_sym_key = encrypt_symmetric_key(symmetric_key, public_key)
    try:
        with open(config['symmetric_key'], 'wb') as f:
            f.write(encrypted_sym_key)
        print(f"Зашифрованный симметричный ключ сохранён: {config['symmetric_key']}")
    except Exception as e:
        print(f"Ошибка при сохранении зашифрованного симметричного ключа: {e}")
        sys.exit(1)

    print("\nГенерация ключей завершена.\n")


def mode_encrypt(config):
    print("\nРежим шифрования\n")

    private_key = load_private_key(config['secret_key'])

    try:
        with open(config['symmetric_key'], 'rb') as f:
            encrypted_sym_key = f.read()
    except FileNotFoundError:
        print(f"Файл с зашифрованным симметричным ключом не найден: {config['symmetric_key']}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при загрузке симметричного ключа: {e}")
        sys.exit(1)

    symmetric_key = decrypt_symmetric_key(encrypted_sym_key, private_key)
    aes_encrypt_file(config['initial_file'], config['encrypted_file'], symmetric_key)

    print("\nШифрование завершено!\n")


def mode_decrypt(config):
    print("\nРежим расшифрования\n")

    private_key = load_private_key(config['secret_key'])

    try:
        with open(config['symmetric_key'], 'rb') as f:
            encrypted_sym_key = f.read()
    except FileNotFoundError:
        print(f"Файл с зашифрованным симметричным ключом не найден: {config['symmetric_key']}")
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка при загрузке симметричного ключа: {e}")
        sys.exit(1)

    symmetric_key = decrypt_symmetric_key(encrypted_sym_key, private_key)
    aes_decrypt_file(config['encrypted_file'], config['decrypted_file'], symmetric_key)

    print("\nРасшифрование завершено.\n")


def main():
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема (RSA + AES)'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '-gen', '--generation', metavar='CONFIG',
        help='Режим генерации ключей (указать JSON-конфиг)'
    )
    group.add_argument(
        '-enc', '--encryption', metavar='CONFIG',
        help='Режим шифрования (указать JSON-конфиг)'
    )
    group.add_argument(
        '-dec', '--decryption', metavar='CONFIG',
        help='Режим расшифрования (указать JSON-конфиг)'
    )

    args = parser.parse_args()

    if args.generation is not None:
        config = load_config(args.generation)
        mode_generate_keys(config)
    elif args.encryption is not None:
        config = load_config(args.encryption)
        mode_encrypt(config)
    elif args.decryption is not None:
        config = load_config(args.decryption)
        mode_decrypt(config)


if __name__ == '__main__':
    main()