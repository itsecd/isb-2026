#!/usr/bin/env python3

import argparse
import sys
from pathlib import Path

import config
import file_utils as fu
import crypto


def mode_generate(settings: dict) -> None:
    """Режим генерации ключей гибридной системы."""
    print("\nГенерация ключей")

    sym_key = crypto.generate_symmetric_key()
    print(f"Ключ SEED создан ({len(sym_key)} байт)")

    private_key, public_key = crypto.generate_rsa_keys()

    print("Сохранение RSA-ключей")
    fu.write_bytes(settings['public_key'], crypto.serialize_public_key(public_key))
    fu.write_bytes(settings['private_key'], crypto.serialize_private_key(private_key))

    enc_sym_key = crypto.rsa_encrypt_key(sym_key, public_key)
    fu.write_bytes(settings['symmetric_key'], enc_sym_key)

    print("\nВсе ключи сохранены:")
    print(f"\nПубличный ключ: {settings['public_key']}")
    print(f"\nПриватный ключ: {settings['private_key']}")
    print(f"\nЗашифрованный SEED: {settings['symmetric_key']}")


def mode_encrypt(settings: dict) -> None:
    """Режим шифрования файла."""
    print("\nШифрование файла")

    print("Загрузка ключей")
    private_key = crypto.deserialize_private_key(
        fu.read_bytes(settings['private_key'])
    )
    enc_sym_key = fu.read_bytes(settings['symmetric_key'])
    sym_key = crypto.rsa_decrypt_key(enc_sym_key, private_key)

    text = fu.read_text(settings['initial_file'])
    data = text.encode('utf-8')
    print(f"Размер исходных данных: {len(data)} байт")

    iv = crypto.generate_iv()
    padded = crypto.pad_data(data)
    encrypted = crypto.seed_encrypt(padded, sym_key, iv)
    print(f"Размер зашифрованных данных: {len(encrypted)} байт")

    fu.write_bytes(settings['encrypted_file'], iv + encrypted)

    print(f"\n Файл зашифрован: {settings['encrypted_file']}")


def mode_decrypt(settings: dict) -> None:
    """Режим дешифрования файла."""
    print("\nДешифрование файла ")

    print("Загрузка ключей...")
    private_key = crypto.deserialize_private_key(
        fu.read_bytes(settings['private_key'])
    )
    enc_sym_key = fu.read_bytes(settings['symmetric_key'])
    sym_key = crypto.rsa_decrypt_key(enc_sym_key, private_key)

    encrypted_data = fu.read_bytes(settings['encrypted_file'])

    iv = encrypted_data[:crypto.IV_SIZE]
    ciphertext = encrypted_data[crypto.IV_SIZE:]
    print(f"IV извлечён ({len(iv)} байт), шифротекст ({len(ciphertext)} байт)")

    decrypted_padded = crypto.seed_decrypt(ciphertext, sym_key, iv)
    original_data = crypto.unpad_data(decrypted_padded)

    text = original_data.decode('utf-8')
    fu.write_text(settings['decrypted_file'], text)

    print(f"\nФайл расшифрован: {settings['decrypted_file']}")


def create_parser() -> argparse.ArgumentParser:
    """Создаёт парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description='Гибридная криптосистема (SEED + RSA)'
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-gen', '--generate', action='store_true',
                       help='Генерация ключей')
    group.add_argument('-enc', '--encrypt', action='store_true',
                       help='Шифрование файла')
    group.add_argument('-dec', '--decrypt', action='store_true',
                       help='Дешифрование файла')
    parser.add_argument('-c', '--config', default='settings.json',
                        help='Путь к файлу конфигурации (по умолчанию settings.json)')
    return parser


def main() -> None:
    """Точка входа."""
    parser = create_parser()
    args = parser.parse_args()

    try:
        settings = config.load_config(args.config)
        config.ensure_directories(settings)
        print("Конфигурация загружена\n")

        match (args.generate, args.encrypt, args.decrypt):
            case (True, False, False):
                mode_generate(settings)
            case (False, True, False):
                mode_encrypt(settings)
            case (False, False, True):
                mode_decrypt(settings)
            case _:
                print("Неизвестный режим работы")
                sys.exit(1)

    except Exception as e:
        print(f"\nОшибка: {e}")
        sys.exit(1)


    print("Работа завершена")



if __name__ == "__main__":
    main()