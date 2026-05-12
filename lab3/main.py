import argparse
import file_io
import scenarios


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (ChaCha20 + RSA). Вариант 3.",
    )
    parser.add_argument("-s", "--settings", default="settings.json", metavar="PATH", help="Путь к JSON-файлу с настройками (по умолчанию: settings.json)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation",  action="store_true", help="1: генерация ключей")
    group.add_argument("-enc", "--encryption",  action="store_true", help="2: шифрование файла")
    group.add_argument("-dec", "--decryption",  action="store_true", help="3: дешифрование файла")

    args = parser.parse_args()
    
    cfg = file_io.load_settings(args.settings)

    if args.generation:
        scenarios.generate_keys(
            nonce_path=cfg["nonce"],
            encrypted_sym_key_path=cfg["encrypted_symmetric_key"],
            public_key_path=cfg["public_key"],
            private_key_path=cfg["private_key"],
        )
    elif args.encryption:
        scenarios.encrypt_data(
            input_file=cfg["initial_file"],
            private_key_path=cfg["private_key"],
            encrypted_sym_key_path=cfg["encrypted_symmetric_key"],
            nonce_path=cfg["nonce"],
            output_file=cfg["encrypted_file"],
        )
    elif args.decryption:
        scenarios.decrypt_data(
            input_file=cfg["encrypted_file"],
            private_key_path=cfg["private_key"],
            encrypted_sym_key_path=cfg["encrypted_symmetric_key"],
            nonce_path=cfg["nonce"],
            output_file=cfg["decrypted_file"],
        )


if __name__ == "__main__":
    main()
