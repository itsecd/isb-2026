"""
Гибридная криптосистема: SM4 (симметричный) + RSA (асимметричный)
Лабораторная работа №3, вариант 7

Использование:
  python main.py --settings settings.json -gen
  python main.py --settings settings.json -enc
  python main.py --settings settings.json -dec
"""

import argparse
import sys
from crypto.file_utils import load_settings
from crypto.scenarios import generate_keys, encrypt_file, decrypt_file


def main():
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема SM4 + RSA"
    )
    parser.add_argument(
        "--settings", default="crypto/settings.json",
        help="Путь к JSON-файлу с настройками (по умолчанию: crypto/settings.json)"
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true",
                       help="Режим генерации ключей")
    group.add_argument("-enc", "--encryption", action="store_true",
                       help="Режим шифрования файла")
    group.add_argument("-dec", "--decryption", action="store_true",
                       help="Режим дешифрования файла")

    args = parser.parse_args()
    try:
        cfg = load_settings(args.settings)
    except Exception as e:
        print(f"[!] Ошибка загрузки настроек: {e}")
        sys.exit(1)

    try:
        if args.generation:
            generate_keys(cfg)
        elif args.encryption:
            encrypt_file(cfg)
        elif args.decryption:
            decrypt_file(cfg)
    except Exception as e:
        print(f"[!] Выполнение сценария завершилось ошибкой: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
