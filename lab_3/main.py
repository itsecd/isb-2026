"""Консольный интерфейс лабораторной работы №3: гибридная криптосистема RSA + 3DES."""

from __future__ import annotations

import argparse
import sys

from config import load_config, pick_value
from hybrid_system import decrypt_file, encrypt_file, generate_keys


def configure_console_encoding() -> None:
    """Включает UTF-8 для русскоязычного вывода, если поток это поддерживает."""
    for stream in (sys.stdout, sys.stderr):
        match hasattr(stream, "reconfigure"):
            case True:
                stream.reconfigure(encoding="utf-8")
            case False:
                pass


def build_parser() -> argparse.ArgumentParser:
    """Создает парсер аргументов командной строки."""
    parser = argparse.ArgumentParser(
        description="Лабораторная работа №3: гибридная криптосистема RSA + 3DES",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true", help="генерация ключей")
    group.add_argument("-enc", "--encryption", action="store_true", help="шифрование файла")
    group.add_argument("-dec", "--decryption", action="store_true", help="дешифрование файла")

    parser.add_argument("-c", "--config", help="путь к JSON-файлу с настройками")
    parser.add_argument("--key-bits", type=int, choices=(64, 128, 192), help="длина ключа 3DES")
    parser.add_argument("--input-file", help="исходный файл для шифрования или дешифрования")
    parser.add_argument("--output-file", help="файл для сохранения результата")
    parser.add_argument("--encrypted-symmetric-key", help="файл с зашифрованным ключом 3DES")
    parser.add_argument("--public-key", help="файл открытого RSA-ключа")
    parser.add_argument("--private-key", help="файл закрытого RSA-ключа")
    return parser


def run_generation(args: argparse.Namespace, config: dict) -> None:
    """Запускает сценарий генерации ключей."""
    encrypted_symmetric_key = pick_value(args, config, "encrypted_symmetric_key")
    public_key = pick_value(args, config, "public_key")
    private_key = pick_value(args, config, "private_key")
    key_bits = int(pick_value(args, config, "key_bits", required=False, default=192))

    print("[1/4] Генерация симметричного ключа 3DES")
    print("[2/4] Генерация пары RSA-ключей")
    generate_keys(encrypted_symmetric_key, public_key, private_key, key_bits)
    print(f"[3/4] Открытый ключ сохранен: {public_key}")
    print(
        "[4/4] Закрытый ключ и зашифрованный 3DES-ключ сохранены: "
        f"{private_key}, {encrypted_symmetric_key}",
    )
    print("Готово: ключи гибридной системы сгенерированы.")


def run_encryption(args: argparse.Namespace, config: dict) -> None:
    """Запускает сценарий шифрования файла."""
    input_file = pick_value(args, config, "input_file")
    private_key = pick_value(args, config, "private_key")
    encrypted_symmetric_key = pick_value(args, config, "encrypted_symmetric_key")
    output_file = pick_value(args, config, "output_file")

    print("[1/3] Расшифровка симметричного ключа закрытым RSA-ключом")
    print("[2/3] Шифрование файла алгоритмом 3DES/CBC")
    encrypt_file(input_file, private_key, encrypted_symmetric_key, output_file)
    print(f"[3/3] Зашифрованный файл сохранен: {output_file}")
    print("Готово: файл зашифрован.")


def run_decryption(args: argparse.Namespace, config: dict) -> None:
    """Запускает сценарий дешифрования файла."""
    input_file = pick_value(args, config, "input_file")
    private_key = pick_value(args, config, "private_key")
    encrypted_symmetric_key = pick_value(args, config, "encrypted_symmetric_key")
    output_file = pick_value(args, config, "output_file")

    print("[1/3] Расшифровка симметричного ключа закрытым RSA-ключом")
    print("[2/3] Дешифрование файла алгоритмом 3DES/CBC")
    decrypt_file(input_file, private_key, encrypted_symmetric_key, output_file)
    print(f"[3/3] Расшифрованный файл сохранен: {output_file}")
    print("Готово: файл расшифрован.")


def main() -> None:
    """Разбирает аргументы и выполняет выбранный сценарий."""
    configure_console_encoding()
    parser = build_parser()
    args = parser.parse_args()
    config = load_config(args.config)

    try:
        match True:
            case _ if args.generation:
                run_generation(args, config)
            case _ if args.encryption:
                run_encryption(args, config)
            case _ if args.decryption:
                run_decryption(args, config)
    except Exception as error:
        parser.exit(status=1, message=f"Ошибка: {error}\n")


if __name__ == "__main__":
    main()
