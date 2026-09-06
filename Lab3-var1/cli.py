#!/usr/bin/env python3
"""
Интерфейс командной строки для гибридной криптосистемы (AES + RSA).
Поддерживает три режима: генерация ключей, шифрование, дешифрование.
"""

import argparse
import os
from crypto_utils import (
    generate_aes_key,
    encrypt_aes_data,
    decrypt_aes_data,
    generate_rsa_keypair,
    save_rsa_private_key,
    save_rsa_public_key,
    load_rsa_private_key,
    encrypt_symmetric_key_rsa,
    decrypt_symmetric_key_rsa,
)
from config_manager import load_settings


def _load_aes_key(private_key_path: str, enc_key_path: str) -> bytes:
    """
    Вспомогательная функция: загружает закрытый RSA-ключ, читает зашифрованный
    AES-ключ из файла, расшифровывает его и возвращает открытый AES-ключ.
    Используется в режимах шифрования и расшифровки для устранения дублирования.
    """
    rsa_priv = load_rsa_private_key(private_key_path)
    with open(enc_key_path, 'rb') as f:
        enc_aes_key = f.read()
    return decrypt_symmetric_key_rsa(enc_aes_key, rsa_priv)


def mode_generation(args):
    """
    Генерирует AES- и RSA-ключи, шифрует AES-ключ открытым RSA-ключом,
    сохраняет все файлы.

    :param args: аргументы командной строки, содержащие пути и размер AES-ключа
    :return: None
    """
    print("Генерация ключей...")
    print(f"Размер AES ключа: {args.aes_key_size} бит")
    aes_key = generate_aes_key(args.aes_key_size)

    print("Генерация RSA ключей (2048 бит)...")
    rsa_priv, rsa_pub = generate_rsa_keypair()

    print("Шифрование AES ключа открытым RSA ключом...")
    enc_aes_key = encrypt_symmetric_key_rsa(aes_key, rsa_pub)

    os.makedirs(os.path.dirname(args.public_key_path), exist_ok=True)
    os.makedirs(os.path.dirname(args.private_key_path), exist_ok=True)
    os.makedirs(os.path.dirname(args.enc_symmetric_key_path), exist_ok=True)

    save_rsa_public_key(rsa_pub, args.public_key_path)
    print(f"Открытый RSA ключ сохранён: {args.public_key_path}")

    save_rsa_private_key(rsa_priv, args.private_key_path)
    print(f"Закрытый RSA ключ сохранён: {args.private_key_path}")

    with open(args.enc_symmetric_key_path, 'wb') as f:
        f.write(enc_aes_key)
    print(f"Зашифрованный AES ключ сохранён: {args.enc_symmetric_key_path}")

    print("Генерация ключей завершена.")


def mode_encryption(args):
    """
    Шифрует файл с использованием гибридной схемы:
    - загружает закрытый RSA ключ,
    - расшифровывает AES ключ,
    - шифрует входной файл алгоритмом AES.

    :param args: аргументы командной строки с путями к файлам
    :return: None
    """

    aes_key = _load_aes_key(args.private_key_path, args.enc_symmetric_key_path)


    with open(args.input_file, 'rb') as f:
        plaintext = f.read()


    encrypted_data = encrypt_aes_data(plaintext, aes_key)


    with open(args.output_file, 'wb') as f:
        f.write(encrypted_data)

    print(f"Файл зашифрован: {args.input_file} -> {args.output_file}")
    print("Шифрование завершено.")


def mode_decryption(args):
    """
    Расшифровывает файл с использованием гибридной схемы:
    - загружает закрытый RSA ключ,
    - расшифровывает AES ключ,
    - расшифровывает входной файл алгоритмом AES.

    :param args: аргументы командной строки с путями к файлам
    :return: None
    """

    aes_key = _load_aes_key(args.private_key_path, args.enc_symmetric_key_path)


    with open(args.input_file, 'rb') as f:
        encrypted_data = f.read()


    plaintext = decrypt_aes_data(encrypted_data, aes_key)


    with open(args.output_file, 'wb') as f:
        f.write(plaintext)

    print(f"Файл расшифрован: {args.input_file} -> {args.output_file}")
    print("Расшифровка завершена.")


def main():
    """
    Разбирает аргументы командной строки и запускает соответствующий режим.
    """

    settings = load_settings()

    parser = argparse.ArgumentParser(description="Гибридная криптосистема (AES + RSA)")
    subparsers = parser.add_subparsers(dest="command", required=True)

    gen = subparsers.add_parser("gen", help="Сгенерировать ключи")
    gen.add_argument("--aes-key-size", type=int, choices=[128, 192, 256], required=True)
    gen.add_argument("--public-key-path", default=settings.get("public_key_path"))
    gen.add_argument("--private-key-path", default=settings.get("private_key_path"))
    gen.add_argument("--enc-symmetric-key-path", default=settings.get("enc_symmetric_key_path"))


    enc = subparsers.add_parser("enc", help="Зашифровать файл")
    enc.add_argument("--input-file", default=settings.get("default_input_file"))
    enc.add_argument("--private-key-path", default=settings.get("private_key_path"))
    enc.add_argument("--enc-symmetric-key-path", default=settings.get("enc_symmetric_key_path"))
    enc.add_argument("--output-file", default=settings.get("default_encrypted_file"))


    dec = subparsers.add_parser("dec", help="Расшифровать файл")
    dec.add_argument("--input-file", default=settings.get("default_encrypted_file"))
    dec.add_argument("--private-key-path", default=settings.get("private_key_path"))
    dec.add_argument("--enc-symmetric-key-path", default=settings.get("enc_symmetric_key_path"))
    dec.add_argument("--output-file", default=settings.get("default_decrypted_file"))

    args = parser.parse_args()

    match args.command:
        case "gen":
            mode_generation(args)
        case "enc":
            mode_encryption(args)
        case "dec":
            mode_decryption(args)
        case _:
            raise ValueError(f"Неизвестная команда: {args.command}")


if __name__ == "__main__":
    main()