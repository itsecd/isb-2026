import json
import argparse
import sys
from cryptography.hazmat.primitives.serialization import (
    load_pem_public_key,
    load_pem_private_key,
)
from key_generator import generate_rsa_keys, save_rsa_keys, generate_aes_key
from encryptor import encrypt_symmetric_key, aes_encrypt_file
from decryptor import decrypt_symmetric_key, aes_decrypt_file
from utils import read_file, write_file

REQUIRED_CONFIG_KEYS = [
    'initial_file', 'encrypted_file', 'decrypted_file',
    'symmetric_key', 'public_key', 'secret_key'
]

def load_key(path: str, key_type: str):
    """Загрузить открытый или закрытый RSA-ключ из PEM-файла."""
    match key_type:
        case "public":
            label = "открытого"
            loader = load_pem_public_key
        case "private":
            label = "закрытого"
            loader = lambda data: load_pem_private_key(data, password=None)
        case _:
            raise ValueError(f"Неизвестный тип ключа: {key_type}")

    data = read_file(path)
    try:
        key = loader(data)
        print(f"Загружен {label} ключ: {path}")
        return key
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке {label} ключа: {e}") from e

def load_config(path: str) -> dict:
    """Загрузить и проверить JSON-конфигурацию."""
    raw = read_file(path, mode='r')
    try:
        config = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError(f"Ошибка чтения JSON в файле {path}: {e}") from e

    missing = [k for k in REQUIRED_CONFIG_KEYS if k not in config]
    match len(missing):
        case 0:
            config.setdefault('aes_key_size', 256)
        case _:
            raise ValueError(f"В конфигурации не хватает ключей: {', '.join(missing)}")

    return config

def mode_generate_keys(config: dict) -> None:
    """Режим генерации ключей."""
    print("\nРежим генерации ключей\n")
    key_size = config['aes_key_size']
    
    match key_size:
        case 128 | 192 | 256:
            print(f"Принят допустимый размер ключа AES: {key_size} бит")
        case _:
            print(f"Некорректная длина ключа AES: {key_size}. Будет использован 256.")
            key_size = 256

    symmetric_key = generate_aes_key(key_size)
    private_key, public_key = generate_rsa_keys()
    save_rsa_keys(private_key, public_key, config['secret_key'], config['public_key'])

    encrypted_sym_key = encrypt_symmetric_key(symmetric_key, public_key)
    write_file(config['symmetric_key'], encrypted_sym_key)
    print(f"Зашифрованный симметричный ключ сохранён: {config['symmetric_key']}")
    print("\nГенерация ключей завершена.\n")

def mode_encrypt(config: dict, public_key_path: str = None) -> None:
    """Режим шифрования с поддержкой пользовательского ключа."""
    print("\nРежим шифрования\n")
    
    match public_key_path:
        case None:
            private_key = load_key(config['secret_key'], "private")
            symmetric_key = decrypt_symmetric_key(read_file(config['symmetric_key']), private_key)
        case _:
            public_key = load_key(public_key_path, "public")
            symmetric_key = generate_aes_key(config['aes_key_size'])
            encrypted_sym_key = encrypt_symmetric_key(symmetric_key, public_key)
            write_file(config['symmetric_key'], encrypted_sym_key)
            print(f"Зашифрованный симметричный ключ сохранён: {config['symmetric_key']}")

    aes_encrypt_file(config['initial_file'], config['encrypted_file'], symmetric_key)
    print("\nШифрование завершено!\n")

def mode_decrypt(config: dict, private_key_path: str = None) -> None:
    """Режим расшифрования с поддержкой пользовательского ключа."""
    print("\nРежим расшифрования\n")
    
    match private_key_path:
        case None:
            key_path = config['secret_key']
        case _:
            key_path = private_key_path

    private_key = load_key(key_path, "private")
    symmetric_key = decrypt_symmetric_key(read_file(config['symmetric_key']), private_key)
    aes_decrypt_file(config['encrypted_file'], config['decrypted_file'], symmetric_key)
    print("\nРасшифрование завершено.\n")

def main() -> None:
    parser = argparse.ArgumentParser(description='Гибридная криптосистема (RSA + AES)')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', metavar='CONFIG')
    group.add_argument('-enc', '--encryption', metavar='CONFIG')
    group.add_argument('-dec', '--decryption', metavar='CONFIG')
    parser.add_argument('--public-key', default=None, help='Путь к вашему открытому ключу')
    parser.add_argument('--private-key', default=None, help='Путь к вашему закрытому ключу')

    args = parser.parse_args()
    config_path = args.generation or args.encryption or args.decryption

    try:
        config = load_config(config_path)
    except Exception as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        match (args.generation, args.encryption, args.decryption):
            case (cfg, None, None):
                mode_generate_keys(config)
            case (None, cfg, None):
                mode_encrypt(config, args.public_key)
            case (None, None, cfg):
                mode_decrypt(config, args.private_key)
            case _:
                raise RuntimeError("Некорректный режим выполнения")
    except Exception as e:
        print(f"Ошибка выполнения: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main()
