import os
import argparse
from services import generate_keys, encrypt_message, decrypt_text
import json


def read_json(config_path: str = "settings.json") -> dict:
    """Читает настройки из JSON-файла."""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Конфигурационный файл '{config_path}' не найден.")
        return {}


def parse_args() -> argparse.Namespace:
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description="Утилита для шифрования")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generation', action='store_true', help='Запускает режим генерации ключей')
    group.add_argument('-enc', '--encryption', action='store_true', help='Запускает режим шифрования')
    group.add_argument('-dec', '--decryption', action='store_true', help='Запускает режим дешифрования')
    
    parser.add_argument('--path_to_cyph', help='Путь к директории зашифрованного симметричного ключа')
    parser.add_argument('--path_to_public_key', help='Путь к директории открытого ключа')
    parser.add_argument('--path_to_private_key', help='Путь к файлу закрытого ключа')
    parser.add_argument('--path_to_message', help='Путь к файлу для шифрования/дешифрования')
    parser.add_argument('--path_to_save', help='Путь к сохраненному файлу')
    
    return parser.parse_args()


def main():
    try:
        args = parse_args()
        config = read_json()
        
        cyph_dir = args.path_to_cyph or config.get("SYMMETRIC_KEY_DIR", "./keys")
        pub_dir = args.path_to_public_key or config.get("PUBLIC_KEY_DIR", "./keys")
        priv_file = args.path_to_private_key or config.get("SECRET_KEY_FILE", "./keys/private.pem")
        msg_file = args.path_to_message or config.get("INITIAL_FILE", "message.txt")
        save_dir = args.path_to_save or config.get("SAVE_DIR", "./output")
        sym_key_path = os.path.join(cyph_dir, config.get("SYMMETRIC_KEY_FILE", "symmetric_encrypted.txt"))
        
        action = "generate" if args.generation else "encrypt" if args.encryption else "decrypt"
        
        if action == "generate":
            generate_keys(cyph_dir, pub_dir, priv_file)
        elif action == "encrypt":
            encrypt_message(msg_file, priv_file, sym_key_path, save_dir)
        else:
            enc_file_path = args.path_to_message or os.path.join(save_dir, config.get("ENCRYPTED_FILE", "encrypted.txt"))
            decrypt_text(enc_file_path, priv_file, sym_key_path, save_dir)
            
    except Exception as e:
        print(f"\nКритическая ошибка выполнения: {e}")


if __name__ == "__main__":
    main()