import argparse
import file_io
import scenarios


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Гибридная криптосистема (ChaCha20 + RSA). Вариант 3.",
    )
    parser.add_argument("-s", "--settings", default="settings.json", metavar="PATH", help="Путь к JSON-файлу с настройками (по умолчанию: settings.json)")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-gen", "--generation", action="store_true", help="1: генерация ключей")
    group.add_argument("-enc", "--encryption", action="store_true", help="2: шифрование файла")
    group.add_argument("-dec", "--decryption", action="store_true", help="3: дешифрование файла")
    parser.add_argument("-pub", "--public-key", metavar="PATH", help="Путь к открытому ключу")
    parser.add_argument("-priv", "--private-key", metavar="PATH", help="Путь к закрытому ключу")
    parser.add_argument("-sym", "--encrypted-sym-key", metavar="PATH", help="Путь к зашифрованному симметричному ключу")
    parser.add_argument("-n", "--nonce", metavar="PATH", help="Путь к файлу nonce")

    args = parser.parse_args()

    try:
        cfg = file_io.load_settings(args.settings)
    except Exception as e:
        raise RuntimeError(f"Ошибка загрузки настроек: {e}")

    match args:
        case _ if args.public_key:
            cfg["public_key"] = args.public_key
        case _ if args.private_key:
            cfg["private_key"] = args.private_key
        case _ if args.encrypted_sym_key:
            cfg["encrypted_symmetric_key"] = args.encrypted_sym_key
        case _ if args.nonce:
            cfg["nonce"] = args.nonce

    nonce_size = cfg["nonce_size"]
    key_size = cfg["key_size"]

    try:
        match args:
            case _ if args.generation:
                scenarios.generate_keys(
                    nonce_path=cfg["nonce"],
                    encrypted_sym_key_path=cfg["encrypted_symmetric_key"],
                    public_key_path=cfg["public_key"],
                    private_key_path=cfg["private_key"],
                    key_size=key_size,
                    nonce_size=nonce_size,
                )
            case _ if args.encryption:
                scenarios.encrypt_data(
                    input_file=cfg["initial_file"],
                    private_key_path=cfg["private_key"],
                    encrypted_sym_key_path=cfg["encrypted_symmetric_key"],
                    nonce_path=cfg["nonce"],
                    output_file=cfg["encrypted_file"],
                    nonce_size=nonce_size,
                )
            case _ if args.decryption:
                scenarios.decrypt_data(
                    input_file=cfg["encrypted_file"],
                    private_key_path=cfg["private_key"],
                    encrypted_sym_key_path=cfg["encrypted_symmetric_key"],
                    nonce_path=cfg["nonce"],
                    output_file=cfg["decrypted_file"],
                    nonce_size=nonce_size,
                )
            case _:
                raise ValueError("Не указано действие")
    except Exception as e:
        raise RuntimeError(f"Ошибка выполнения: {e}")


if __name__ == "__main__":
    main()
