import os
import argparse
import settings
from services import generate_keys, encrypt_message, decrypt_text
import json

def load_config(config_path: str) -> dict:
    """
    Загружает настройки путей из JSON-файла.
    
    config_path: Путь к файлу settings.json.
    Возвращает словарь с настройками.
    """
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def parse_args() -> argparse.Namespace:
    """
        Парсит аргументы командной строки

        Возвращает аргументы
    """
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
    args = parse_args()

    cyph_dir = args.path_to_cyph or settings.SYMMETRIC_KEY_DIR
    pub_dir = args.path_to_public_key or settings.PUBLIC_KEY_DIR
    priv_file = args.path_to_private_key or settings.SECRET_KEY_FILE
    msg_file = args.path_to_message or settings.INITIAL_FILE
    save_dir = args.path_to_save or settings.SAVE_DIR

    sym_key_path = os.path.join(cyph_dir, settings.SYMMETRIC_KEY_FILE)

    action = "generate" if args.generation else "encrypt" if args.encryption else "decrypt"

    match action:
        case "generate":
            generate_keys(cyph_dir, pub_dir, priv_file)
            
        case "encrypt":
            encrypt_message(msg_file, priv_file, sym_key_path, save_dir)
            
        case "decrypt":
            enc_file_path = args.path_to_message or os.path.join(save_dir, settings.ENCRYPTED_FILE)
            decrypt_text(enc_file_path, priv_file, sym_key_path, save_dir)
            
        case _:
            print("Ошибка: Неизвестная операция.")

if __name__ == "__main__":
    main()