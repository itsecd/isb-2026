'''Консольный интерфейс гибридной криптосистемы RSA + 3DES.

Режимы:
    -gen (--generation): генерация ключей.
    -enc (--encryption): шифрование файла.
    -dec (--decryption): дешифрование файла.

Настройки загружаются из JSON-файла (по умолчанию config.json).
'''

import argparse
from config_utils import load_config
from hybrid_utils import generate_all_keys, encrypt_file, decrypt_file


def main():
    '''Точка входа консольного интерфейса.'''
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + 3DES")

    parser.add_argument("-c", "--config", default="config.json", help="Путь к JSON-файлу настроек")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true", help="Генерация ключей")
    group.add_argument("-enc", "--encryption", action="store_true", help="Шифрование файла")
    group.add_argument("-dec", "--decryption", action="store_true", help="Дешифрование файла")

    parser.add_argument("--key-size", type=int, choices=[64, 128, 192], help="Размер ключа 3DES в битах")

    parser.add_argument("--input", help="Путь к исходному файлу")
    parser.add_argument("--output", help="Путь к выходному файлу")
    parser.add_argument("--pub-key", help="Путь к открытому ключу RSA")
    parser.add_argument("--priv-key", help="Путь к закрытому ключу RSA")
    parser.add_argument("--enc-key", help="Путь к зашифрованному ключу 3DES")

    args = parser.parse_args()
    settings = load_config(args.config)

    if args.key_size:
        settings["key_size"] = args.key_size
    if args.input:
        settings["input_file"] = args.input
    if args.output:
        if args.generation:
            pass
        elif args.encryption:
            settings["encrypted_file"] = args.output
        elif args.decryption:
            settings["decrypted_file"] = args.output
    if args.pub_key:
        settings["public_key_file"] = args.pub_key
    if args.priv_key:
        settings["private_key_file"] = args.priv_key
    if args.enc_key:
        settings["encrypted_key_file"] = args.enc_key

    match True:
        case _ if args.generation:
            print("[1/3] Генерирую ключи RSA и 3DES...")
            generate_all_keys(
                settings["encrypted_key_file"],
                settings["public_key_file"],
                settings["private_key_file"],
                int(settings["key_size"])
            )
            print(f"[2/3] Открытый ключ RSA сохранён: {settings['public_key_file']}")
            print(f"[2/3] Закрытый ключ RSA сохранён: {settings['private_key_file']}")
            print(f"[3/3] Зашифрованный ключ 3DES сохранён: {settings['encrypted_key_file']}")
            print("Готово: ключи созданы")

        case _ if args.encryption:
            print(f"[1/2] Шифрую файл: {settings['input_file']}...")
            encrypt_file(
                settings["input_file"],
                settings["public_key_file"],
                settings["encrypted_key_file"],
                settings["encrypted_file"]
            )
            print(f"[2/2] Файл зашифрован: {settings['encrypted_file']}")

        case _ if args.decryption:
            print(f"[1/2] Расшифровываю файл: {settings['encrypted_file']}...")
            decrypt_file(
                settings["encrypted_file"],
                settings["private_key_file"],
                settings["encrypted_key_file"],
                settings["decrypted_file"]
            )
            print(f"[2/2] Файл расшифрован: {settings['decrypted_file']}")


if __name__ == "__main__":
    main()