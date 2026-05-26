import argparse
import sys
import workflow
import crypto_storage as storage


def collect_arguments() -> argparse.Namespace:
    """
    Настраивает и разбирает аргументы командной строки.
    Требует указания одного из режимов: генерация, шифрование или дешифрование.
    """
    parser = argparse.ArgumentParser(description="Гибридная криптосистема RSA+Blowfish (Lab 3)")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--gen-keys", action="store_true", help="Режим генерации ключей")
    mode_group.add_argument("--encrypt", action="store_true", help="Режим шифрования")
    mode_group.add_argument("--decrypt", action="store_true", help="Режим дешифрования")

    parser.add_argument("--config", default="path.json", help="Путь к JSON-конфигурации")
    parser.add_argument("--input-file", help="Путь к входному файлу")
    parser.add_argument("--output-file", help="Путь к выходному файлу")
    parser.add_argument("--sym-key-path", help="Путь к зашифрованному симметричному ключу")
    parser.add_argument("--priv-key-path", help="Путь к приватному RSA-ключу")
    parser.add_argument("--pub-key-path", help="Путь к публичному RSA-ключу")
    parser.add_argument("--key-size", type=int, choices=range(32, 449, 8), default=128,
                        help="Длина ключа Blowfish в битах (32-448, шаг 8)")
    return parser.parse_args()


def main() -> None:
    """
    Точка входа приложения. Определяет режим работы и вызывает соответствующий модуль workflow.
    """
    args = collect_arguments()
    
    try:
        config = storage.open_json(args.config)
    except Exception as e:
        print(f"Ошибка чтения конфигурации {args.config}: {e}", file=sys.stderr)
        sys.exit(1)

    sym_key = args.sym_key_path or config.get("sym_key", "keys/session_key.enc")
    priv_key = args.priv_key_path or config.get("private_key", "keys/private.pem")
    pub_key = args.pub_key_path or config.get("public_key", "keys/public.pem")
    
    src_file = args.input_file or config.get("initial_file", "data/original.txt")
    dst_file = args.output_file or config.get("encrypted_file", "data/encrypted.bin")

    try:
        if args.gen_keys:
            workflow.run_key_generation(sym_key, priv_key, pub_key, args.key_size)
        elif args.encrypt:
            workflow.run_encryption(src_file, dst_file, sym_key, priv_key)
        elif args.decrypt:
            dst_file = args.output_file or config.get("decrypted_file", "data/decrypted.txt")
            workflow.run_decryption(src_file, dst_file, sym_key, priv_key)
    except Exception as error:
        print(f"Критическая ошибка выполнения: {error}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
