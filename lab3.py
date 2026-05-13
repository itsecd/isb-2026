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
from utils import fail, read_file, write_file


def load_key(path: str, key_type: str):
    """Загрузка открытого или закрытого ключа."""
    match key_type:
        case "public":
            label = "открытого"
            loader = load_pem_public_key
        case "private":
            label = "закрытого"
            loader = lambda data: load_pem_private_key(data, password=None)
        case _:
            fail(f"Неизвестный тип ключа: {key_type}")

    data = read_file(path)
    try:
        key = loader(data)
        print(f"Загружен {label} ключ: {path}")
        return key
    except Exception as e:
        fail(f"Ошибка при загрузке {label} ключа: {e}")


def load_config(path: str) -> dict:
    """Загрузка JSON-конфигурации."""
    raw = read_file(path, mode='r')
    try:
        config = json.loads(raw)
    except json.JSONDecodeError as e:
        fail(f"Ошибка чтения JSON в файле {path}: {e}")

    required_keys = [
        'initial_file', 'encrypted_file', 'decrypted_file',
        'symmetric_key', 'public_key', 'secret_key'
    ]
    missing = [k for k in required_keys if k not in config]
    if missing:
        fail(f"В конфигурации не хватает ключей: {', '.join(missing)}")

    config.setdefault('aes_key_size', 256)
    return config


def _read_and_decrypt_symmetric_key(symmetric_key_path: str, private_key) -> bytes:
    """Загрузка зашифрованного симметричного ключа и его расшифрование."""
    encrypted_key = read_file(symmetric_key_path)
    return decrypt_symmetric_key(encrypted_key, private_key)


def mode_generate_keys(config: dict) -> None:
    """Режим генерации ключей."""
    print("\nРежим генерации ключей\n")

    key_size = config['aes_key_size']
    match key_size:
        case 128 | 192 | 256:
            pass
        case _:
            print(f"Некорректная длина ключа AES: {key_size}. Использую 256.")
            key_size = 256

    symmetric_key = generate_aes_key(key_size)
    private_key, public_key = generate_rsa_keys()

    save_rsa_keys(private_key, public_key, config['secret_key'], config['public_key'])

    encrypted_sym_key = encrypt_symmetric_key(symmetric_key, public_key)
    write_file(config['symmetric_key'], encrypted_sym_key)
    print(f"Зашифрованный симметричный ключ сохранён: {config['symmetric_key']}")

    print("\nГенерация ключей завершена.\n")


def mode_encrypt(config: dict) -> None:
    """Режим шифрования."""
    print("\nРежим шифрования\n")
    private_key = load_key(config['secret_key'], "private")
    symmetric_key = _read_and_decrypt_symmetric_key(config['symmetric_key'], private_key)
    aes_encrypt_file(config['initial_file'], config['encrypted_file'], symmetric_key)
    print("\nШифрование завершено!\n")


def mode_decrypt(config: dict) -> None:
    """Режим расшифрования."""
    print("\nРежим расшифрования\n")
    private_key = load_key(config['secret_key'], "private")
    symmetric_key = _read_and_decrypt_symmetric_key(config['symmetric_key'], private_key)
    aes_decrypt_file(config['encrypted_file'], config['decrypted_file'], symmetric_key)
    print("\nРасшифрование завершено.\n")


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема (RSA + AES)'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', metavar='CONFIG')
    group.add_argument('-enc', '--encryption', metavar='CONFIG')
    group.add_argument('-dec', '--decryption', metavar='CONFIG')

    args = parser.parse_args()

    match args:
        case _ if args.generation is not None:
            config = load_config(args.generation)
            mode_generate_keys(config)
        case _ if args.encryption is not None:
            config = load_config(args.encryption)
            mode_encrypt(config)
        case _ if args.decryption is not None:
            config = load_config(args.decryption)
            mode_decrypt(config)


if __name__ == '__main__':
    main()
