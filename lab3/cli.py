import argparse
from config_utils import load_config
from hybrid_utils import generate_all_keys, encrypt_file, decrypt_file


def main():
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA + 3DES")
    parser.add_argument("-c", "--config", default="config.json", help="Путь к JSON-файлу настроек")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true", help="Генерация ключей")
    group.add_argument("-enc", "--encryption", action="store_true", help="Шифрование файла")
    group.add_argument("-dec", "--decryption", action="store_true", help="Дешифрование файла")

    args = parser.parse_args()
    settings = load_config(args.config)

    match True:
        case _ if args.generation:
            print("[1/3] Ключи генерируются RSA и 3DES...")
            generate_all_keys(
                settings["encrypted_key_file"],
                settings["public_key_file"],
                settings["private_key_file"],
                int(settings["key_size"])
            )
            print("[2/3] Ключи RSA сохранены...")
            print("[3/3] Зашифрованный ключ 3DES сохранён...")
            print("Готово: ключи созданы")

        case _ if args.encryption:
            print("[1/2] Файл шифруется...")
            encrypt_file(
                settings["input_file"],
                settings["public_key_file"],
                settings["encrypted_key_file"],
                settings["encrypted_file"]
            )
            print("[2/2] Файл зашифрован...")
            print("Готово: " + settings["encrypted_file"])

        case _ if args.decryption:
            print("[1/2] Файл расшифровывается...")
            decrypt_file(
                settings["encrypted_file"],
                settings["private_key_file"],
                settings["encrypted_key_file"],
                settings["decrypted_file"]
            )
            print("[2/2] Файл расшифрован...")
            print("Готово: " + settings["decrypted_file"])


if __name__ == "__main__":
    main()